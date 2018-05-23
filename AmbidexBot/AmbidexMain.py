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
    if(game.createGame(game, "main", "object?")): #o que e o playerobject?
        for i in range(0,9):
            machine = game.addMachine(game)
            playerArray.append(machine)
    game.startGame(game)
    while(game.checkInProgress):
        #bots recebem as combinacoes e teem de votar numa. HOW? criar array de consideracoes para cada player
        # -> fazer funcao que calcula as combinacoes possiveis e a "utilidade" para cada player para que estes votem
        # -> fazer funcao que receba a votacao dos players e devolva a combinacao possivel ou recomece a votacao em caso de empates

    
