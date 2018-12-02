import string

import numpy as np

class MoveEvaluator():
    def evaluateMoves(self, moves, board):
        """give moves and the current board return a evaluation
           of the moves such that better moves return higher scores
           
        Args:
        - move (list<2-Tuple>) : a list of moves.
        - board (Board) : the current board state
        
        Returns (double):
          A evaluation score of the the given move
        """
        raise NotImplementedError
        
class BlackWinMoveEvaluator(MoveEvaluator):
    def __init__(self, probabilityModel):
        self.probabilityModel = probabilityModel
       
    def evaluateMoves(self, moves, board):
        color = np.prod(board[board != 0].shape) % 2
        if color == 0:
            color += 2
        print(color)
        states = np.repeat(board.state[np.newaxis, 1:-1, 1:-1], len(moves), axis=0)
        for i, state in enumerate(states):
            state[moves[i][0] - 1, board.col_to_number[moves[i][1]] - 1] = color
        evals = self.probabilityModel.predict(states.reshape(list(states.shape) + [1]))
        if color == 1:
            return 1 - evals[:, 1]
        else:
            return evals[:, 0]

class TestMoveEvaluator(MoveEvaluator):        
    def evaluateMoves(self, moves, board):
        return np.ones(len(moves))

    
class SimpleMoveEvaluator(MoveEvaluator):
    def __init__(self, probabilityModel):
        self.probabilityModel = probabilityModel
        
    def evaluateMoves(self, moves, board):
        color = np.prod(board[board != 0].shape) % 2
        if color == 0:
            color += 2
        states = np.repeat(board.state[np.newaxis, 1:-1, 1:-1], len(moves), axis=2)
        for i, state in enumerate(states):
            state[moves[i][0] - 1, board.col_to_number[moves[i][1]] - 1] = color
        return self.probabilityModel.predict(states.reshape(list(states.shape) + [1]))[:, color]
