class Generative_Method(object):
    def generate(self, player1, player2):
        """Given current board, return the next move.
           
        Args:
          - board (Board): current board.
          
        Returns (tuple(int, str)):
          Position of next move as a tuple, e.g., (3, "C")
        """
        raise NotImplementedError
        
class Simple_Generator(Generative_Method):
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    def generate(self):
        game = Game(self.player1, self.player2)
        return game.play(verbose=False)
