import os
import math

from Player import Player
from Color import Color
import random
from Type import Type
from Status import Status
from Vote import Vote
from tabulate import tabulate
from operator import itemgetter
from PrivateState import PrivateState
from OpponentState import OpponentState

class GameInstance:
    
    def __init__(self,server):

        self.doorNineOpen = False
        self.server = server
        self.PlayerArray = []
        self.GameStarted = False
        self.ColorSets = {}
        self.InitializeColorSets()
        self.GameIterations = 0
        self.CurrentColorSet = []
        self.CurrentDoorSet = []
        self.ProposedColorCombo = ""
        self.CurrentVotes = {}
        self.CurrentVotes["a"] = []
        self.CurrentVotes["b"] = []
        self.CurrentVotes["c"] = []
        self.AmbidexGameRound = {}
        self.cyanLot = []
        self.yellowLot = []
        self.magentaLot = []
        self.redLot = []
        self.greenLot = []
        self.blueLot = []
        self.ColorLotMapping = {Color.CYAN: self.cyanLot, Color.YELLOW: self.yellowLot, Color.MAGENTA: self.magentaLot, Color.RED: self.redLot, Color.GREEN: self.greenLot, Color.BLUE: self.blueLot}
        self.lookupCombi = {"RED SOLO": (0,1,2), "RED PAIR": (0,2,1), "GREEN SOLO": (1,2,0), "GREEN PAIR":(1,0,2), "BLUE SOLO": (2,0,1), "BLUE PAIR": (2,1,0),"CYAN SOLO": (0,1,2), "CYAN PAIR": (0,2,1), "MAGENTA SOLO": (1,2,0), "MAGENTA PAIR":(1,0,2), "YELLOW SOLO": (2,0,1), "YELLOW PAIR": (2,1,0)}
        self.combinations = {"a": [[],[],[]], "b": [[],[],[]], "c": [[],[],[]]}
        self.playerObjectives = {}



    def InitializeColors(self):
        self.ColorSets["Primary Colors"] = [Color.RED,Color.GREEN,Color.BLUE]
        self.ColorSets["Complementary Colors"] = [Color.CYAN,Color.YELLOW,Color.MAGENTA]
        self.ColorSets["RedSolo|RedPair"] = {"RED SOLO": Color.CYAN, "RED PAIR": Color.CYAN, "GREEN SOLO": Color.MAGENTA, "GREEN PAIR": Color.MAGENTA, "BLUE SOLO": Color.YELLOW, "BLUE PAIR": Color.YELLOW }
        self.ColorSets["RedSolo|GreenPair"] = {"RED SOLO": Color.YELLOW, "RED PAIR": Color.MAGENTA, "GREEN SOLO": Color.CYAN, "GREEN PAIR": Color.YELLOW, "BLUE SOLO": Color.MAGENTA, "BLUE PAIR": Color.CYAN }
        self.ColorSets["RedSolo|BluePair"] = {"RED SOLO": Color.MAGENTA, "RED PAIR": Color.YELLOW, "GREEN SOLO": Color.YELLOW, "GREEN PAIR": Color.CYAN, "BLUE SOLO": Color.CYAN, "BLUE PAIR": Color.MAGENTA }
        self.ColorSets["CyanSolo|CyanPair"] = {"CYAN SOLO": Color.RED, "CYAN PAIR": Color.RED, "YELLOW SOLO": Color.BLUE, "YELLOW PAIR": Color.BLUE, "MAGENTA SOLO": Color.GREEN, "MAGENTA PAIR": Color.GREEN }
        self.ColorSets["CyanSolo|YellowPair"] = {"CYAN SOLO": Color.GREEN, "CYAN PAIR": Color.BLUE, "YELLOW SOLO": Color.RED, "YELLOW PAIR": Color.GREEN, "MAGENTA SOLO": Color.BLUE, "MAGENTA PAIR": Color.RED }
        self.ColorSets["CyanSolo|MagentaPair"] = {"CYAN SOLO": Color.BLUE, "CYAN PAIR": Color.GREEN, "YELLOW SOLO": Color.GREEN, "YELLOW PAIR": Color.RED, "MAGENTA SOLO": Color.RED, "MAGENTA PAIR": Color.BLUE }



    def createGame(self):
        nameArray = ["Alice","Bob","Carolyn","Dexter","Emily","Frank","Gwen","Haynes","Igor"]
        while(len(nameArray) > 0):
            self.PlayerArray.append(Player(nameArray.pop()))
        print("A new game was created.")
        return PlayerArray;


    def endGame(self):
        self.doorNineOpen = True



    def printPlayers(self):
        messageArray = []
        for player in self.PlayerArray:
            messageArray.append([player.getName(),player.getColor().name,player.getType().name])
            messageArray = sorted(messageArray,key=itemgetter(1,2))
        return tabulate(messageArray, headers=['Name', 'Color','Type'])


    def startGame(self):
        self.GameIterations += 1
        self.randomizeBracelets()
        #self.generatePlayerObjectives()
        


    def randomizeBracelets(self):
        playerSet = self.PlayerArray.copy()
        finalSet = []
        if(self.GameIterations%2 != 0):
            self.CurrentColorSet = self.ColorSets["Primary Colors"]
            self.CurrentDoorSet = self.ColorSets["Complementary Colors"]
        elif(self.GameIterations%2 == 0):
            self.CurrentColorSet = self.ColorSets["Complementary Colors"]
            self.CurrentDoorSet = self.ColorSets["Primary Colors"]
        for color in self.CurrentColorSet:
            player = playerSet[random.randint(0,len(playerSet)-1)]
            playerSet.remove(player)
            player.setColor(color)
            player.setType(Type.SOLO)
            finalSet.append(player)
            for i in range(0,2):
                player = playerSet[random.randint(0,len(playerSet)-1)]
                playerSet.remove(player)
                player.setColor(color)
                player.setType(Type.PAIR)
                finalSet.append(player)
        self.PlayerArray = finalSet




    def getOpponent(self,player):
        colortype = self.getPlayerColorType(player)     #aka "RED SOLO" or etc
        playerdoor = player.getDoor()                   #aka Color.CYAN
        for key in self.ColorSets[self.ProposedColorCombo].keys():
            if(key != colortype and self.ColorSets[self.ProposedColorCombo][key] == playerdoor):
                return key




    def getAmbidexResult(self,playerColorType,opponentColorType):
        playerVote = self.AmbidexGameRound[playerColorType]
        opponentVote = self.AmbidexGameRound[opponentColorType]
        if(playerVote == Vote.ALLY and opponentVote == Vote.ALLY):
            return 2
        elif(playerVote == Vote.ALLY and opponentVote == Vote.BETRAY):
            return -2
        elif(playerVote == Vote.BETRAY and opponentVote == Vote.ALLY):
            return 3
        elif(playerVote == Vote.BETRAY and opponentVote == Vote.BETRAY):
            return 0
        

    #funcao que distribui os players pelas portas , pos votacao
    def setPlayerDoors(self,combi):
        self.setProposedColorCombo(combi)
        for player in self.PlayerArray:
            bracelet = player.getColor().name + " " + player.getType().name
            playerCombi = self.lookupCombi[bracelet]
            if(combi == "a"):
                playerCombi = playerCombi[0]
            elif(combi == "b"):
                playerCombi = playerCombi[1]
            elif(combi == "c"):
                playerCombi = playerCombi[2]
            player.setDoor(self.getDoorFromCombi(playerCombi,player))


    def initPollingDict(self):
        self.CurrentVotes.clear()
        self.CurrentVotes["a"] = []
        self.CurrentVotes["b"] = []
        self.CurrentVotes["c"] = []

    def getAlivePlayers(self):      #it only counts HUMAN players right now
        result = 0
        for player in self.PlayerArray:
            if(player.getStatus() == Status.ALIVE and player.getSpecies() == Species.HUMAN):
                result += 1
        return result

    def clearDoorLots(self):
        self.cyanLot.clear()
        self.yellowLot.clear()
        self.magentaLot.clear()
        self.redLot.clear()
        self.greenLot.clear()
        self.blueLot.clear()

    def checkGameStarted(self):
        return (self.GameStarted)

    def checkPlayer(self,player):
        for p in self.PlayerArray:
            if(p.getName() == player):
                return True
        return False

    def getPlayer(self,player):
        for p in self.PlayerArray:
            if(p.getName() == player):
                return p

    def getPlayerColorType(self,player):
        return player.getColor().name + " " + player.getType().name


    def checkPlayerLimit(self):
        return(len(self.PlayerArray) < 9)


    def getPlayerByTypecolor(self,typecolorString):
        resultArray = []

        for player in self.PlayerArray:
            if(self.getPlayerColorType(player) == typecolorString and player.getStatus() == Status.ALIVE):      #alteraçao feita para o computeVote()
                resultArray.append(player)

        return resultArray


    def parseBotNamesFile(self,filename):
        file = open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), filename),'r')
        names = file.read().splitlines()
        file.close()
        return names




    def generateSingleObjective(self):

        intKill = 15            #between 0 and 14
        intTrapInside = 70           #between 15 and 69
        intEscapeWith = 100     #between 70 and 99
        randomNumber = random.randrange(100)

        if(randomNumber < intKill):
            return "KILL"

        elif(randomNumber >= intKill and randomNumber < intTrapInside):
            return "TRAP_INSIDE"

        elif(randomNumber >= intTrapInside and randomNumber < intEscapeWith):
            return "ESCAPE_WITH"


    def generateObjectiveTarget(self,player):
        
        targets = list(self.PlayerArray)
        targets.remove(player)
        
        randomNumber = random.randrange(len(targets))

        return targets[randomNumber].getName()


    def generatePlayerObjectives(self):
        for player in self.PlayerArray:
            if(player.getSpecies() == Species.HUMAN):
                selectObjective = self.generateSingleObjective()
                selectTarget = self.generateObjectiveTarget(player)
                self.playerObjectives[player.getName()] = (selectObjective, selectTarget)


    def setPlayerCombi(self,player):
        
        colorType = self.getPlayerColorType(player)
        playerCombi = self.lookupCombi[colorType]
        playerLots = [list(self.combinations["a"]),list(self.combinations["b"]),list(self.combinations["c"])]
        print(playerLots)
        playerLots[0][playerCombi[0]].append(player)
        playerLots[1][playerCombi[1]].append(player)
        playerLots[2][playerCombi[2]].append(player)
        self.combinations["a"] = playerLots[0]
        self.combinations["b"] = playerLots[1]
        self.combinations["c"] = playerLots[2]


    def erasePlayerVote(self,player):
        for key in self.combinations.keys():
            if player in self.combinations[key]:
                self.combinations[key].remove(player);

    def getDoorFromCombi(self,combiNumber,player):
        if(self.GameIterations%2 != 0):
            if(combiNumber == 0):
                self.cyanLot.append(player)
                return Color.CYAN
            elif(combiNumber == 1):
                self.magentaLot.append(player)
                return Color.MAGENTA
            elif(combiNumber == 2):
                self.yellowLot.append(player)
                return Color.YELLOW
        else:
            if(combiNumber == 0):
                self.redLot.append(player)
                return Color.RED
            elif(combiNumber == 1):
                self.greenLot.append(player)
                return Color.GREEN
            elif(combiNumber == 2):
                self.blueLot.append(player)
                return Color.BLUE




    def setProposedColorCombo(self,combiNumber):
        if(self.GameIterations%2 != 0):
            if(combiNumber == "a"):
                self.ProposedColorCombo = "RedSolo|RedPair"
            elif(combiNumber == "b"):
                self.ProposedColorCombo = "RedSolo|BluePair"
            elif(combiNumber == "c"):
                self.ProposedColorCombo = "RedSolo|GreenPair"
        else:
            if(combiNumber == "a"):
                self.ProposedColorCombo = "CyanSolo|CyanPair"
            elif(combiNumber == "b"):
                self.ProposedColorCombo = "CyanSolo|YellowPair"
            elif(combiNumber == "c"):
                self.ProposedColorCombo = "CyanSolo|MagentaPair"

    def clearCombi(self):
        self.combinations = {"a": [[],[],[]], "b": [[],[],[]], "c": [[],[],[]]}  #apaga as combinaçoes possiveis de distribuiçao dos jogadores numa determinada ronda


    def calcVoting(self):

        preferenceDict = {}

        utilityArray = [0,0,0]

        voteArray = [0,0,0]

        leastSufferingArray = [0,0,0]

        combi = ["a","b","c"]


        for player in self.PlayerArray:
            
            preferenceArray = [0,0,0]

            for i in range(3):
                doorArray = findCombiWithPlayer(combi[i],player)

                if(player.type == Type.PAIR):
                    opponentName = doorArray[2].name
                    opponentState = player.privateState.getOpponentState(opponentName)
                    combiValue = opponentState.consValue + opponentState.consValuePrev + 4*opponentState.nAlly - 4*opponentState.nBetray + checkPromise(player.name,opponentName,2)
                    preferenceArray[i] = combiValue
                    utilityArray[i] += combiValue

                elif(player.type == Type.SOLO):
                    opponentName = doorArray[0].name
                    opponentState = player.privateState.getOpponentState(opponentName)
                    combiValue = opponentState.consValue + opponentState.consValuePrev + 4*opponentState.nAlly - 4*opponentState.nBetray + checkPromise(player.name,opponentName,2)

                    opponentName = doorArray[1].name
                    opponentState = player.privateState.getOpponentState(opponentName)
                    combiValue += opponentState.consValue + opponentState.consValuePrev + 4*opponentState.nAlly - 4*opponentState.nBetray + checkPromise(player.name,opponentName,2)

                    combiValue /= 2

                    preferenceArray[i] = combiValue
                    utilityArray[i] += combiValue

            preferenceDict[player.name] = preferenceArray

        for key in preferenceDict.keys():
            voteArray[preferenceDict[key].index(max(preferenceDict[key]))] += 1;
            leastSufferingArray.[preferenceDict[key].index(min(preferenceDict[key]))] += min(preferenceDict[key])

        maxVoteValue = max(voteArray)
        drawCheck = 0
        for v in range(len(voteArray)):
            if(voteArray[v] == maxVoteValue):
                drawCheck += 1

        if(drawCheck > 1):          #verificar se há empate de votos nas combinações
                                #vê utility
            maxUtilityValue = max(utilityArray)
            utilityCheck = 0
            for u in range(len(utilityArray)):
                if(utilityArray[u] == maxUtilityValue):
                    utilityCheck += 1

            if(utilityCheck > 1):
                maxLeastSufferingValue = max(leastSufferingArray)
                sufferingCheck = 0
                for s in range(len(leastSufferingArray)):
                    if(leastSufferingArray[s] == maxLeastSufferingValue):
                        sufferingCheck += 1

                if(sufferingCheck > 1):
                    return combi[0]             #if all criteria are tied, it simply returns the first combination
                
                else:
                    return combi[leastSufferingArray.index(max(leastSufferingArray))]

            else:
                return combi[utilityArray.index(max(utilityArray))]

        else:
            return combi[voteArray.index(max(voteArray))]
                    

    def computeVote(self,typecolor,capValue):                                   #CASO EM QUE ELES MORREM É COBERTO PELO GETPLAYERBYTYPECOLOR
        participatingPlayers = self.getPlayerByTypecolor(typecolor)
        if(len(participatingPlayers) == 2):       #aka, if it's a pair vote

            opponents = self.getPlayerByTypecolor(self.getOpponent(participatingPlayers[0]))

            if(len(opponents == 0)):
                self.AmbidexGameRound[typecolor] = Vote.ALLY
                return "ALLY"

            playerA = participatingPlayers[0]
            playerB = participatingPlayers[1]

            aToBState = playerA.privateState.getOpponentState(playerB.name)
            bToAState = playerB.privateState.getOpponentState(playerA.name)

            aToCState = playerA.privateState.getOpponentState(opponents[0].name)
            promiseToOpponent = self.checkPromise(opponents[0].name,playerA.name,2)
            initialOpinion1 = aToCState.consValue + aToCState.consValuePrev + 3*aToCState.nAlly - 3*aToCState.nBetray + promiseToOpponent

            bToCState = playerB.privateState.getOpponentState(opponents[0].name)
            promiseToOpponent = self.checkPromise(opponents[0].name,playerB.name,2)
            initialOpinion2 = bToCState.consValue + bToCState.consValuePrev + 3*bToCState.nAlly - 3*bToCState.nBetray + promiseToOpponent

            if(initialOpinion1 > playerA.privateState.decisionThreshold == initialOpinion2 > playerB.privateState.decisionThreshold):  #they both want to ally or both want to betray
                votingPlayer = random.randrange(2)    #they choose randomly between themselves, since there's no conflict
                if(votingPlayer == 0):
                    self.votingAuxNoPromises(initialOpinion1,initialOpinion2,capValue,playerA,playerB,1,-2,typecolor)


                elif(votingPlayer == 1):
                    self.votingAuxNoPromises(initialOpinion2,initialOpinion1,capValue,playerB,playerA,1,-2,typecolor)


            else:       #NEGOTIATION PART
                if(initialOpinion1 > playerA.privateState.decisionThreshold and initialOpinion2 < playerB.privateState.decisionThreshold):  #P1 ALLY, P2 BETRAY
                    player1InitialVote = "ALLY"
                    player2InitialVote = "BETRAY"
                    firstProposal = [playerA.name,playerB.name,"ALLY","ACTIVE"]
                    

                    if((bToAState.consValuePrev + bToAState.consValue + bToCState.consValuePrev + bToCState.consValue) > playerB.privateState.decisionThreshold):   #P1 propoe ao P2 que ele faça ally
                        return decideWithPressure(playerB,opponents[0],2*playerB.privateState.honorFactor,capValue,playerA,"ALLY",1,-2,firstProposal)       #the 2 represents the weight of the promise
                    
                    secondProposal = [playerB.name,playerA.name,"ALLY","ACTIVE"]
                    if((aToBState.consValuePrev + aToBState.consValue + aToCState.consValuePrev + aToCState.consValue) < playerA.privateState.decisionThreshold):           #P2 propoe ao P1 que ele faça betray
                        return decideWithPressure(playerA,opponents[0],-2*playerB.privateState.honorFactor,capValue,playerB,"BETRAY",1,-2,secondProposal)

                    else:
                        votingPlayer = self.chooseVotingPlayer(initialOpinion1,initialOpinion2,playerA,playerB,capValue)
                        if(votingPlayer == 0):
                            self.votingAuxNoPromises(initialOpinion1,initialOpinion2,capValue,playerA,playerB,1,-1,typecolor)

                        elif(votingPlayer == 1):
                            self.votingAuxNoPromises(initialOpinion2,initialOpinion1,capValue,playerB,playerA,1,-1,typecolor)



        elif(len(participatingPlayers) == 1):
            opponents = self.getPlayerByTypecolor(self.getOpponent(participatingPlayers[0]))
            currentProposal = 0
            if(len(opponents) == 0):
                self.AmbidexGameRound[typecolor] = Vote.ALLY
                return "ALLY"
            else:
                for opp in opponents:
                    opponentState = participatingPlayers[0].privateState.getOpponentState(opp.name)
                    promiseToOpponent = self.checkPromise(opp.name,participatingPlayers[0].name,2)
                    currentProposal += opponentState.consValue + opponentState.consValuePrev + 3*opponentState.nAlly - 3*opponentState.nBetray + promiseToOpponent
                currentProposal /= len(opponents)

                votingProbabilities = self.computeProbabilities(currentProposal,capValue,participatingPlayers[0].privateState.decisionThreshold)
                choiceGenerated = random.random()
                if(choiceGenerated < votingProbabilities[0]):
                    self.AmbidexGameRound[typecolor] = Vote.ALLY
                    return "ALLY"
                else:
                    self.AmbidexGameRound[typecolor] = Vote.BETRAY
                    return "BETRAY"
            


        elif(len(participatingPlayers) == 0):
            self.AmbidexGameRound[typecolor] = Vote.ALLY
            return "ALLY"
                   
           

    def chooseVotingPlayer(self,proposal1,proposal2,player1,player2):
        distTotal = abs(proposal1 - player1.privateState.decisionThreshold) + abs(proposal2 - player2.privateState.decisionThreshold)
        prob1 = proposal1/distTotal
        choiceGenerated = random.random()
        if(choiceGenerated < prob1):
            return 0
        else:
            return 1



    def votingAuxNoPromises(self,decidingProposal,inactiveProposal,capValue,decidingPlayer,inactivePlayer,bonus,penalty,typecolor):

            dToIState = decidingPlayer.privateState.getOpponentState(inactivePlayer.name)
            iToDState = inactivePlayer.privateState.getOpponentState(decidingPlayer.name)

            votingProbabilities = self.computeProbabilities(decidingProposal,capValue,decidingPlayer.privateState.decisionThreshold)
            choiceGenerated = random.random()
            if(choiceGenerated < votingProbabilities[0]):
                self.AmbidexGameRound[typecolor] = Vote.ALLY                #DEFINE O VOTO PARA A GAME INSTANCE
                #bonus/penalty de seguir a decision
                if(inactiveProposal > inactivePlayer.privateState.decisionThreshold):
                    iToDState.consValue += bonus*inactivePlayer.privateState.emotionalMultiplier
                    dToIState.consValuePrev += bonus
                else:
                    iToDState.consValue += penalty*inactivePlayer.privateState.emotionalMultiplier
                    dToIState.consValuePrev += penalty
                return "ALLY"
            else:
                self.AmbidexGameRound[typecolor] = Vote.BETRAY
                if(inactiveProposal > inactivePlayer.privateState.decisionThreshold):
                    iToDState.consValue += penalty*inactivePlayer.privateState.emotionalMultiplier
                    dToIState.consValuePrev += penalty
                else:
                    iToDState.consValue += bonus*inactivePlayer.privateState.emotionalMultiplier
                    dToIState.consValuePrev += bonus
                return "BETRAY"







    def decideWithPressure(self,player,opponent,negotiationWeight,capValue,partner,promisedToPartner,bonus,penalty,promise):
        opponentState = player.privateState.getOpponentState(opponent.name)
        promiseToOpponent = self.checkPromise(opponent.name,player.name,2)

        partnerToPlayerState = partner.privateState.getOpponentState(player.name)
        playerToPartnerState = player.privateState.getOpponentState(partner.name)


        proposalValue = opponentState.consValue + opponentState.consValuePrev + 3*opponentState.nAlly - 3*opponentState.nBetray + promiseToOpponent*player.privateState.honorFactor + negotiationWeight
        votingProbabilities = self.computeProbabilities(proposalValue,capValue,player.privateState.decisionThreshold)

        if(promisedToPartner == "ALLY"):
            choiceGenerated = random.random()
            if(choiceGenerated < votingProbabilities[0]):
                self.AmbidexGameRound[typecolor] = Vote.ALLY
                partnerToPlayerState.consValue += bonus*partner.privateState.emotionalMultiplier
                playerToPartnerState.consValuePrev += bonus
                player.privateState.promiseHistory.append(promise)
                partner.privateState.promiseHistory.append(promise)
                return "ALLY"
            else:
                self.AmbidexGameRound[typecolor] = Vote.BETRAY
                partnerToPlayerState.consValue += penalty*partner.privateState.emotionalMultiplier
                playerToPartnerState.consValuePrev += penalty
                return "BETRAY"



        elif(promisedToPartner == "BETRAY"):
            choiceGenerated = random.random()
            if(choiceGenerated < votingProbabilities[0]):
                self.AmbidexGameRound[typecolor] = Vote.ALLY
                partnerToPlayerState.consValue += penalty*partner.privateState.emotionalMultiplier
                playerToPartnerState.consValuePrev += penalty
                return "ALLY"
            else:
                self.AmbidexGameRound[typecolor] = Vote.BETRAY
                partnerToPlayerState.consValue += bonus*partner.privateState.emotionalMultiplier
                playerToPartnerState.consValuePrev += bonus
                player.privateState.promiseHistory.append(promise)
                partner.privateState.promiseHistory.append(promise)
                return "BETRAY"





    def findCombiWithPlayer(self,combiName,player):
        combi = self.combinations[combiName]
        for lot in combi:
            for i in range(len(lot)):
                if player.name == lot[i]:
                    return lot


    def checkPromise(self,receiver,proposer,promiseValue):
        currentValue = 0
        for promise in player.privateState.promiseHistory:
            if(promise[0] == proposer and promise[1] == receiver and promise[2] == "ALLY" and promise[3] == "ACTIVE"):
                return promiseValue
            #elif(promise[0] == opponentName and promise[1] == player.name and promise[2] == "ALLY" and promise[3] == "FAILED"):        possibilidade de fazer cenas com promessas n cumpridas
        return currentValue


    def getPromise(self,receiver,proposer, player):
        for promise in player.privateState.promiseHistory:
            if(promise[0] == proposer and promise[1] == receiver and promise[2] == "ALLY" and promise[3] == "ACTIVE"):
                return promise
        return "NULL"


    def computeProbabilities(self,proposalValue,capValue,decisionThreshold):
        finalArray = [0,0]
        linearProbAlly = (((proposalValue-decisionThreshold)+(capValue-decisionThreshold))/((capValue-decisionThreshold)*2))
        linearProbBetray = 1 - linearProbAlly
        if(linearProbAlly > linearProbBetray):
            finalArray[0] = math.sqrt(linearProbAlly)
            finalArray[1] = 1 - finalArray[0]
        elif(linearProbBetray > linearProbAlly):
            finalArray[1] = math.sqrt(linearProbBetray)
            finalArray[0] = 1 - finalArray[1]
        else:
            finalArray = [0.5,0.5]
        return finalArray



    def computeAmbidexGame(self):

        for player in self.PlayerArray:
            playerColorType = self.getPlayerColorType(player)
            opponentColorType = self.getOpponent(player)
            value = self.getAmbidexResult(playerColorType,opponentColorType)
            player.addPoints(value)
            self.updateOpponentValues(playerColorType,opponentColorType,player,self.getPlayerByTypecolor(opponentColorType))
            self.updateOutsiderValues(player)

        self.GameIterations += 1
        self.randomizeBracelets()
        self.AmbidexGameRound.clear()



    def updateOpponentValues(self,playerColorType,opponentColorType,player,opponents):
        playerVote = self.AmbidexGameRound[playerColorType]
        opponentVote = self.AmbidexGameRound[opponentColorType]

        for opp in opponents:
            opponentState = player.privateState.getOpponentState(opp.name)

            playerPromise = self.getPromise(opp,player,player)        
            opponentPromise = self.getPromise(player,opp,player)


            if(opponentVote == Vote.ALLY):
                if(opponentPromise != "NULL"):
                    opponentPromise[3] = "SUCCESS"
                    opponentState.consValue += 2*player.privateState.emotionalMultiplier        #bonus from holding up to his previous promise
                opponentState.consValue += 1*player.privateState.emotionalMultiplier
                opponentState.nAlly += 1

            elif(opponentVote == Vote.BETRAY):
                if(opponentPromise != "NULL"):
                    opponentPromise[3] = "FAILURE"
                    opponentState.consValue += -2*player.privateState.emotionalMultiplier        #penalty from not holding up to his previous promise
                opponentState.consValue += -1*player.privateState.emotionalMultiplier
                opponentState.nBetray += 1


            if(playerVote == Vote.ALLY):
                if(playerPromise != "NULL"):
                    playerPromise[3] = "SUCCESS"
                    opponentState.consValuePrev += 2
                opponentState.consValuePrev += 2

            elif(playerVote == Vote.BETRAY):
                if(playerPromise != "NULL"):
                    playerPromise[3] = "FAILURE"
                    opponentState.consValuePrev += -2
                opponentState.consValuePrev += -2


    def updateOutsiderValues(self,outsider):
        outsiderColorType = self.getPlayerColorType(outsider)
        outsiderOpponentColorType = self.getOpponent(outsider)


        outsiderVote = self.AmbidexGameRound[outsiderColorType]


        for player in self.PlayerArray:
            finalValue = 0
            playerColorType = self.getPlayerColorType(player)
            opponentColorType = self.getOpponent(player)
            playerState = outsider.privateState.getOpponentState(player.name)

            opponents = self.getPlayerByTypecolor(opponentColorType)
            playerVote = self.AmbidexGameRound[playerColorType]

            if(playerColorType != outsiderColorType and playerColorType != outsiderOpponentColorType):      
    
                #actualiza a opiniao do outsider em relaçao aos outros players

                if(playerVote == Vote.ALLY):        
                    if(len(opponents) > 0):
                        for opp in opponents:
                            opponentState = outsider.privateState.getOpponentState(opp.name)
                            if(opponentState.consValue >= 0 and playerState.consValue != 0):
                                finalValue += (opponentState.consValue/abs(playerState.consValue)) + 1
                            elif(opponentState.consValue < 0 and playerState.consValue != 0):
                                finalValue += (opponentState.consValue/abs(playerState.consValue)) - 1
                            elif(opponentState.consValue != 0 and playerState.consValue == 0):
                                finalValue += (opponentState.consValue/abs(opponentState.consValue))
                            elif(opponentState.consValue == 0 and playerState.consValue == 0):
                                finalValue += 1
                        finalValue /= len(opponents)

                elif(playerVote == Vote.BETRAY):
                    if(len(opponents) > 0):
                        for opp in opponents:
                            opponentState = outsider.privateState.getOpponentState(opp.name)
                            if(opponentState.consValue > 0):
                                finalValue += (abs(playerState.consValue)/(-1*opponentState.consValue)) - 1
                            elif(opponentState.consValue < 0):
                                finalValue += (abs(playerState.consValue)/(-1*opponentState.consValue)) + 1
                            elif(opponentState.consValue == 0):
                                finalValue += -1

                playerState.consValue += finalValue

                #actualiza a opiniao que o outsider acha que os outros têm dele, como outsiders

                if(outsiderVote == Vote.ALLY):
                    playerState.consValuePrev += 1

                elif(outsiderVote == Vote.BETRAY):
                    playerState.consValuePrev -= 1
        