

def print_state(list, size):
    position = 0
    for i in range(1, size+1):
        print(" "*(size-i), end="")
        for j in range(i):
            if list[position] == 0:
                print("O ", end="")
            if list[position] == 1:
                print("# ", end="")
            position += 1
        print()


def rotate120(a):
    """This will create symmetric states"""
    mapping = {
        0: 14,
        1: 9,
        2: 13,
        3: 5,
        4: 8,
        5: 12,
        6: 2,
        7: 4,
        8: 7,
        9: 11,
        10: 0,
        11: 1,
        12: 3,
        13: 6,
        14: 10,
    }
    a_copy = a.copy()
    a = [0] * len(a)
    for i in range(len(a)):
        a[i] = a_copy[mapping[i]]
    return a

def main_argparse():
    pass

def main_input():
    initial = [0 for _ in range(15)]
    a = input('Pass in all indices that are pegged (space delimited): ').strip()
    a = [int(item.strip()) for item in a.split()]
    for i in a:
        initial[i] = 1
    print_state(initial, 5)
    r1 = rotate120(initial)
    print_state(r1, 5)
    r2 = rotate120(r1)
    print_state(r2, 5)

if __name__ == '__main__':
    #main_argparse()
    main_input()