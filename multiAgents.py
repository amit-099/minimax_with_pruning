import operator
import random
import util

from game import Agent


class ReflexAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        successor_states = []
        for action in gameState.getLegalActions(0):
            successor_states.append(gameState.generateSuccessor(0, action))
        all_values = {}
        i = 0
        for suc_state in successor_states:
            all_values.update({i: self.minimizing_ghost(0, suc_state, 1)})
            i += 1
        return gameState.getLegalActions(0)[max(all_values.iteritems(), key=operator.itemgetter(1))[0]]

    def maximizing_pacman(self, depth, gameState):
        pacman_successors = []
        if self.depth == depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            pacman_successors.append(gameState.generateSuccessor(0, action))
        values = []
        for suc in pacman_successors:
            values.append(self.minimizing_ghost(depth, suc, 1))
        return max(values)

    def minimizing_ghost(self, depth, gameState, ghost_number):
        ghost_successors = []
        if self.depth == depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        total_agents = gameState.getNumAgents()
        for action in gameState.getLegalActions(ghost_number):
            ghost_successors.append(gameState.generateSuccessor(ghost_number, action))
        if ghost_number >= total_agents - 1:
            values = []
            for suc in ghost_successors:
                values.append(self.maximizing_pacman(depth + 1, suc))
        else:
            values = []
            for suc in ghost_successors:
                values.append(self.minimizing_ghost(depth, suc, ghost_number + 1))
        return min(values)


class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        global best
        def min_ghost(depth, state, ghost_number, alpha, beta):
            if ghost_number == state.getNumAgents():
                return max_pacman(depth + 1, state, 0, alpha, beta)
            min_val = 999999999
            for action in state.getLegalActions(ghost_number):
                ghost_successors = state.generateSuccessor(ghost_number, action)
                min_val = min(min_val, min_ghost(depth, ghost_successors, ghost_number + 1, alpha, beta))
                if min_val < alpha:
                    return min_val
                beta = min(beta, min_val)
            if min_val is 999999999:
                return self.evaluationFunction(state)
            return min_val

        def max_pacman(depth, state, ghost_number, alpha, beta):
            if depth > self.depth:
                return self.evaluationFunction(state)
            max_val = -999999999
            for action in state.getLegalActions(ghost_number):
                pacman_successors = state.generateSuccessor(ghost_number, action)
                max_val = max(max_val, min_ghost(depth, pacman_successors, ghost_number + 1, alpha, beta))
                if max_val > beta:
                    return max_val
                alpha = max(alpha, max_val)
            if max_val is -999999999:
                return self.evaluationFunction(state)
            return max_val

        alpha = -999999999
        beta = 999999999
        value = -999999999
        best_action = {}
        for action in gameState.getLegalActions(0):
            ghost_successors = gameState.generateSuccessor(0, action)
            value = max(value, min_ghost(1, ghost_successors, 1, alpha, beta))
            if value > alpha:
                best_action.update({action: value})
                alpha = best_action.get(action)
        return max(best_action.iteritems(), key=operator.itemgetter(1))[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
