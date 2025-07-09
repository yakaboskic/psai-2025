class MinimaxSolver:
    def __init__(self, get_successors, is_terminal, evaluate, other_player):
        """
        get_successors: function(state, player) -> list of (action, new_state)
        is_terminal: function(state) -> bool
        evaluate: function(state) -> utility (int)
        other_player: function(player) -> other player
        """
        self.get_successors = get_successors
        self.is_terminal = is_terminal
        self.evaluate = evaluate
        self.other_player = other_player

    def minimax(self, state, player, depth):
        if self.is_terminal(state) or depth == 0:
            return self.evaluate(state), None

        if player == "X":  # Maximizing
            best_score = float('-inf')
            best_action = None
            for action, new_state in self.get_successors(state, player):
                score, _ = self.minimax(new_state, self.other_player(player), depth - 1)
                if score > best_score:
                    best_score = score
                    best_action = action
            return best_score, best_action

        else:  # Minimizing
            best_score = float('inf')
            best_action = None
            for action, new_state in self.get_successors(state, player):
                score, _ = self.minimax(new_state, self.other_player(player), depth - 1)
                if score < best_score:
                    best_score = score
                    best_action = action
            return best_score, best_action