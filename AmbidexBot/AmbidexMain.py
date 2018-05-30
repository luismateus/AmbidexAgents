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
    game.startGame()

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
        #calcular a utilidade para cada player de acordo com os consideration values e retornar combinacao escolhida "por todos"
        #game.setPlayerDoors(combi) // combi returnada na linha anterior
        game.LockAmbidex=True
        game.AmbidexInProgress=True
        #negotiation between pairs, solo vote is linear 
        
        
        
        #at end game write to log:
        tree_ = ET.ElementTree(game_)
        tree.write("log.xml")
            
            



