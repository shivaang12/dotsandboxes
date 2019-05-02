#!/usr/bin/env python3

__author__ = "Nantha Kumar Sunder"
__version__ = "0.1.0"
__license__ = "MIT"

import numpy as np
import matplotlib.pyplot as plt
import random
import csv

##---------------------------------------------------
## class for AI
class ai:
    def __init__(self, game, grid_size, alpha, epsilon, gamma, maxEpsilon, minEpsilon, total_episodes):
        self.qTable = dict()
        self.game = game
        self.alpha = alpha
        self.epsilon = maxEpsilon
        self.grid_size = grid_size
        self.gamma = gamma
        self.maxEpsilon = maxEpsilon
        self.minEpsilon = minEpsilon
        self.episodeNum = total_episodes

    def write2csv(self):
        with open('../Results/qTable' + str(self.grid_size) + '.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['State', 'Value'])
            allStates = list(self.qTable.keys())
            allStates.sort()
            for state in allStates:
                writer.writerow([state, self.qTable[state]])

    def loadFromCsv(self):
        # reader = csv.reader(open('../Results/qTable' + str(self.grid_size) + '.csv', 'r'))
        reader = csv.reader(open('../Results/qTable' + str(self.grid_size-1) + '.csv', 'r'))
        for k, v in reader:
            if v == 'Value':
                # self.qTable[k] = v
                continue
            else:
                self.qTable[k] = float(v)

    def trainFromEpisode(self ):
        decayRate = (self.maxEpsilon - self.minEpsilon) / self.episodeNum
        for episode in range(self.episodeNum):
            self.epsilon = decayRate*self.epsilon
            # if (episode % 10000 == 0): print('Completed ' + str(episode) + ' episodes')
            self.learnFromEpisode()
        print("Training Done")

    def learnFromEpisode(self):
        NewGame = self.game(self.grid_size)
        _, move = self.getMove(NewGame)
        while move:
            move = self.trainAI(NewGame, move)

    def trainAI(self, game, move):
        boxTaken = game.makeMove(move, 0, 0)
        count = 0
        if game.winner == game.player:
            count = 1
        reward = self.giveReward(game, boxTaken +  count)
        cummulativeReward = reward
        nextReward = 0.0
        selectedMove = None
        if ( not game.isBoardFull() ):
            bestNextMove, selectedMove = self.getMove(game)
            nextReward = self.qTableValue(bestNextMove)
        currentQValue = self.qTableValue(move)
        cummulativeReward = reward - self.gamma*(nextReward)
        self.qTable[move] = currentQValue + self.alpha * (cummulativeReward - currentQValue)
        return selectedMove

    def getMoveVsHuman(self):
        posMoves = self.getQTableValues(self.possibleMoves(self.game))
        ## exploitation
        move = self.maxExploit(posMoves)
        self.game.makeMove( move,0,0 )

    def getMove(self, game):
        posMoves = self.getQTableValues(self.possibleMoves(game))
        ## exploitation
        move = self.maxExploit(posMoves)
        randomMove = move
        ## exploration
        if random.random() < self.epsilon:
            randomMove = random.choice(list(posMoves.keys()))
        return (move, randomMove)

    def possibleMoves(self, game):
        posStates = list()
        for i in range(0, int(((2*self.grid_size + 1)**2-1)/2)):
            if game.states[i] == ' ':
                tempBoard = game.states[:i] + str(1) + game.states[i+1:]
                posStates.append(tempBoard)
        return posStates

    def qTableValue(self, state):
    	return self.qTable.get(state, 0.0)

    def getQTableValues(self, posStatesDict):
    	return dict((state, self.qTableValue(state)) for state in posStatesDict)

    def maxExploit(self, posStatesDict):
        maxValue = max(posStatesDict.values())
        chosenState = random.choice([state for state,\
         val in posStatesDict.items() if val == maxValue])
        return chosenState

    def minExploit(self, posStatesDict):
        minValue = min(posStatesDict.values())
        chosenState = random.choice([state for state,\
         val in posStatesDict.items() if val == minValue])
        return chosenState

    def giveReward(self, game, mode):
        if mode==1:
            return 1.0
        elif mode == 2:
            return 5.0
        else:
            return 0.0

    def roundQvalues(self):
        for k in self.qTable.keys():
            self.qTable[k] = round(self.qTable[k], 1)
