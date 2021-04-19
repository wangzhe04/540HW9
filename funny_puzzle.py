import copy
import heapq
import time




def heuristic (puzzle):
    row = 0
    col = 0
    h = 0
    #print(puzzle)
    for element in puzzle:
        # print(element)
        expect_corrd = get_expect_coord(element)

        if(element == 0):
            col += 1
            if col % 3 == 0 and col != 0:
                row += 1
            if col % 3 == 0 and col != 0:
                col = 0

            continue

        # print(element)
        h += abs(expect_corrd[0] - row) + abs(expect_corrd[1] - col)

        col += 1

        if col %3 == 0 and col != 0:
            row += 1
        if col % 3 == 0 and col != 0:
            col = 0
    return h

def pirnt_succ(state):

    succ_list = succ(state)

    for element in succ_list:
        print(element, 'h=' + str(heuristic(element)))

def succ(state):
    row = 0
    succ_list = []
    for i in range(9):
        if state[i] == 0:
            # for the first row
            if row == 0:
                # first row tiles can always switch with the tile under them
                succ1 = swap_pos(state, i, i + 3)
                succ_list.append(succ1)

                succs = help_print(state, i)
                if i % 3 == 1:
                    succ_list.append(succs[0])
                    succ_list.append(succs[1])
                else:
                    succ_list.append(succs)

            elif row == 1:
                # second row can always swith up and down
                succ1 = swap_pos(state, i, i + 3)
                succ3 = swap_pos(state, i, i - 3)

                succ_list.append(succ1)
                succ_list.append(succ3)

                succs = help_print(state, i)

                if i % 3 == 1:
                    succ_list.append(succs[0])
                    succ_list.append(succs[1])
                else:
                    succ_list.append(succs)

            elif row == 2:
                # third row can always swithc up
                succ1 = swap_pos(state, i, i - 3)
                succ_list.append(succ1)

                succs = help_print(state, i)

                if i % 3 == 1:
                    succ_list.append(succs[0])
                    succ_list.append(succs[1])
                else:
                    succ_list.append(succs)
        if i % 3 == 2:
            row += 1

    sorted(succ_list)


    return succ_list


def help_print(state, i):
    succ_list = []

    if i % 3 == 0:
        # col 0
        succ2 = swap_pos(state, i, i + 1)
        succ_list = succ2


    if i % 3 == 1:
        # col 1
        succ2 = swap_pos(state, i, i + 1)
        succ3 = swap_pos(state, i, i - 1)

        succ_list.append(succ2)
        succ_list.append(succ3)


    if i % 3 == 2:
        # col 2
        succ2 = swap_pos(state, i, i - 1)
        succ_list = succ2

    return succ_list


def swap_pos (state, pos1, pos2):
    state_copy = copy.deepcopy(state)
    a = state_copy[pos1]
    state_copy[pos1] = state_copy[pos2]
    state_copy[pos2] = a
    # print(state_copy)

    return state_copy


def get_expect_coord(value):
    coord = []
    if value == 1:
        coord = [0,0]
    elif value == 2:
        coord = [0,1]
    elif value == 3:
        coord = [0,2]
    elif value == 4:
        coord = [1,0]
    elif value == 5:
        coord = [1,1]
    elif value == 6:
        coord = [1,2]
    elif value == 7:
        coord = [2,0]
    elif value == 8:
        coord = [2,1]
    return coord

def solve(state):
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    a = A_star(state, goal_state)
    moves = 0

    i = len(a) - 1

    while i >= 0:
        # print(a[i])
        print(a[i], 'h='+ str(heuristic(a[i])), 'moves: ' + str(moves))

        i = i - 1
        moves += 1

    pq = []

def A_star(start, goal_state):
    open = []
    closed = []
    open_heap = []

    a = -1 # parent index

    current = start
    open.append(current)

    parents = dict()

    max_len = 0


    heapq.heappush(open_heap, (heuristic(start), start, (0, heuristic(start), a)))

    # used for reconstruct_path1 but ends with higher time complexity
    # static_heap.append((heuristic(start), start, (0, heuristic(start), a)))

    while len(open_heap) > 0:

        if len(open_heap) > max_len:
            max_len = len(open_heap)


        f_score, current, info = heapq.heappop(open_heap)

        open.remove(current)
        closed.append(current)

        if current == goal_state:
            print(max_len)
            return reconstruct_path(parents, current)

        for node in succ(current):


            temp_g_score = info[0] + 1
            temp_f_score = temp_g_score + heuristic(node)

            # parent_index = static_heap.index((f_score, current, info))

            if node not in closed:
                parents[str(node)] = current

                open.append(node)
                heapq.heappush(open_heap,(temp_f_score, node, (temp_g_score, heuristic(node), a + 1)))

                # used for reconstruct_path1 but ends with higher time complexity
                # static_heap.append((temp_f_score, node, (temp_g_score, heuristic(node), parent_index)))




"""
def reconstruct_path1(current, static_heap, info):
    total_path = [(info[0] + info[1], current, info)]

    while info[2] != -1:

        current = static_heap[info[2]]
        info = static_heap[info[2]][2]
        total_path.append(current)
    return total_path

"""


def reconstruct_path(parents, current):

    total_path = [current]

    while str(current) in parents.keys():
        current = parents[str(current)]
        total_path.append(current)

    return total_path


if __name__ == "__main__":
    puzzle = [4,3,8,5,1,6,7,2,0]

    # print(heuristic(puzzle))
    #print_succ(puzzle)
    # print(heuristic([1, 2, 3, 4, 5, 6, 7, 0, 8]))
    pq = []
    heapq.heappush(pq, (5, [1, 2, 3, 4, 5, 0, 6, 7, 8], (0, 5, -1)))
    #print(pq)

    fScore = {}
    fScore['a'] = 0

    #print(fScore)
    a = time.perf_counter()
    solve(puzzle)
    b = time.perf_counter()
    print(b - a)