import xml.etree.ElementTree
import numpy as np
import pylab as plt
import matplotlib.lines as mlines
import datetime
import time

#root = xml.etree.ElementTree.parse('log_2018_06_01_160635.xml').getroot()
#root = xml.etree.ElementTree.parse('log_2018_06_01_193345.xml').getroot()

#root = xml.etree.ElementTree.parse('log_2018_06_01_195825.xml').getroot()


#root = xml.etree.ElementTree.parse('log_2018_06_01_213006.xml').getroot()

#root = xml.etree.ElementTree.parse('log_2018_06_01_222919.xml').getroot()


#root = xml.etree.ElementTree.parse('log_2018_06_01_232637.xml').getroot()


root = xml.etree.ElementTree.parse('output.xml').getroot()


def scatterBPbyRound1():
    games = root.findall("./Game")
    
    gamesAllied = []
    gamesBetrayed = []
    
    bpAllied = []
    bpBetrayed = []
    
    
    name = "Haynes"
    
    for i in range(len(games)):
        playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
        firstVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']").text
        finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
        if(firstVote == "ALLY"):
            gamesAllied.append(i+1)
            bpAllied.append(int(finalPoints))
        elif(firstVote == "BETRAY"):
            gamesBetrayed.append(i+1)
            bpBetrayed.append(int(finalPoints))
            
            
    plt.axis([0, len(games), -3, 12])
    
    plt.title('Final BP of ' + name + ' given 1st AB decision')
    plt.xlabel('Game Instance')
    plt.ylabel('Final BP')
    plt.plot(gamesAllied, bpAllied, 'bo', gamesBetrayed, bpBetrayed, 'rx')
    plt.axhline(-0.5, color='red')
    plt.axhline(8.5, color='green')
    
    
    blue_marker = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=8, label='Round 1 Ally')
    red_marker = mlines.Line2D([], [], color='red', marker='x', linestyle='None', markersize=8, label='Round 1 Betray')
        
    plt.legend(handles=[blue_marker,red_marker])
    
    
    plt.show()
    
    
    
    
def frequencyHistBPbyRound1():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    bpAllied = {}
    bpBetrayed = {}

    for j in range(-3,14):
        bpAllied[str(j)] = 0
        bpBetrayed[str(j)] = 0
    
    
    
    name = "Haynes"
    
    for i in range(len(games)):
        playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
        firstVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']").text
        finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
        if(firstVote == "ALLY"):
            bpAllied[finalPoints] += 1
        elif(firstVote == "BETRAY"):
            bpBetrayed[finalPoints] += 1

    for j in range(-3,14):
        line = ""
        line += str(j) + "	" + str(bpAllied[str(j)]) + "	" + str(bpBetrayed[str(j)]) + "\n"
        text_file.write(line)
                
    text_file.close()
    
    
    
    
    
def playersWinningFrequency():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    playerDict = {}
    
    #for name in ["Alice","Bob","Carolyn","Dexter","Emily","Frank","Gwen","Haynes","Igor"]:
    for name in ["Lana","Ignis","Flora","Percy","Iris","Louie","Carter","Douglas","Preston"]:
        playerDict[name] = 0
        
    for game in games:
        winners = game.find("Winners").text[:-2]
        winnerArray = winners.split("; ")
        for winner in winnerArray:
            playerDict[winner] += 1
        
    for pairkey in sorted(playerDict.items(), key=lambda kv: kv[1], reverse=True):
        line = ""
        line += pairkey[0] + "	" + str(pairkey[1]) + "\n"
        text_file.write(line)
        print("Total WinRatio for " + pairkey[0] + ": " + format(pairkey[1]/len(games), '.3f'))
                
    text_file.close()
    
    
    

    
    
def allPlayersFrequencyHistBPbyRound1():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    bpAllied = {}
    bpBetrayed = {}

    for j in range(-20,30):
        bpAllied[str(j)] = 0
        bpBetrayed[str(j)] = 0
    
    
    for name in ["Alice","Bob","Carolyn","Dexter","Emily","Frank","Gwen","Haynes","Igor"]:
        for i in range(len(games)):
            playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
            firstVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']").text
            finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
            if(firstVote == "ALLY"):
                bpAllied[finalPoints] += 1
            elif(firstVote == "BETRAY"):
                bpBetrayed[finalPoints] += 1

    for j in range(-20,30):
        line = ""
        line += str(j) + "	" + str(bpAllied[str(j)]) + "	" + str(bpBetrayed[str(j)]) + "\n"
        text_file.write(line)
                
    text_file.close()            
        
    
    

    
    
def basedOnOpponentFrequencyHistBPbyRound1():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    bpAllied = {}
    bpBetrayed = {}

    for j in range(-20,30):
        bpAllied[str(j)] = 0
        bpBetrayed[str(j)] = 0
    
    
    
    
    for name in ["Alice","Bob","Carolyn","Dexter","Emily","Frank","Gwen","Haynes","Igor"]:
        for i in range(len(games)):
            playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
            firstOpponentVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']/Opponent").text
            finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
            if(firstOpponentVote == "ALLY"):
                bpAllied[finalPoints] += 1
            elif(firstOpponentVote == "BETRAY"):
                bpBetrayed[finalPoints] += 1

    for j in range(-20,30):
        line = ""
        line += str(j) + "	" + str(bpAllied[str(j)]) + "	" + str(bpBetrayed[str(j)]) + "\n"
        text_file.write(line)
                
    text_file.close()            
    
    
    
    

