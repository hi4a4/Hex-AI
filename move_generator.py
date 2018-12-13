import numpy as np

class MoveGenerator():
    
    def generateMove(self, board, evaluator, role):
        """given the possible moves and a move evaluator
           return a next move
           
        Args:
        - board (Board) : current board
        - evaluator (MoveEvaluator) : a move evaluator
        
        Returns (tuple(int, str)):
          Position of next move as a tuple, e.g., (3, "C")
        """
        raise NotImplementedError
        
class ExhaustiveGenerator(MoveGenerator):
    def generateMove(self, board, evaluator, role):
        possibleMoves = board.getPossibleMoves()
        np.random.shuffle(possibleMoves)
        return possibleMoves[np.argmax(evaluator.evaluateMoves(possibleMoves, board, role))]
    
class ExhaustiveProbabilisticGenerator(MoveGenerator):
    def __init__(self, transformation=None):
        if transformation is None:
            transformation = lambda x : x
        self.transformation = transformation

    def generateMove(self, board, evaluator, role):
        possibleMoves = board.getPossibleMoves()
        moveProbs = np.array(evaluator.evaluateMoves(possibleMoves, board, role))
        moveProbs = self.transformation(moveProbs)
        moveProbs = moveProbs / sum(moveProbs)
        return possibleMoves[np.random.choice(len(possibleMoves), 1, p=moveProbs)[0]]
    
class SamplingGenerator(MoveGenerator):
    def __init__(self, num_samples):
        self.num_samples = num_samples

    def generateMove(self, board, evaluator, role):
        possibleMoves = board.getPossibleMoves()
        sample = [possibleMoves[i] for i in np.random.choice(len(possibleMoves), size=self.num_samples)]
        return sample[np.argmax(evaluator.evaluateMoves(sample, board, role))]
    
class SamplingProbabilisticGenerator(MoveGenerator):
    def __init__(self, num_samples, transformation=None):
        if transformation is None:
            transformation = lambda x : x
        self.transformation = transformation
        self.num_samples = num_samples

    def generateMove(self, board, evaluator, role):
        possibleMoves = board.getPossibleMoves()
        sample = [possibleMoves[i] for i in np.random.choice(len(possibleMoves), size=self.num_samples)]
        moveProbs = np.array(evaluator.evaluateMoves(sample, board, role))
        moveProbs = self.transformation(moveProbs)
        moveProbs = moveProbs / sum(moveProbs)
        return sample[np.random.choice(len(sample), 1, p=moveProbs)[0]]

class MonteCarloGenerator(MoveGenerator):
    def generateMove(self, board, evaluator):
        raise NotImplmentedError