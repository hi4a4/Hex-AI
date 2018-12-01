import numpy as np

class MoveGenerator():
    
    def generateMove(self, board, evaluator):
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
    def generateMove(self, board, evaluator):
        evaluate = lambda move : evaluator.evaluate_move(move, board)
        possibleMoves = board.getPossibleMoves()
        np.random.shuffle(possibleMoves)
        return possibleMoves[np.argmax(map(evaluate, possibleMoves))]
    
class ExhaustiveProbalisticGenerator(MoveGenerator):
    def __init__(self, transformation=None):
        if transformation is None:
            transformation = lambda x : x
        self.transformation = transformation

    def generateMove(self, board, evaluator):
        evaluate = lambda move : evaluator.evaluate_move(move, board)
        possibleMoves = board.getPossibleMoves()
        moveProbs = np.array(map(evaluated, possibleMoves))
        moveProbs = self.transformation(moveProbs)
        moveProbs = moveProbs / sum(moveProbs)
        return np.random.choice(possibleMoves, 1, p=moveProbs)
    
class SamplingGenerator(MoveGenerator):
    def __init__(self, num_samples):
        self.num_samples = num_samples

    def generateMove(self, board, evaluator):
        evaluate = lambda move : evaluator.evaluate_move(move, board)
        possibleMoves = board.getPossibleMoves()
        sample = np.random.choice(possibleMoves, size=self.num_samples)
        return (sample[np.argmax(map(evaluate, sample))])
    
class SamplingProbalisticGenerator(MoveGenerator):
    def __init__(self, num_samples, transformation=None):
        if transformation is None:
            transformation = lambda x : x
        self.transformation = transformation
        self.num_samples = num_samples

    def generateMove(self, possibleMoves, evaluator):
        evaluate = lambda move : evaluator.evaluate_move(move, board)
        possibleMoves = board.getPossibleMoves()
        sample = np.random.choice(possibleMoves, size=self.num_samples)
        moveProbs = np.array(map(evaluate, sample))
        moveProbs = self.transformation(moveProbs)
        moveProbs = moveProbs / sum(moveProbs)
        return np.random.choice(sample, 1, p=moveProbs)

class MonteCarloGenerator(MoveGenerator):
    def generateMove(self, board, evaluator):
        raise NotImplmentedError