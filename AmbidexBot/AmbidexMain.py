from GameInstance import GameInstance
from Player import Player
import Token
from Species import Species
from Type import Type
from Vote import Vote
from Status import Status

def main():
    playerArray = []
    game = GameInstance()
    if(game.createGame("main", "object?")): #o que e o playerobject?
        for i in range(0,9):
            machine = game.addMachine()
            playerArray.append(machine)
    game.startGame()
    while(game.checkInProgress):
        #bots recebem as combinacoes e teem de votar numa. HOW? criar array de consideracoes para cada player
        if(not(game.ActivePolling or game.LockAmbidex)): # time for votation, falta verificacao para ver se os players nao estao dentro das portas
            game.clearCombi()
            for player in playerArray:
                game.setPlayerCombi(player)
            game.ActivePolling = True
            combiA = game.combinations["a"]
            combiB = game.combinations["b"]
            combiC = game.combinations["c"]            
            #HERE : put combinations in log
            #calcular a utilidade para cada player de acordo com os consideration values e retornar combinacao escolhida "por todos"
            #game.setPlayerDoors(combi) // combi returnada na linha anterior
            game.ActivePolling=False
            game.LockAmbidex=True
        if(game.LockAmbidex and (not game.AmbidexInProgress)):
            game.AmbidexInProgress=True
            #negotiation between pairs, solo vote is linear 
            
            
            



