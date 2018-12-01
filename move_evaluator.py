import string

class MoveEvaluator():
    def evaluateMove(self, move, board):
        """given a move and the current board return a evaluation
           of the move such that better moves return higher scores
           
        Args:
        - move (2-Tuple) : a move.
        - board (Board) : the current board state
        
        Returns (double):
          A evaluation score of the the given move
        """
        raise NotImplementedError
        
class TestMoveEvaluator(MoveEvaluator):        
    def evaluateMove(self, move, board):
        return 1

class SimpleMoveEvaluator(MoveEvaluator):
    def __init__(self, probabilityModel):
        self.probabilityModel = probabilityModel
        
    def evaluateMove(self, move, board):
        state = board.state[1:-1, 1:-1]
        state[move[0] - 1, board.col_to_number(move[1]) - 1]
        return self.probabilityModel.predict(state)
