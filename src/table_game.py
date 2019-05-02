#!/usr/bin/env python3

__author__ = "Nantha Kumar Sunder"
__version__ = "0.1.0"
__license__ = "MIT"

import numpy as np
import matplotlib.pyplot as plt
import random
from q_table import ai

class dotsnboxes:
    def __init__(self, grid_size):
        self.board = np.zeros((2*grid_size + 1, 2*grid_size + 1))
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[0]):
                if j % 2 == 0 and i % 2 == 0:
                    self.board[i][j] = 1
        self.player = 1
        self.states = ' ' * int(((2*grid_size + 1)**2-1)/2)

    def drawBoard(self):
        board = self.board.copy()
        print('\n-------------Board--------------\n')

        for i in range(board.shape[0]):
            str = '        '
            for j in range(board.shape[0]):
                if j % 2 == 0 and i % 2 == 0:
                    str = str + ' * '
                elif j % 2 != 0 and i % 2 !=0:
                    if board[i][j] == 0:
                        str = str + '   '
                    elif board[i][j] == 1:
                        str = str + ' A '
                    elif board[i][j] == 2:
                        str = str + ' B '
                elif i % 2 == 0:
                    if board[i][j] == 0:
                        str = str + '   '
                    else:
                        str = str + '---'
                else:
                    if board[i][j] == 0:
                        str = str + '   '
                    else:
                        str = str + ' | '
            print(str)
        print('\n--------------------------------\n')

    def availMove(self):
        posMove = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if i % 2 == 0 and j % 2 != 0:
                    if self.board[i][j] == 0:
                        posMove.append([i,j])
                    else:
                        continue
                elif i % 2 != 0 and j % 2 == 0:
                    if self.board[i][j] == 0:
                        posMove.append([i,j])
                    else:
                        continue
                else:
                    continue
        return posMove

    def updateState(self, row,col):
        # print('Update states')
        size = self.board.shape[0]
        id = int((row*size + col-1)/2)
        # print('id:',id)
        strList = list(self.states)
        # print(strList)
        strList[id] = '1'
        self.states = ''.join(strList)


    def makeMove(self,move,row,col):
        # move = list(move)
        # print('Inside make move')
        id = 0
        if move: # if move is not empty
            for id in range(len(move)):
                # id = id + 1
                if move[id] != self.states[id]:
                    break

            row = int((2*id+1)/self.board.shape[0])
            col = 2*(id+1) - row*self.board.shape[0] - 1

            # finding the rows and cols
            self.board[row][col] = 1
            self.states = move
        else: # if move is empty
            # finding the rows and cols
            # print('Updating states in makemove')
            self.board[row][col] = 1
            self.updateState(row,col)

        # print('Finding if boxes are taken')
        boxTaken = 0
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[0]):
                if i%2 !=0 and j %2 !=0:
                    if self.board[i+1][j] == 1 and self.board[i-1][j] == 1 and self.board[i][j+1] == 1  and self.board[i][j-1] == 1 and self.board[i][j] ==0:
                        self.board[i][j] = self.player
                        boxTaken = 1
                        # print('Box taken', i ,j)
        if not boxTaken:
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

        return boxTaken

    def isBoardFull(self):
        return np.all(self.board)

    def winner(self):
        one_count = 0
        two_count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if (i % 2 != 0 and j % 2 != 0):
                    if self.board[i][j] == 1:
                        one_count = one_count + 1
                    elif self.board[i][j] == 2:
                        two_count = two_count + 1
                else:
                    continue

        if (one_count >  two_count):
            return 1
        elif (two_count > one_count):
            return 2
        else:
            return 0
        # return (1 if one_count > two_count else 2 if two_count < one_count else 0)

###############################################################
#---------------------Play against Human----------------------#

def benchmark(game,episode_num,grid_size):
    winTotal = 0.0
    drawTotal = 0.0
    lossTotal = 0.0
    log_file = "./data3_"+str(episode_num)+"_N.csv"
    for i in range(episode_num):
        if (i%100 ==0): print('Episodes :' , i)

        game = dotsnboxes(grid_size)
        firstTurn = random.randint(0,1)
        # print(firstTurn)
        if firstTurn == 1:
            aiCharacter = 2
            userLetter = 1
        else:
            aiCharacter = 1
            userLetter = 2

        aiAgent = ai(game, grid_size, 1, 0.1,0.95, 1.0, 0.01, 100)
        aiAgent.loadFromCsv()
        turn = firstTurn
        gameOn = 1
        while gameOn == 1:
            if game.player == aiCharacter:
                aiAgent.getMoveVsHuman()
                if game.isBoardFull():
                    gameOn = 0

            # user turn
            else:
                m, n = random.choice(game.availMove())
                game.makeMove([],int(m),int(n))
                if game.isBoardFull():
                    gameOn = 0

        # print('winner is ' + str(game.winner()))
        if game.winner() == aiCharacter:
            winTotal = winTotal + 1
        elif game.winner() == 0:
            drawTotal = drawTotal + 1
        else:
            lossTotal = lossTotal + 1
        
        with open(log_file, 'a') as file:
            file.write('{},{},{}\n'.format(winTotal/(i+1), drawTotal/(i+1), lossTotal/(i+1)))
            # print('Total Episode :', episode_num)
            # print('Win percentage is: ', winTotal / episode_num)
            # print('Draw percentage is: ', drawTotal / episode_num)
    



def trainAI(grid_size, episode_num):
    aiAgent = ai(dotsnboxes,grid_size, 1e-6,  0.05, 0.6, 1.0, 0.01,episode_num)
    aiAgent.trainFromEpisode()
    aiAgent.write2csv()


def main():
    episode_num = [100,1000,10000]
    grid_size = 3
    game = dotsnboxes(grid_size)

    for i in range(len(episode_num)):
        trainAI(grid_size, episode_num[i])
        benchmark(game, episode_num[i], grid_size)


if __name__ == "__main__":
    main()
