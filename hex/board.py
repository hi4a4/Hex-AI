import numpy as np
import string

class Board:
    
    def __init__(self, size=13):
        # board size
        self.size = size
        # define mappings between 
        # columns (a, b, c, ...) and numbers (1, 2, 3, ...)
        self.col_to_number = dict(zip(
            string.ascii_lowercase,
            range(1, size + 1)
        ))
        self.number_to_col = dict(zip(
            range(1, size + 1),
            string.ascii_lowercase
        ))
        # define board state (0 for empty, 1 for black,
        # 2 for white), with two extra rows and columns 
        # for the boundaries (their state is -1)
        self.state = np.zeros((size + 2, size + 2), 
                              dtype=np.int8)
        self.state[:, [0, size + 1]] = -1
        self.state[[0, size + 1], :] = -1
        # initialize data structure for storing the chains 
        # (i.e., connected components) for each player, 
        # used to determine when a player has won.
        self.chains = {
            1: [
                {(0, i) for i in range(self.size + 1)},
                {(self.size + 1, i) for i in range(self.size + 1)}
            ],
            2: [
                {(i, 0) for i in range(self.size + 1)},
                {(i, self.size + 1) for i in range(self.size + 1)}
            ]
        }
        
    def addPiece(self, loc, player):
        """Adds piece to board.
        
        Args
        - loc: space to add the piece, specified as a 
               tuple (i, j) where 1 <= i,j <= self.size
        - player: which player (1 for black, 2 for white)
                  should occupy that space
                  
        Returns
        The player who won, if applicable.
        """
        # add piece to board if loc is unoccupied
        if self.state[loc] == 0:
            self.state[loc] = player
        else:
            raise Exception("Space is already occupied.")
        # update chains using the union-find algorithm
        new_chain = set([loc])
        for space in self.getAdjacent(loc):
            # if any existing chain is adjacent to new chain,
            # merge the chains
            for chain in self.chains[player]:
                if space in chain:
                    self.chains[player].remove(chain)
                    new_chain.update(chain)
                    break
        self.chains[player].append(new_chain)
        # check whether this player has won
        return self.checkWin(player)
    
    def getAdjacent(self, space):
        """Get all adjacent spaces to a given space.
        
        Args
        - space (tuple, int): a space on the board
        
        Returns (list, int)
        A list of all spaces on the board that are adjacent.
        """
        r, c = space
        return [
            (r - 1, c), (r - 1, c + 1),
            (r, c - 1), (r, c + 1),
            (r + 1, c - 1), (r + 1, c)
        ]
    
    def checkWin(self, player):
        """Check whether player has won.
        
        Args
        - player (int): 1 for black, 2 for white
        
        Returns (bool)
        True if player has won
        """
        for group in self.chains[player]:
            if player == 1:
                if (
                    any(i == 0 for i, _ in group) and
                    any(i == self.size for i, _ in group)
                ):
                    return True
            if player == 2:
                if (
                    any(j == 0 for _, j in group) and
                    any(j == self.size for _, j in group)
                ):
                    return True
        return False
    
    def getPossibleMoves(self):
        """Get a list of all possible moves.
        
        Returns (tuple(int, str))
        List of valid moves (i.e., empty spaces on the board)
        using the (number, letter) convention to refer to spaces.
        """
        return [
            (int(r), self.number_to_col[c])
            for r, c in zip(*np.where(self.state == 0))
        ]
    
    def __str__(self):
        """Prints the current board.
        """
        out = "    A B C D E F G H I J K L M\n"
        out += "   \\---------------------------\\\n"
        for i in range(1, self.size + 1):
            if i < 10:
                out += " "
            out += (str(i) + (" " * i) + "W\\ ")
            for j in range(1, self.size + 1):
                if self.state[i, j] == 0:
                    out += "O "
                elif self.state[i, j] == 1:
                    out += "B "
                elif self.state[i, j] == 2:
                    out += "W "
            out += "\\W\n"
        out += (" " * 17) + "\\---------------------------\\\n"
        out += (" " * 19) + ("B " * 13)
        return out