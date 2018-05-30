from GameInstance import GameInstance
from Player import Player
import Token
from Species import Species
from Type import Type
from Vote import Vote
from Status import Status

def main():
    game = GameInstance()
    playerArray = game.createGame()

    game.startGame()

    while(not game.doorNineOpen):
        #bots recebem as combinacoes e teem de votar numa. HOW? criar array de consideracoes para cada player
        game.clearCombi()
        for player in playerArray:
            game.setPlayerCombi(player)
        combiA = game.combinations["a"]
        combiB = game.combinations["b"]
        combiC = game.combinations["c"]
        #HERE : put combinations in log
        #calcular a utilidade para cada player de acordo com os consideration values e retornar combinacao escolhida "por todos"
        #game.setPlayerDoors(combi) // combi returnada na linha anterior
        game.LockAmbidex=True
        game.AmbidexInProgress=True
        #negotiation between pairs, solo vote is linear 
            
            
            