def winnerDecisionAnalysis():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    winnerFreq = {}
    allyDict = {}
    betrayDict = {}
    
    for i in range(9):
        allyDict[str(i+1)] = 0
        betrayDict[str(i+1)] = 0
        winnerFreq[str(i+1)] = 0
    
    
    for game in games:
        rounds = game.findall("Round")
        winners = game.find("Winners").text[:-2]
        winnerArray = winners.split("; ")
        for winner in winnerArray:
            winnerFreq[str(len(winnerArray))] += 1
            for round in rounds:
                playerTypeColor = round.find("Players/Player[@name=\'" + winner + "\']/Typecolor").text
                firstVote = round.find("Vote/Type[@name=\'" + str(playerTypeColor) + "\']").text
                if(firstVote == "ALLY"):
                    allyDict[str(len(winnerArray))] += 1
                elif(firstVote == "BETRAY"):
                    betrayDict[str(len(winnerArray))] += 1
                
        
    
        
    for key in winnerFreq.keys():
        line = ""
        if(winnerFreq[key]  == 0):
            line += key + "	" + str(0) + "	" + str(0) + "\n"
        else:
            line += key + "	" + format(allyDict[key]/winnerFreq[key], '.3f') + "	" + format(betrayDict[key]/winnerFreq[key], '.3f') + "\n"
        text_file.write(line)
                
    text_file.close()
    
    
    


    
def round1DecisionBPComparison():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    bpAllied = {}
    bpBetrayed = {}

    allyGames=0
    allyWins=0
    
    betrayGames=0
    betrayWins=0
    
    
    
    
    for j in range(-10,20):
        bpAllied[str(j)] = 0
        bpBetrayed[str(j)] = 0
    
    
    
    name = "Lana"
    
    for i in range(len(games)):
        playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
        firstVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']").text
        finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
        if(firstVote == "ALLY"):
            bpAllied[finalPoints] += 1
            allyGames += 1
        elif(firstVote == "BETRAY"):
            bpBetrayed[finalPoints] += 1
            betrayGames += 1
            
    for j in range(-10,20):
        line = ""
        line += str(j) + "	" + str(bpAllied[str(j)]) + "	" + str(bpBetrayed[str(j)]) + "\n"
        text_file.write(line)
        
        if(j >= 9):
            allyWins += bpAllied[str(j)]
            betrayWins += bpBetrayed[str(j)]
            
    print("Ally Ratio: " + str(allyGames) + "/" + str(len(games)) + ", " + str(allyGames/len(games)))
    print("Ally Wins: " + str(allyWins) + "/" + str(len(games)))
    print("Ally WinRatio in Total of Games: " + str(allyWins/len(games)))
    print("Ally WinRatio in Allied Games Only: " + str(allyWins/allyGames))
    print("Ally WinRatio in Total of Wins: " + str(allyWins/(allyWins+betrayWins)))
    
    print("Betray Ratio: " + str(betrayGames) + "/" + str(len(games)) + ", " + str(betrayGames/len(games)))
    print("Betray Wins: " + str(betrayWins) + "/" + str(len(games)))
    print("Betray WinRatio in Total of Games: " + str(betrayWins/len(games)))
    print("Betray WinRatio in Betrayed Games Only: " + str(betrayWins/betrayGames))
    print("Betray WinRatio in Total of Wins: " + str(betrayWins/(allyWins+betrayWins)))
    
    print("Total WinRatio: " + str((allyWins + betrayWins)/len(games)))
    
    
    
    text_file.close()
    
    
def round1OpponentDecisionBPComparison():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    bpAllied = {}
    bpBetrayed = {}

    for j in range(-20,30):
        bpAllied[str(j)] = 0
        bpBetrayed[str(j)] = 0
    
    
    name = "Bob"
    
    for i in range(len(games)):
        playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
        firstOpponentVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']/Opponent").text
        finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
        if(firstOpponentVote == "ALLY"):
            bpAllied[finalPoints] += 1
        elif(firstOpponentVote == "BETRAY"):
            bpBetrayed[finalPoints] += 1

    for j in range(-20,30):
        line = ""
        line += str(j) + "	" + str(bpAllied[str(j)]) + "	" + str(bpBetrayed[str(j)]) + "\n"
        text_file.write(line)
                
    text_file.close()            
    
  

def singleWinnerNumberEscapeesAnalysis():

    games = root.findall("./Game")
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S')
    text_file = open("output" + st + ".txt", "w")

    
    winnerFreq = {}
    allyDict = {}
    betrayDict = {}
    
    for i in range(9):
        allyDict[str(i+1)] = 0
        betrayDict[str(i+1)] = 0
        winnerFreq[str(i+1)] = 0
    
    name = "Bob"
    flagAccess = False
    
    for game in games:
        rounds = game.findall("Round")
        winners = game.find("Winners").text[:-2]
        winnerArray = winners.split("; ")
        if(name in winnerArray):
            winnerFreq[str(len(winnerArray))] += 1
                
        
    
        
    for key in winnerFreq.keys():
        line = ""
        if(winnerFreq[key]  == 0):
            line += key + "	" + str(0) + "	" + "\n"
        else:
            line += key + "	" + str(winnerFreq[key]) + "\n"
        text_file.write(line)
                
    text_file.close()
    
    
playersWinningFrequency()

#allPlayersFrequencyHistBPbyRound1()

#basedOnOpponentFrequencyHistBPbyRound1()


#winnerDecisionAnalysis()


#round1DecisionBPComparison()

#round1OpponentDecisionBPComparison()


#winnerDecisionAnalysis()

#singleWinnerNumberEscapeesAnalysis()





