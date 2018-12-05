from hex.game import Game

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
    def gen_wrap(players):
        game = Game(players[0], players[1])
        return game.play(verbose=False)

    def generate(self, n, player1, player2):
        return zip(*map(Simple_Generator.gen_wrap, [(player1, player2)] * n))
