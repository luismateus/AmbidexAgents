import xml.etree.ElementTree
import numpy as np
import pylab as plt
import matplotlib.lines as mlines

root = xml.etree.ElementTree.parse('log_2018_06_01_160635.xml').getroot()


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
    

    bpAllied = []
    bpBetrayed = []
    
    
    name = "Haynes"
    
    for i in range(len(games)):
        playerTypeColor = games[i].find("Round/Players/Player[@name=\'" + name + "\']/Typecolor").text
        firstVote = games[i].find("Round/Vote/Type[@name=\'" + str(playerTypeColor) + "\']").text
        finalPoints = games[i].find("FinalState/Player[@name=\'" + name + "\']/Points").text
        if(firstVote == "ALLY"):
            bpAllied.append(int(finalPoints))
        elif(firstVote == "BETRAY"):
            bpBetrayed.append(int(finalPoints))
            
            
            
    fig = plt.figure()
    #plt.axis([0, len(games), -3, 12])
    
    #plt.title('Final BP of ' + name + ' given 1st AB decision')
    plt.xlabel('Final BP')
    plt.ylabel('Number of Games')
    #plt.plot(gamesAllied, bpAllied, 'bo', gamesBetrayed, bpBetrayed, 'rx')
    #plt.axhline(-0.5, color='red')
    #plt.axhline(8.5, color='green')
    
    
    #blue_marker = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=8, label='Round 1 Ally')
    #red_marker = mlines.Line2D([], [], color='red', marker='x', linestyle='None', markersize=8, label='Round 1 Betray')
        
    #plt.legend(handles=[blue_marker,red_marker])
    
    
    
    n, bins, patches = plt.hist([bpAllied, bpBetrayed],density=True, histtype='bar', stacked=True)
    plt.xticks(range(min(min(bpAllied),min(bpBetrayed)),max(max(bpAllied),max(bpBetrayed))))
    
    plt.show()
    







scatterBPbyRound1()










