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
            for opponent in player.privateState.opponentStateArray:
                opState_ = ET.SubElement(state_, "Opponent", name=opponent.opponentName)
                ET.SubElement(opState_,"ConsiderationValue").text = str(opponent.considerationValue)
                ET.SubElement(opState_,"ConsiderationValuePrev").text = str(opponent.considerationValuePrev)
                ET.SubElement(opState_,"AllyCounter").text = str(opponent.allyCounter)
                ET.SubElement(opState_,"BetrayCounter").text = str(opponent.betrayCounter)                   
        combiA = game.combinations["a"]
        combiB = game.combinations["b"]
        combiC = game.combinations["c"]
        combinations_ =ET.SubElement(round_,"Combinations")
        ET.SubElement(combinations_,"CombinationA")

        #HERE : put combinations in log

        chosenCombination = game.calcVoting()           #calculates which door is chosen for the round
        game.setPlayerDoors(chosenCombination)          #locks the players to the respective door according to the chosen combination

        if(game.GameIterations%2 != 0):
            for typecolor in ["RED PAIR","RED SOLO","GREEN PAIR","GREEN SOLO","BLUE PAIR","BLUE SOLO"]:
                voteString = game.computeVote(typecolor,20)              #20 is the maximum cap value for which Ally probability is 100%
        else:
            for typecolor in ["CYAN PAIR","CYAN SOLO","MAGENTA PAIR","MAGENTA SOLO","YELLOW PAIR","YELLOW SOLO"]:
                voteString = game.computeVote(typecolor,20)

        game.computeAmbidexGame()
        
        
        #at end game write to log:
        tree_ = ET.ElementTree(game_)
        tree.write("log.xml")
            
            



