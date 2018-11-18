import random


class Player(object):

    def move(self, board):
        """Given current board, return the next move.
           
        Args:
          - board (Board): current board.
          
        Returns (tuple(int, str)):
          Position of next move as a tuple, e.g., (3, "C")
        """
        raise NotImplementedError


class RandomPlayer(Player):
    
    def move(self, board):
        possibleMoves = board.getPossibleMoves()
        if possibleMoves:
            return random.choice(possibleMoves)
        else:
            raise Exception("No possible moves to make.")
            
            
class HumanPlayer(Player):
    
    def move(self, board):
        possibleMoves = board.getPossibleMoves()
        while True:
            loc = input(
                "Enter the location where you want to place a piece "
                "(e.g., 'K3'): "
            )
            r, c = int(loc[1:]), loc[0].lower()
            # check that this is an allowable move
            if (r, c) in possibleMoves:
                break
            else:
                print("That is not an allowable move.")
        return (r, c)