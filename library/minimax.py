import numpy as np

class MinimaxSolver:
    def __init__(self,
                 initial_state,
                 get_successor_fn,
                 is_terminal_fn,
                 utility_fn,
                 other_player=2,
                 max_depth=None,
                ):
        
        self.max_depth = max_depth
        self.state = initial_state
        self.get_successors = get_successor_fn
        self.is_terminal = is_terminal_fn
        self.utility = utility_fn
        self.other_player = other_player

    def minimax(self, state, player, depth):
        if self.is_terminal(state) or depth > self.max_depth:
            return self.utility(state), state
        
        if player == 1: # Maximizing player
            best_score = -np.inf
            best_action = None
            for action, successor in self.get_successors(state):
                score, _ = self.minimax(successor, 2, depth - 1)
                if score > best_score:
                    best_score = score
                    best_action = action
            return best_score, best_action
        
        else: # Minimizing player
            best_score = np.inf
            best_action = None
            for action, successor in self.get_successors(state):
                score, _ = self.minimax(successor, 1, depth - 1)
                if score < best_score:
                    best_score = score
                    best_action = action
            return best_score, best_action
            
