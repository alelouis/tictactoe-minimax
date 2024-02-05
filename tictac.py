import networkx as nx
import numpy as np


def has_win(board, player):
    horizontal = (board == player).all(axis=0).any()
    vertical = (board == player).all(axis=1).any()
    diag = np.diag(board == player).all()
    anti_diag = np.diag(board[::-1, :] == player).all()
    return horizontal or vertical or diag or anti_diag


def possible_moves(player, board):
    rows, cols = np.where(board == 0)
    n_possible_moves = rows.size
    next_boards = np.tile(board, (n_possible_moves, 1, 1))
    for idx_game, (i, j) in enumerate(zip(rows, cols)):
        next_boards[idx_game][i, j] = player
    return next_boards


def evaluate(board):
    if has_win(board, 1):
        return 1
    if has_win(board, -1):
        return -1
    else:
        return 0


def add_move(G, player):
    leaves = [v for v, d in G.out_degree() if d == 0]
    for leaf in leaves:
        board = G.nodes[leaf]['board']
        if not (has_win(board, 1) or has_win(board, -1)):
            next_boards = possible_moves(player, board)
            for idx_board in range(next_boards.shape[0]):
                G.add_node(G.number_of_nodes(), board=next_boards[idx_board])
                G.add_edge(leaf, G.number_of_nodes() - 1)
    return G


def play_to_depth(board, max_depth):
    G = nx.DiGraph()
    G.add_node(0, board=board)
    player = 1
    for _ in range(max_depth):
        G = add_move(G, player)
        player = -player
    return G


def evaluate_leaves(G, player):
    leaves = [v for v, d in G.out_degree() if d == 0]
    for leaf in leaves:
        board = G.nodes[leaf]['board']
        G.nodes[leaf]['value'] = evaluate(board)


def minimax(root, G, player):
    if G.out_degree(root) != 0:
        f = max if player == 1 else min
        G.nodes[root]['value'] = f([minimax(s, G, -player) for s in G.successors(root)])
    return G.nodes[root]['value']
