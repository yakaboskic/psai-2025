import numpy as np
import json
import itertools

# Variables
V = np.zeros((4,4))
A = [(1,0), (-1, 0), (0, 1), (0, -1)]
threshold = 0.01
discount_rate = 0.9

# Helper functions
def get_neighbors(state, size, A):
    neighbors = []
    for a in A:
        new_state = tuple(np.array(state) + np.array(a))
        if new_state[0] < 0 or new_state[0] > (size - 1):
            continue
        if new_state[1] < 0 or new_state[1] > (size - 1):
            continue
        neighbors.append(new_state)
    return neighbors

# Wall Probs
T = {}
for i in range(4):
    for j in range(4):
        state = (i, j)
        for a in A:
            new_state = tuple(np.add(np.array(state), np.array(a)))
            if new_state[0] < 0 or new_state[0] > 3:
                T[(state, a, state)] = 0.99
                neighbors = get_neighbors(state, 4, A)
                for neighbor in neighbors:
                    T[(state, a, neighbor)] = 0.01 / len(neighbors)
            elif new_state[1] < 0 or new_state[1] > 3:
                T[(state, a, state)] = 0.99
                neighbors = get_neighbors(state, 4, A)
                for neighbor in neighbors:
                    T[(state, a, neighbor)] = 0.01 / len(neighbors)
            else:
                T[(state, a, new_state)] = .8
                neighbors = get_neighbors(state, 4, A)
                for neighbor in neighbors:
                    if neighbor != new_state:
                        T[(state, a, neighbor)] = .2 / len(neighbors)

def get_reward(state):
    if state == (1, 2):
        return -10
    if state == (2,1):
        return -100
    if state == (3,3):
        return 100
    return 0

max_delta = np.inf
iteration_count = 0
while max_delta > threshold:
    iteration_count += 1
    for state in itertools.product(range(4), range(4)):
        all_expected_rewards = []
        for a in A:
            expect_reward = 0
            for neighbor in get_neighbors(state, 4, A):
                P = T[((state, a, neighbor))]
                R = get_reward(state)
                discount = discount_rate * V[neighbor]
                expect_reward += P*(R + discount)
            all_expected_rewards.append((expect_reward, a))
        V[state] = sorted(all_expected_rewards, reverse=True)[0]
        

