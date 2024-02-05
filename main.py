from tictac import *
import pickle

board = np.zeros((3, 3))
g = play_to_depth(board, 9)
evaluate_leaves(g, 1)
minimax(0, g, 1)

with open('graph.pkl', 'wb') as f:
    pickle.dump(g, f)

