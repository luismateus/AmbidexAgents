import os

from Player import Player
from Color import Color
import random
from Type import Type
from Species import Species
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
        self.preferenceDict = {}
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
            self.PlayerArray.append(Player(list.pop()))
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



    def calculateCombinations(self,soloPlayer,pairPlayer):
        if((soloPlayer.getColor() == Color.RED and pairPlayer.getColor() == Color.RED) or (soloPlayer.getColor() == Color.GREEN and pairPlayer.getColor() == Color.GREEN) or (soloPlayer.getColor() == Color.BLUE and pairPlayer.getColor() == Color.BLUE)):
            colorCombo = "RedSolo|RedPair"
        if((soloPlayer.getColor() == Color.RED and pairPlayer.getColor() == Color.GREEN) or (soloPlayer.getColor() == Color.GREEN and pairPlayer.getColor() == Color.BLUE) or (soloPlayer.getColor() == Color.BLUE and pairPlayer.getColor() == Color.RED)):
            colorCombo = "RedSolo|GreenPair"
        if((soloPlayer.getColor() == Color.RED and pairPlayer.getColor() == Color.BLUE) or (soloPlayer.getColor() == Color.GREEN and pairPlayer.getColor() == Color.RED) or (soloPlayer.getColor() == Color.BLUE and pairPlayer.getColor() == Color.GREEN)):
            colorCombo = "RedSolo|BluePair"
        if((soloPlayer.getColor() == Color.CYAN and pairPlayer.getColor() == Color.CYAN) or (soloPlayer.getColor() == Color.YELLOW and pairPlayer.getColor() == Color.YELLOW) or (soloPlayer.getColor() == Color.MAGENTA and pairPlayer.getColor() == Color.MAGENTA)):
            colorCombo = "CyanSolo|CyanPair"
        if((soloPlayer.getColor() == Color.CYAN and pairPlayer.getColor() == Color.YELLOW) or (soloPlayer.getColor() == Color.YELLOW and pairPlayer.getColor() == Color.MAGENTA) or (soloPlayer.getColor() == Color.MAGENTA and pairPlayer.getColor() == Color.CYAN)):
            colorCombo = "CyanSolo|YellowPair"
        if((soloPlayer.getColor() == Color.CYAN and pairPlayer.getColor() == Color.MAGENTA) or (soloPlayer.getColor() == Color.YELLOW and pairPlayer.getColor() == Color.CYAN) or (soloPlayer.getColor() == Color.MAGENTA and pairPlayer.getColor() == Color.YELLOW)):
            colorCombo = "CyanSolo|MagentaPair"
        self.ProposedColorCombo = colorCombo
        return self.getTempCombinations()






    def getOpponent(self,player):
        colortype = self.getPlayerColorType(player)     #aka "RED SOLO" or etc
        playerdoor = player.getDoor()                   #aka Color.CYAN
        for key in self.ColorSets[self.ProposedColorCombo].keys():
            if(key != colortype and self.ColorSets[self.ProposedColorCombo][key] == playerdoor):
                return key

    def getTempCombinations(self):
        message = ""
        self.cyanLot.clear()
        self.yellowLot.clear()
        self.magentaLot.clear()
        self.redLot.clear()
        self.greenLot.clear()
        self.blueLot.clear()
        for player in self.PlayerArray:
            bracelet = player.getColor().name + " " + player.getType().name
            playerDoor = self.ColorSets[self.ProposedColorCombo][bracelet]
            if(playerDoor == Color.CYAN):
                self.cyanLot.append(player)
            if(playerDoor == Color.YELLOW):
                self.yellowLot.append(player)
            if(playerDoor == Color.MAGENTA):
                self.magentaLot.append(player)
            if(playerDoor == Color.RED):
                self.redLot.append(player)
            if(playerDoor == Color.GREEN):
                self.greenLot.append(player)
            if(playerDoor == Color.BLUE):
                self.blueLot.append(player)
        if(len(self.cyanLot) != 0):
            message += self.cyanLot[0].getName() + ", " + self.cyanLot[1].getName() + " and " + self.cyanLot[2].getName() + " will go through the Cyan Door.\n"
            message += self.yellowLot[0].getName() + ", " + self.yellowLot[1].getName() + " and " + self.yellowLot[2].getName() + " will go through the Yellow Door.\n"
            message += self.magentaLot[0].getName() + ", " + self.magentaLot[1].getName() + " and " + self.magentaLot[2].getName() + " will go through the Magenta Door.\n"
        if(len(self.redLot) != 0):
            message += self.redLot[0].getName() + ", " + self.redLot[1].getName() + " and " + self.redLot[2].getName() + " will go through the Red Door.\n"
            message += self.greenLot[0].getName() + ", " + self.greenLot[1].getName() + " and " + self.greenLot[2].getName() + " will go through the Green Door.\n"
            message += self.blueLot[0].getName() + ", " + self.blueLot[1].getName() + " and " + self.blueLot[2].getName() + " will go through the Blue Door.\n"
        return message

    def generateRoundVote(self,player):
        personality = player.getPersonality()

        if(personality == "Cooperator"):
            return Vote.ALLY

        elif(personality == "Undecided"):
            if(random.random() > 0.5):
                return Vote.ALLY
            else:
                return Vote.BETRAY

        elif(personality == "Killer"):
            opponentColor = self.getOpponent(player).split()[0]
            opponentType = self.getOpponent(player).split()[1]
            for opponent in self.PlayerArray:
                if(opponent.getColor() == opponentColor and opponent.getType() == opponentType):
                    if (opponent.getPoints() <= 2):
                        return Vote.BETRAY
            return Vote.ALLY

        elif(personality == "Cockblocker"):
            opponentColor = self.getOpponent(player).split()[0]
            opponentType = self.getOpponent(player).split()[1]
            for opponent in self.PlayerArray:
                if(opponent.getColor() == opponentColor and opponent.getType() == opponentType):
                    if (opponent.getPoints() >= 6):
                        if(random.random() < 0.7):
                            return Vote.BETRAY
            return Vote.ALLY

        elif(personality == "Asshole"):
            return Vote.BETRAY

        elif(personality == "Paranoid"):
            if(self.GameIterations == 1 or player.getPoints() <= 2):
                return Vote.BETRAY
            else:
                 if(random.random() > 0.6):
                     return Vote.ALLY
                 else:
                     return Vote.BETRAY



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
            if(self.getPlayerColorType(player) == typecolorString):
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

        self.preferenceDict = {}

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
                    combiValue = opponentState.consValue + opponentState.consValuePrev + 4*opponentState.nAlly - 4*opponentState.nBetray + checkPromise(player,opponentName)
                    preferenceArray[i] = combiValue
                    utilityArray[i] += combiValue

                elif(player.type == Type.SOLO):
                    opponentName = doorArray[0].name
                    opponentState = player.privateState.getOpponentState(opponentName)
                    combiValue = opponentState.consValue + opponentState.consValuePrev + 4*opponentState.nAlly - 4*opponentState.nBetray + checkPromise(player,opponentName)

                    opponentName = doorArray[1].name
                    opponentState = player.privateState.getOpponentState(opponentName)
                    combiValue += opponentState.consValue + opponentState.consValuePrev + 4*opponentState.nAlly - 4*opponentState.nBetray + checkPromise(player,opponentName)

                    combiValue /= 2

                    preferenceArray[i] = combiValue
                    utilityArray[i] += combiValue

            self.preferenceDict[player.name] = preferenceArray

        for key in self.preferenceDict.keys():
            voteArray[self.preferenceDict[key].index(max(self.preferenceDict[key]))] += 1;
            leastSufferingArray.[self.preferenceDict[key].index(min(self.preferenceDict[key]))] += min(self.preferenceDict[key])

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
                    
                    
                    




    def findCombiWithPlayer(self,combiName,player):
        combi = self.combinations[combiName]
        for lot in combi:
            for i in range(len(lot)):
                if player.name == lot[i]:
                    return lot


    def checkPromise(self,player,opponentName):
        for promise in player.privateState.promiseHistory:
            if(promise[0] == opponentName and promise[1] == player.name and promise[2] == "ALLY"):
                return 2
            
            

    def willingToLeave(self, player1):
        goodGuys=0
        badGuys=0
        for player in self.PlayerArray:
            if(not player.getName() == player1.getName()):
                opponentState = player1.privateState.getOpponetState(player.getName())
                if((opponentState.consValue + opponentState.consValuePrev >= 7) and player.getPoints()>=5 and player.getPoints()<9):
                    goodGuys+=1
                elif((opponentState.consValue + opponentState.consValuePrev < -1) and player.getPoints()<9):
                    badGuys+=1
        if(goodGuys>badGuys):
            return False
        else:
            return True
                    
                
                
        