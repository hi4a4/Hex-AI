import string
import copy
import numpy as np
import util

class MoveEvaluator():
    def evaluateMoves(self, moves, board, role):
        """give moves and the current board return a evaluation
           of the moves such that better moves return higher scores
           
        Args:
        - move (list<2-Tuple>) : a list of moves.
        - board (Board) : the current board state
        - role (string) : string representation of role
        
        Returns (double):
          A evaluation score of the the given move
        """
        raise NotImplementedError
        
    def setModel(self, model):
        raise NotImplementedError
        
class BlackWinMoveEvaluator(MoveEvaluator):
    def __init__(self, probabilityModel):
        self.probabilityModel = probabilityModel
       
    def evaluateMoves(self, moves, board, role):
        board_state = board.state[np.newaxis, 1:-1, 1:-1]
        color = np.prod(board_state[board_state != 0].shape) % 2 + 1
        states = np.repeat(board_state, len(moves), axis=0)
        for i, state in enumerate(states):
            state[moves[i][0] - 1, board.col_to_number[moves[i][1]] - 1] = color
        evals = self.probabilityModel.predict(boadstates.reshape(list(states.shape) + [1]))
        if color == 1:
            return 1 - evals[:, 1]
        else:
            return evals[:, 0]

    def setModel(self, model):
        self.probabilityModel = model

class TestMoveEvaluator(MoveEvaluator):        
    def evaluateMoves(self, moves, board, role):
        return np.ones(len(moves))

    def setModel(self, model):
        self.probabilityModel = model


class SimpleMoveEvaluator(MoveEvaluator):
    def __init__(self, probabilityModel):
        self.probabilityModel = probabilityModel
        
    def evaluateMoves(self, moves, board, role):
        color = 1 if role == "black" else 2
        #print(color)
        boards = [copy.deepcopy(board) for i in range(len(moves))]
        for move, board_i in zip(moves, boards):
            board_i.addPiece((move[0], board.col_to_number[move[1]]), color)
        board_states = np.stack(list(map(util.get_board, boards)))
        #print(board_states.shape)
        return self.probabilityModel.predict(np.swapaxes(np.swapaxes(board_states, 1, 2), 2, 3))[:, color - 1]

    def setModel(self, model):
        self.probabilityModel = model
