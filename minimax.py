from decimal import Decimal


def mini_max(node, depth, isMaximizingPlayer, values, alpha, beta):
    if depth == 4:
        return values[node]

    if isMaximizingPlayer:
        best_val = Decimal('-Infinity')
        for i in range(2):
            val = mini_max(node * 2 + i, depth + 1, False, values, alpha, beta)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val

    else:
        best_val = Decimal('Infinity')
        for i in range(2):
            val = mini_max(node * 2 + i, depth + 1, True, values, alpha, beta)
            best_val = min(best_val, val)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val


if __name__ == '__main__':
    values = [8, 5, 6, -4, 3, 8, 4, -6, 1, 2, 5, 2, 1, 1, 1, 1]
    alpha = Decimal('-Infinity')
    beta = Decimal('Infinity')
    print("The optimal value is: ", mini_max(0, 0, True, values, alpha, beta))