from GameInstance import GameInstance
from Player import Player
import Token
from Species import Species
from Type import Type
from Vote import Vote
from Status import Status
import xml.etree.cElementTree as ET

def main():
    game = GameInstance()
    playerArray = game.createGame()
    game_ = ET.Element("Game")
    game.startGame()        #randomizes the bracelets

    while(not game.doorNineOpen):
        #bots recebem as combinacoes e teem de votar numa. HOW? criar array de consideracoes para cada player
        game.clearCombi()
        round_ = ET.SubElement(_game, "Round")
        players_ = ET.SubElement(round_, "Players")
        for player in playerArray:
            game.setPlayerCombi(player)
            
            player_ = ET.SubElement(players_, "Player", name= player.getName())
            ET.SubElement(player_, "Points").text = str(player.getPoints()) 
            ET.SubElement(player_, "Type").text = str(player.getType())
            state_ = ET.SubElement(player_, "State") # definir subStates
            promises_=ET.SubElement(state_,"PromiseHistory")
            for promise in player.privateState.promiseHistory:
                ET.SubElement(promises_,"Promise").text = promise[1] +" "+ promise[2] +" to "+ promise[0] + ". Status: " + promise[3]
            ET.SubElement(promises_,"DecisionThreshold").text = str(player.privateState.decisionThreshold)
            ET.SubElement(promises_,"EmotionalMultiplier").text = str(player.privateState.emotionalMultiplier)
            ET.SubElement(promises_,"HonorFactor").text = str(player.privateState.honorFactor)
            for opponent in player.privateState.opponentStateArray:
                opState_ = ET.SubElement(state_, "Opponent", name=opponent.opponentName)
                ET.SubElement(opState_,"ConsiderationValue").text = str(opponent.consValue)
                ET.SubElement(opState_,"ConsiderationValuePrev").text = str(opponent.consValuePrev)
                ET.SubElement(opState_,"AllyCounter").text = str(opponent.allyCounter)
                ET.SubElement(opState_,"BetrayCounter").text = str(opponent.betrayCounter)                   
        combiA = game.combinations["a"]
        combiB = game.combinations["b"]
        combiC = game.combinations["c"]
        combinationsL_ = ET.SubElement(round_,"CombinationLots")
        combA_ = ET.SubElement(combinationsL_,"CombinationA")
        for i in range(0,3):
            lot_ = ET.SubElement(combA_,"Lot"+str(i+1))
            ET.SubElement(lot_,combiA[i][0].getName())
            ET.SubElement(lot_,combiA[i][1].getName())
            ET.SubElement(lot_,combiA[i][2].getName())
        combB_ = ET.SubElement(combinationsL_,"CombinationB")
        for i in range(0,3):
            lot_ = ET.SubElement(combB_,"Lot"+str(i+1))
            ET.SubElement(lot_,combiB[i][0].getName())
            ET.SubElement(lot_,combiB[i][1].getName())
            ET.SubElement(lot_,combiB[i][2].getName())
        combC_ = ET.SubElement(combinationsL_,"CombinationC")
        for i in range(0,3):
            lot_ = ET.SubElement(combC_,"Lot"+str(i+1))
            ET.SubElement(lot_,combiC[i][0].getName())
            ET.SubElement(lot_,combiC[i][1].getName())
            ET.SubElement(lot_,combiC[i][2].getName())
        combinations_ = ET.SubElement(round_,"Combinations")
        for player in playerArray:
            player_ = ET.SubElement(combinations_,player.getName())
            preferenceArray = game.preferenceDict[player.getName()]
            ET.SubElement(player_,"A").text =  str(preferenceArray[0])
            ET.SubElement(player_,"B").text =  str(preferenceArray[1])
            ET.SubElement(player_,"C").text =  str(preferenceArray[2])
             
        chosenCombination = game.calcVoting()           #calculates which door is chosen for the round
        chosenComb_ = ET.SubElement(round_, "ChosenCombination").text = chosenCombination
        game.setPlayerDoors(chosenCombination)          #locks the players to the respective door according to the chosen combination
        vote_ = ET.SubElement(round_, "Vote")
        voteDict = {}
        for typecolor in ["RED PAIR","RED SOLO","GREEN PAIR","GREEN SOLO","BLUE PAIR","BLUE SOLO"]:
            voteString = game.computeVote(typecolor,20)              #20 is the maximum cap value for which Ally probability is 100%
            voteDict[typecolor]=voteString
        for typecolor in ["RED PAIR","RED SOLO","GREEN PAIR","GREEN SOLO","BLUE PAIR","BLUE SOLO"]:
            type_= ET.SubElement(vote_,"Type", name =typecolor).text = voteDict[typecolor]
            arrayType = game.getPlayerByTypecolor(typecolor)
            if(len(arrayType)>0):
                p1 = arrayType[0]
                opponent = game.getOpponent(p1)
                ET.SubElement(type_,"Opponent", name=opponent.getColor()).text = voteDict[opponent.getColor()]
        
            
        

        #score
        
        #at end game write to log:
        tree_ = ET.ElementTree(game_)
        tree.write("log.xml")
            
            



