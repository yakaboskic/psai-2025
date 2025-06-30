import argparse
import numpy as np


def median(n):
    n.sort()
    length = len(n) % 2
    if length == 0:
        ind1 = len(n) // 2
        ind2 = ind1 - 1
        val1 = n[ind1]
        val2 = n[ind2]
        return val1 + val2 / 2
    return n[len(n) // 2]

def mean(n):
    return np.mean(n)

OPERATIONS = {
    'median': median,
    'mean': mean
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('numbers', help='Numbers you want to operate over.', nargs='+', type=int)
    parser.add_argument('--operation', default='median', choices=['median', 'mean'])
    args = parser.parse_args()

    print(
        OPERATIONS.get(args.operation)(args.numbers)
    )
    


if __name__ == '__main__':
    main()