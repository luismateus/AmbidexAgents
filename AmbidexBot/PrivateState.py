from OpponentState import OpponentState

class PrivateState:

    def __init__(self):
        self.opponentStateArray = [OpponentState(),OpponentState(),OpponentState(),OpponentState(),OpponentState(),OpponentState(),OpponentState(),OpponentState()]
        self.promiseHistory = []           #array which stores the promises made as pairs
        self.decisionThreshold = 0          #mid-value on which the player has 50% chance to ally or betray
        self.emotionalMultiplier = 1
        self.honorFactor = 1                #multiplies by promise weight

    def getOpponentState(self,name):
        for i in range(0,len(self.opponentStateArray)):
            if(self.opponentStateArray[i].opponentName == name):
                return self.opponentStateArray[i]

    
        