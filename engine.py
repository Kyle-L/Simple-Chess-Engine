import chess
import chess.engine
from board_evaluator import evaluate

class console_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _determine_best_move(board, is_white, depth = 3):
    """Given a board, determines the best move.

    Args:
        board (chess.Board): A chess board.
        is_white (bool): Whether the particular move is for white or black.
        depth (int, optional): The number of moves looked ahead.

    Returns:
        chess.Move: The best predicated move.
    """

    best_move = -100000 if is_white else 100000
    best_final = None
    for move in board.legal_moves:
        board.push(move)
        value = _minimax_helper(depth - 1, board, -10000, 10000, not is_white)
        board.pop()
        if (is_white and value > best_move) or (not is_white and value < best_move):
            best_move = value
            best_final = move
    return best_final

def _minimax_helper(depth, board, alpha, beta, is_maximizing):
    if depth <= 0 or board.is_game_over():
        return evaluate(board)

    if is_maximizing:
        best_move = -100000
        for move in board.legal_moves:
            board.push(move)
            value = _minimax_helper(depth - 1, board, alpha, beta, False)
            board.pop()
            best_move = max(best_move, value)
            alpha = max(alpha, best_move)
            if beta <= alpha:
                break
        return best_move
    else:
        best_move = 100000
        for move in board.legal_moves:
            board.push(move)
            value = _minimax_helper(depth - 1, board, alpha, beta, True)
            board.pop()
            best_move = min(best_move, value)
            beta = min(beta, best_move)
            if beta <= alpha:
                break
        return best_move

if __name__ == '__main__':
    board = chess.Board()

    print(console_colors.HEADER + f'==================================================' + console_colors.ENDC)
    print(console_colors.HEADER + f'                   Chess Engine                   ' + console_colors.ENDC)
    print(console_colors.HEADER + f'==================================================' + console_colors.ENDC)
    print()

    is_white = input(console_colors.OKBLUE + 'Will you be playing as white or black (white/black)? ' + console_colors.ENDC).lower()[0] == "w"

    print()
    print(console_colors.HEADER + f'= Board State =' + console_colors.ENDC)
    print(board)

    if is_white:
        while not board.is_game_over():
            print()
            while True:
                try:
                    move = board.parse_san(input(console_colors.OKGREEN + 'Enter your move: ' + console_colors.ENDC))
                except ValueError:
                    print(console_colors.FAIL + f'That is not a valid move!' + console_colors.ENDC)
                    continue
                break
            board.push(move)

            move = _determine_best_move(board, False)
            board.push(move)

            print()
            print(console_colors.FAIL + f'Black made the move: {move}' + console_colors.ENDC)
            print()
            print(console_colors.HEADER + f'= Board State =' + console_colors.ENDC)
            print(board)
            print()
    else:
        while not board.is_game_over():
            move = _determine_best_move(board, True)
            board.push(move)

            print()
            print(console_colors.FAIL + f'White made the move: {move}' + console_colors.ENDC)
            print()
            print(console_colors.HEADER + f'= Board State =' + console_colors.ENDC)
            print(board)

            print()
            while True:
                try:
                    move = board.parse_san(input(console_colors.OKGREEN + 'Enter your move: ' + console_colors.ENDC))
                except ValueError:
                    print(console_colors.FAIL + f'That is not a valid move!' + console_colors.ENDC)
                    continue
                break
            board.push(move)

    print(console_colors.HEADER + f'The game is over!' + console_colors.ENDC)
