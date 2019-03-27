from decimal import Decimal

import math


def mini_max(node, depth, isMaximizingPlayer, values, alpha, beta, treeDepth):
    if depth == treeDepth:
        return values[node]

    if isMaximizingPlayer:
        best_val = Decimal('-Infinity')
        for i in range(2):
            val = mini_max(node * 2 + i, depth + 1, False, values, alpha, beta, treeDepth)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val

    else:
        best_val = Decimal('Infinity')
        for i in range(2):
            val = mini_max(node * 2 + i, depth + 1, True, values, alpha, beta, treeDepth)
            best_val = min(best_val, val)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val


if __name__ == '__main__':
    values = [8, 5, 6, -4, 3, 8, 4, -6, 1, 2, 5, 2, 10, 11, 12, 13]
    treeDepth = math.log(len(values), 2)
    alpha = Decimal('-Infinity')
    beta = Decimal('Infinity')
    print("The optimal value is: ", mini_max(0, 0, True, values, alpha, beta, treeDepth))