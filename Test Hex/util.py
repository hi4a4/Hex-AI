import re

import numpy as np

from hex.board import Board
from hex.game import Game
from generative_method import Simple_Generator

def getBoard(board):    
   return np.take(board.state[1:14], range(1,14), axis=1)
  
def makeInputOutput(moveList, winner, scraped=True):
    '''
    moveList - string representing all move in a game
    scraped - True - this movelist was scraped False - a movelist from a hex game
    winner - string - white or black
    '''
    outputWinner = [1, 0]
    if (winner == 'white'):
        outputWinner = [0, 1]
    inputBoard = []
    outputWin = []
    if scraped:
        splitOn = r"([a-z]+)([0-9]+)"
    else:
        splitOn = r"([0-9]+)([a-z]+)"
    black = True
    tempBoard = Board()
    moves = re.findall(splitOn, moveList)
    for index, move in enumerate(moves):
#         print(getBoard(tempBoard))
#         print(1 * (tempBoard.getStateForPlayer(2))
        inputBoard.append(get_board(tempBoard))
#         inputBoard.append(getBoard(tempBoard))
        #D sun stores number then letter
        if scraped:
          move = move[::-1]
        # move is in form (number, letter)
        # Change letter to integer
        letterToNumber = tempBoard.col_to_number[move[1]]
        # Cast string number to integer
        move = (int(move[0]), letterToNumber)
        # If * mirror the move set the first player to white
        if '*' in moveList and index==0:
            #mirror the first move
            black = not(black)
            move = (move[1], move[0])
        #Out of 13*13= 169 possible board squares
        moveIntegerized = 13*(int(move[1])-1) + move[0]
        # Store which square the piece went
        outputWin.append(outputWinner)
        # Append piece to the board 1 is black 2 is white
        tempBoard.addPiece(move, 1 if black else 2)
        black = not(black)
#     print(tempBoard.chains)
#     print(tempBoard.__str__())
            
    return inputBoard[1:], outputWin[1:]

def get_board(board):
  """Get a 2 x n x n tensor representing a padded, two-channel representation of the board

  Args
  - board (board object)

  Returns (np.ndarray)
  A 2 x n x n Numpy array.
  """
  return np.array([hex_pad((1 * (board.getStateForPlayer(1) > 0)), 1), hex_pad((1 * (board.getStateForPlayer(2) > 0)), 2)])
  
def hex_pad(board, player, pad_width=2):
  padded = np.lib.pad(board, pad_width, 'constant', constant_values=1)
  if player == 1:
    padded[pad_width:-pad_width:1][: ,0:pad_width] = 0
    padded[pad_width:-pad_width:1][: ,-pad_width:] = 0
  if player == 2:
    padded[0:pad_width, :][:, pad_width:-pad_width:1] = 0
    padded[-pad_width:, :][:, pad_width:-pad_width:1] = 0
  return padded

def generate_games(n, player1, player2, generator=None):
    if generator is None:
        generator = Simple_Generator()
    movelists, winners = generator.generate(n, player1, player2)
    return movelists, winners

def makeInputOutputTotal(moveLists, winners, scraped=True):
    
    total = map(lambda args: makeInputOutput(args[0], args[1], args[2]),
                zip(moveLists, winners, [scraped]*len(winners)))
    board_states_cumulative, winners_cumulative = zip(*total)
    return (np.concatenate(board_states_cumulative, axis=0),
            np.concatenate(winners_cumulative, axis=0))
