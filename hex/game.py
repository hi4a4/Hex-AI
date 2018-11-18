from . import Board

class Game:
    
    def __init__(self, black_player, white_player):
        """Initializes a game.
        
        Args
        - black_player (Player): an instance of Player which
                                 will serve as the black player
        - white_player (Player): an instance of Player which
                                 will serve as the white player
        """
        self.board = Board()
        self.black_player = black_player
        self.white_player = white_player
        
    def play(self, verbose=True):
        """Plays an entire game.
        
        Args
        - verbose (bool): whether or not to print output
        
        Returns (tuple, str)
        A tuple consisting of two strings: the move list
        (in the format required by this project) and the
        winner (either "white", "black", or "draw")
        """
        
        # initialize string for storing the move list
        movelist = ""
        
        # initialize the winner
        winner = None
        
        # Make 2 moves at a time (1 black, 1 white).
        # The maximum number of such moves is the
        # number of spaces (board.size ** 2) divided
        # by 2, rounded down.
        for _ in range(self.board.size ** 2 // 2):
            
            # make black move
            r, c = self.black_player.move(self.board)
            movelist += "%d%s" % (r, c)
            win1 = self.board.addPiece(
                (r, self.board.col_to_number[c]), 
                1
            )
            
            # print board
            if verbose:
                print(self.board)

            # check if black won
            if win1:
                winner = "black"
                if verbose:
                    print("BLACK PLAYER WINS")
                break
                
            # make white move
            r, c = self.white_player.move(self.board)
            movelist += "%d%s" % (r, c)
            win2 = self.board.addPiece(
                (r, self.board.col_to_number[c]), 
                2
            )
            
            # print board
            if verbose:
                print(self.board)

            # check if white won
            if win2:
                winner = "white"
                if verbose:
                    print("WHITE PLAYER WINS")
                break
                
        # If there are an odd number of spaces on the board,
        # it's possible that the game has not terminated yet.
        # There is only one remaining space on the board,
        # which black must take. Black will win the game
        # because Hex cannot end in a draw.
        if winner is None:
            # there should only be 1 remaining move, get it
            possibleMoves = self.board.getPossibleMoves()
            assert(len(possibleMoves) == 1)
            r, c = possibleMoves[0]
            movelist += "%d%s" % (r, c)
            
            # declare black the winner
            winner = "black"
            if verbose:
                print("BLACK PLAYER WINS")
            
        return movelist, winner