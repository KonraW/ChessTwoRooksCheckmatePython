import chess
import random
import time
import chess.svg
import cairosvg
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

def is_valid_move(start_x, start_y, end_x, end_y):
    # Check if the move is allowed for the queen
    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)
    return (dx == dy or start_x == end_x or start_y == end_y)

def is_valid_position(x, y, obstacles):
    # Check if the position is within the bounds of the chessboard
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    # Check if the position is obstructed by any obstacles
    for obstacle in obstacles:
        obstacle_x = ord(obstacle[0]) - ord('a')
        obstacle_y = int(obstacle[1]) - 1
        if x == obstacle_x and y == obstacle_y:
            return False
    return True

def astar(start, goal, obstacles):
    start_x, start_y = ord(start[0]) - ord('a'), int(start[1]) - 1
    goal_x, goal_y = ord(goal[0]) - ord('a'), int(goal[1]) - 1

    open_list = []
    closed_list = []

    start_node = Node(start_x, start_y)
    goal_node = Node(goal_x, goal_y)

    open_list.append(start_node)

    licznik=0
    while open_list:
        licznik+=1
        list_of_full_board = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"]
        if licznik>1000:
            return list_of_full_board
        current_node = min(open_list, key=lambda node: node.f)
        open_list.remove(current_node)
        closed_list.append(current_node)

        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            path = []
            while current_node is not None:
                path.append(chr(current_node.x + ord('a')) + str(current_node.y + 1))
                current_node = current_node.parent
            path = path[::-1]  # Remove the starting position below added UWAGA
            return path[1:]

        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x, new_y = current_node.x + dx, current_node.y + dy

            if not is_valid_move(current_node.x, current_node.y, new_x, new_y):
                continue

            if not is_valid_position(new_x, new_y, obstacles):
                continue

            new_node = Node(new_x, new_y, current_node)
            new_node.g = current_node.g + 1
            new_node.h = ((new_node.x - goal_node.x) ** 2) + ((new_node.y - goal_node.y) ** 2)
            new_node.f = new_node.g + new_node.h

            open_list.append(new_node)

    return None

# Example usage:
start = "a1"
goal = "e8"
obstacles = ["c3", "b8"]  # Obstacles in the form of a list of strings

path = astar(start, goal, obstacles)

print(path)





def update_board_image(board, label):
    svg_board = chess.svg.board(board, size=640, coordinates=False)
    render_svg = cairosvg.svg2png(bytestring=svg_board)
    image = Image.open(BytesIO(render_svg))
    photo_image = ImageTk.PhotoImage(image)
    label.config(image=photo_image)
    label.image = photo_image


def is_king_in_opposite_corner(white_king_last):
    if white_king_last == "a8" or white_king_last == "h8" or white_king_last == "h1" or white_king_last == "a1":
        return True
    return False


def are_rooks_in_same_column_or_row(rook_1_last, rook_2_last):
    if rook_1_last[0] == rook_2_last[0] or rook_1_last[1] == rook_2_last[1]:
        return True
    return False


def are_rooks_neighbours(rook_1_last, rook_2_last):
    if chess.square_distance(chess.parse_square(rook_1_last), chess.parse_square(rook_2_last)) == 1:
        return True
    return False


black_king_block = 0

block_direction = 0


def rooks_to_opposite_site(param):
    global rook_1_last
    global rook_2_last
    global block_direction
    global black_king_block
    if param == 1:
        if column_or_row(rook_1_last, rook_2_last):
            if rook_1_last[0] == "a":
                block_direction = "h"
                return rook_1_last + "h" + rook_1_last[1]
            else:
                block_direction = "a"
                return rook_1_last + "a" + rook_1_last[1]
        else:
            if rook_1_last[1] == "1":
                block_direction = 8
                return rook_1_last + rook_1_last[0] + "8"
            else:
                block_direction = 1
                return rook_1_last + rook_1_last[0] + "1"
    if param == 2:
        black_king_block = 0
        if block_direction == 1:
            return rook_2_last + rook_2_last[0] + "1"
        elif block_direction == 8:
            return rook_2_last + rook_2_last[0] + "8"
        elif block_direction == "a":
            return rook_2_last + "a" + rook_2_last[1]
        elif block_direction == "h":
            return rook_2_last + "h" + rook_2_last[1]
    return "a1a8"


def random_king_move(legal_moves, index):
    for move in legal_moves:
        # print(move.uci()[index])
        # print(white_king_last[index])
        if move.from_square == chess.parse_square(white_king_last) and white_king_last[index] != move.uci()[index + 2]:
            return move.uci()
    global black_king_block
    black_king_block = 1
    return rooks_to_opposite_site(1)


def column_or_row(rook_1_last, rook_2_last):
    if rook_1_last[0] == rook_2_last[0]:
        return True
    return False


def find_opposite_corner(vector):
    global rook_1_last
    global rook_2_last
    rook_positions = [rook_1_last, rook_2_last]
    if vector[0] == -1:
        if vector[1] == 1 and "h1" not in rook_positions:
            return "h1"
        else:
            return "a1"
    else:
        if vector[1] == -1 and "h8" not in rook_positions:
            return "h8"
        else:
            return "a8"


king_path = []
is_king_path = 0
king_ooo = []
bad_corner = False


def black_king_neighbours():
    global black_king_last
    global rook_1_last
    global rook_2_last
    black_king_list = [black_king_last, rook_1_last, rook_2_last]
    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        new_x, new_y = ord(black_king_last[0]) - ord('a') + dx, int(black_king_last[1]) - 1 + dy
        if 0 <= new_x <= 7 and 0 <= new_y <= 7:
            black_king_list.append(chr(new_x + ord('a')) + str(new_y + 1))


    # print(black_king_list)
    # joined = ""

    # for i in black_king_list:
    #     joined += i
    #return every neighbour of black king in one return
    print(black_king_list)
    return black_king_list


def white_king_to_opposite_corner(legal_moves):
    global black_king_last
    global white_king_last
    global king_path
    global is_king_path
    global king_ooo
    global bad_corner

    a1_white = astar(white_king_last, "a1", [black_king_last])
    a8_white = astar(white_king_last, "a8", [black_king_last])
    h1_white = astar(white_king_last, "h1", [black_king_last])
    h8_white = astar(white_king_last, "h8", [black_king_last])
    a1_black = astar(black_king_last, "a1", [white_king_last])
    a8_black = astar(black_king_last, "a8", [white_king_last])
    h1_black = astar(black_king_last, "h1", [white_king_last])
    h8_black = astar(black_king_last, "h8", [white_king_last])
    if len(a1_white) - 2 < len(a1_black):
        king_path = astar(white_king_last, "b2", [black_king_last])
        king_path.append("a1")
        if rook_1_last != "a1" and rook_2_last != "a1":
            king_path = astar(white_king_last, "a1", black_king_neighbours())
            black_king_path = astar(black_king_last, "a1", [white_king_last, rook_1_last, rook_2_last])
            is_king_path = 1
            # print(rook_1_last, rook_2_last)
            if len(king_path)<=len(black_king_path):
                print(king_path)
                if chess.Move.from_uci(white_king_last + king_path[0]) in legal_moves:
                    return white_king_last + king_path.pop(0)
                # else:
                #     return move_to_other_corner(legal_moves)
    if len(a8_white) - 2 < len(a8_black):
        king_path = astar(white_king_last, "b7", [black_king_last])
        king_path.append("a8")
        if rook_1_last != "a8" and rook_2_last != "a8":
            king_path = astar(white_king_last, "a8", black_king_neighbours())
            black_king_path = astar(black_king_last, "a8", [white_king_last, rook_1_last, rook_2_last])
            is_king_path = 1
            # print(rook_1_last, rook_2_last)
            print(king_path)
            if len(king_path)<=len(black_king_path):
                if chess.Move.from_uci(white_king_last + king_path[0]) in legal_moves:
                    return white_king_last + king_path.pop(0) #.pop(0)
                # else:
                #     return move_to_other_corner(legal_moves)
    print(h1_white, h1_black)
    if len(h1_white) - 2 < len(h1_black):
        king_path = astar(white_king_last, "g2", [black_king_last])
        king_path.append("h1")
        if rook_1_last != "h1" and rook_2_last != "h1":
            king_path = astar(white_king_last, "h1", black_king_neighbours())
            black_king_path = astar(black_king_last, "h1", [white_king_last, rook_1_last, rook_2_last])
            is_king_path = 1
            # print(rook_1_last, rook_2_last)
            print(king_path)
            if len(king_path)<=len(black_king_path):
                if chess.Move.from_uci(white_king_last + king_path[0]) in legal_moves:
                    return white_king_last + king_path.pop(0)
                # else:
                #     return move_to_other_corner(legal_moves)
    if len(h8_white) - 2 < len(h8_black):
        king_path = astar(white_king_last, "g7", [black_king_last])
        king_path.append("h8")
        if rook_1_last != "h8" and rook_2_last != "h8":
            king_path = astar(white_king_last, "h8", black_king_neighbours())
            black_king_path = astar(black_king_last, "h8", [white_king_last, rook_1_last, rook_2_last])
            is_king_path = 1
            # print(rook_1_last, rook_2_last)
            print(king_path)
            if len(king_path)<=len(black_king_path):
                if chess.Move.from_uci(white_king_last + king_path[0]) in legal_moves:
                    return white_king_last + king_path.pop(0)
                # else:
                #     return move_to_other_corner(legal_moves)

    # if len(king_path) == 1:
    is_king_path = 2
    bad_corner = True
    if column_or_row(rook_1_last, rook_2_last):
        # king_ooo=[]
        # for i in len(1, king_path):
        #     if len(king_ooo)>i:
        #         king_ooo.append(king_path[i] + king_path[i+1])
        # king_ooo = [king_path[-1] + king_path[-2][0]+king_path[-1][1], king_path[-2]+king_path[-1]]
        # king_path.pop(0)
        # return king_path[-1] + white_king_last[0] + king_path[-1][1]
        if len(king_path) > 1:
            king_ooo = [king_path[-1] + king_path[-2][0] + king_path[-1][1], king_path[-2] + king_path[-1]]
            print(king_path)
            king_path = king_path[:-1]
            if chess.Move.from_uci(white_king_last + king_path[0]) in legal_moves:
                return white_king_last + king_path.pop(0)
            else:
                return move_to_other_corner(legal_moves)
        else:
            king_ooo = [king_path[-1] + white_king_last[0] + king_path[-1][1], white_king_last + king_path[-1]]
            king_path.pop(0)
            print(king_path)

            return king_ooo.pop(0)
    else:
        # print(king_path)
        # king_ooo = [king_path[-1] + king_path[0], king_path[-1] + white_king_last[0] + king_path[-1][1]]
        # return white_king_last + king_path.pop(0)
        if len(king_path) > 1:
            king_ooo = [king_path[-1] + king_path[-1][0] + king_path[-2][1], king_path[-2] + king_path[-1]]
            print(king_path)
            king_path = king_path[:-1]
            if chess.Move.from_uci(white_king_last + king_path[0]) in legal_moves:
                return white_king_last + king_path.pop(0)
            else:
                return move_to_other_corner(legal_moves)
        else:
            king_ooo = [king_path[-1] + king_path[-1][0] + white_king_last[1], white_king_last + king_path[-1]]
            king_path.pop(0)
            print(king_path)
            return king_ooo.pop(0)

    # is_king_path = 3
    # king_path = astar(white_king_last, king_path[-2], [black_king_last, rook_1_last, rook_2_last])
    # return king_path.pop(0)

    # if rook_1_last != "a1" and rook_2_last != "a1":
    #     a1 = astar(white_king_last, "a1", [black_king_last, rook_1_last, rook_2_last])
    # else:
    #     if column_or_row(rook_1_last, rook_2_last):
    #         king_path = a1
    #         is_king_path = 2
    #         a1 = a1[1:]
    #         return a1[0]
    #
    # if rook_1_last != "a8" and rook_2_last != "a8":
    #     a8 = astar(white_king_last, "a8", [black_king_last, rook_1_last, rook_2_last])
    # if rook_1_last != "h1" and rook_2_last != "h1":
    #     h1 = astar(white_king_last, "h1", [black_king_last, rook_1_last, rook_2_last])
    # if rook_1_last != "h8" and rook_2_last != "h8":
    #     h8 = astar(white_king_last, "h8", [black_king_last, rook_1_last, rook_2_last])
    # row_distance = (int(white_king_last[1]) - int(black_king_last[1]))
    # column_distance = (ord(white_king_last[0]) - ord(black_king_last[0]))
    # vector = [0, 0]
    # if row_distance > 0:
    #     vector[0] = 1
    # elif row_distance < 0:
    #     vector[0] = -1
    # elif row_distance == 0:
    #     vector[0] = 0
    # if column_distance > 0:
    #     vector[1] = 1
    # elif column_distance < 0:
    #     vector[1] = -1
    # elif column_distance == 0:
    #     vector[1] = 0
    #
    # return find_opposite_corner(vector)
    #
    # print(vector)
    # return "a1a8"


# def is_rook_on_site(rook_2_last):
#     if rook_2_last[0] == "a" or rook_2_last[1] == "h" or rook_2_last == "a8" or rook_2_last == "h8":
#         return False
#     return True

penultimate = ""
penultimate2 = ""
def start_checkmate(legal_moves):
    global rows
    global columns
    global attack_column_or_row
    global attack_direction
    global black_king_last
    global white_king_last
    global rook_1_last
    global rook_2_last
    # global penultimate
    global penultimate2
    "halo?"
    print(chess.square_distance(chess.parse_square(black_king_last), chess.parse_square(rook_1_last)))
    print(chess.square_distance(chess.parse_square(black_king_last), chess.parse_square(rook_2_last)))
    if chess.square_distance(chess.parse_square(black_king_last), chess.parse_square(rook_1_last)) == 1:
        if attack_column_or_row == 1:
            tmp_list1 = ["a", "b", "c"]
            tmp_list2 = ["h", "g", "f"]
            if rook_1_last[0] in tmp_list1:
                for i in tmp_list2:
                    if rook_2_last[0] != i and white_king_last[0] != i and not under_attack3(rook_1_last, i) and rook_1_last + i + rook_1_last[1]!=penultimate2:
                        return rook_1_last + i + rook_1_last[1]
            elif rook_1_last[0] in tmp_list2:
                for i in tmp_list1:
                    if rook_2_last[0] != i and white_king_last[0] != i and not under_attack3(rook_1_last, i) and rook_1_last + i + rook_1_last[1]!=penultimate2:
                        return rook_1_last + i + rook_1_last[1]
            else:
                for i in ["b", "g"]:
                    if rook_2_last[0] != i and not under_attack3(rook_1_last, i) and rook_1_last + i + rook_1_last[1]!=penultimate2:
                        return rook_1_last + i + rook_1_last[1]
        else:
            tmp_list1 = ["1", "2", "3"]
            tmp_list2 = ["8", "7", "6"]
            if rook_1_last[1] in tmp_list1:
                for i in tmp_list2:
                    if rook_2_last[1] != i and white_king_last[1] != i and not under_attack3(rook_1_last, i) and rook_1_last + rook_1_last[0] + i!=penultimate2:
                        return rook_1_last + rook_1_last[0] + i
            elif rook_1_last[1] in tmp_list2:
                for i in tmp_list1:
                    if rook_2_last[1] != i and white_king_last[1] != i and not under_attack3(rook_1_last, i) and rook_1_last + rook_1_last[0] + i!=penultimate2:
                        return rook_1_last + rook_1_last[0] + i
            else:
                for i in ["2", "7"]:
                    if rook_2_last[1] != i and not under_attack3(rook_1_last, i) and rook_1_last + rook_1_last[0] + i!=penultimate2:
                        return rook_1_last + rook_1_last[0] + i
        # for row in rows:
        #     if not under_attack(rook_1_last, rook_2_last, row):
        #         if attack_column_or_row == 1:
        #             return rook_1_last + rook_1_last[0] + row
        #         else:
        #             return rook_1_last + row + rook_1_last[1]
    if chess.square_distance(chess.parse_square(black_king_last), chess.parse_square(rook_2_last)) == 1:
        if attack_column_or_row == 1:
            tmp_list1 = ["a", "b", "c"]
            tmp_list2 = ["h", "g", "f"]
            if rook_2_last[0] in tmp_list1:
                for i in tmp_list2:
                    if rook_1_last[0] != i and white_king_last[0] != i and not under_attack3(rook_2_last, i) and rook_2_last + i + rook_2_last[1]!=penultimate2:
                        return rook_2_last + i + rook_2_last[1]
            elif rook_2_last[0] in tmp_list2:
                for i in tmp_list1:
                    if rook_1_last[0] != i and white_king_last[0] != i and not under_attack3(rook_2_last, i) and rook_2_last + i + rook_2_last[1]!=penultimate2:
                        return rook_2_last + i + rook_2_last[1]
            else:
                for i in ["b", "g"]:
                    if rook_1_last[0] != i and not under_attack3(rook_2_last, i) and rook_2_last + i + rook_2_last[1]!=penultimate2:
                        return rook_2_last + i + rook_2_last[1]
        else:
            tmp_list1 = ["1", "2", "3"]
            tmp_list2 = ["8", "7", "6"]
            if rook_2_last[1] in tmp_list1:
                for i in tmp_list2:
                    if rook_1_last[1] != i and white_king_last[1] != i and not under_attack3(rook_2_last, i) and rook_2_last + rook_2_last[0] + i!=penultimate2:
                        return rook_2_last + rook_2_last[0] + i
            elif rook_2_last[1] in tmp_list2:
                for i in tmp_list1:
                    if rook_1_last[1] != i and white_king_last[1] != i and not under_attack3(rook_2_last, i) and rook_2_last + rook_2_last[0] + i!=penultimate2:
                        return rook_2_last + rook_2_last[0] + i
            else:
                for i in ["2", "7"]:
                    if rook_1_last[1] != i and not under_attack3(rook_2_last, i) and rook_2_last + rook_2_last[0] + i!=penultimate2:
                        return rook_2_last + rook_2_last[0] + i
        # for row in rows:
        #     if not under_attack(rook_1_last, rook_2_last, row):
        #         if attack_column_or_row == 1:
        #             return rook_2_last + rook_2_last[0] + row
        #         else:
        #             return rook_2_last + row + rook_2_last[1]
    if attack_direction == 0:
        if attack_column_or_row == 1:
            if rook_1_last[1] < rook_2_last[1]:
                if chess.square_distance(chess.parse_square(rook_1_last[0] + str(int(rook_2_last[1]) + 1)),
                                         chess.parse_square(black_king_last)) == 1 or rook_1_last[0] + str(int(rook_2_last[1]) + 1)==white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[0] and row != \
                                rook_2_last[0] and rook_1_last + row + rook_1_last[1]!=penultimate2:
                            # if attack_column_or_row == 0:
                            #     return rook_1_last + rook_1_last[0] + row
                            return rook_1_last + row + rook_1_last[1]

                return rook_1_last + rook_1_last[0] + str(int(rook_2_last[1]) + 1)
            else:
                if chess.square_distance(chess.parse_square(rook_2_last[0] + str(int(rook_1_last[1]) + 1)),
                                         chess.parse_square(black_king_last)) == 1 or rook_2_last[0] + str(int(rook_1_last[1]) + 1)==white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[0] and row != \
                                rook_2_last[0] and rook_2_last + row + rook_2_last[1]!=penultimate2:
                            # if attack_column_or_row == 0:
                            #     return rook_2_last + rook_2_last[0] + row
                            return rook_2_last + row + rook_2_last[1]
                return rook_2_last + rook_2_last[0] + str(int(rook_1_last[1]) + 1)
        else:
            if rook_1_last[0] < rook_2_last[0]:
                if chess.square_distance(chess.parse_square(chr(ord(rook_2_last[0]) + 1) + rook_1_last[1]),
                                         chess.parse_square(black_king_last)) == 1 or  chr(ord(rook_2_last[0]) + 1) + rook_1_last[1]==white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[1] and row != \
                                rook_2_last[1] and rook_1_last + row + rook_1_last[1]!=penultimate2:
                            # if attack_column_or_row == 0:
                            return rook_1_last + rook_1_last[0] + row
                        # return rook_1_last + row + rook_1_last[1]
                return rook_1_last + chr(ord(rook_2_last[0]) + 1) + rook_1_last[1]
            else:
                if chess.square_distance(chess.parse_square(chr(ord(rook_1_last[0]) + 1) + rook_2_last[1]),
                                         chess.parse_square(
                                             black_king_last)) == 1 or rook_2_last + chr(ord(rook_1_last[0]) + 1) + rook_2_last[1]==white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[1] and row != \
                                rook_2_last[1] and rook_2_last + row + rook_2_last[1]!=penultimate2:
                            # if attack_column_or_row == 1:
                            return rook_2_last + rook_2_last[0] + row
                        # return rook_2_last + row + rook_2_last[1]
                return rook_2_last + chr(ord(rook_1_last[0]) + 1) + rook_2_last[1]
    else:
        if attack_column_or_row == 1:
            if rook_1_last[1] > rook_2_last[1]:
                if chess.square_distance(chess.parse_square(rook_1_last[0] + str(int(rook_2_last[1]) - 1)),
                                         chess.parse_square(black_king_last)) == 1 or rook_1_last[0] + str(int(rook_2_last[1]) - 1)==white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[0] and row != \
                                rook_2_last[0] and rook_1_last + row + rook_1_last[1]!=penultimate2:
                            # if attack_column_or_row == 0:
                            return rook_1_last  + row+ rook_1_last[1]
                            # return rook_1_last + row + rook_1_last[1]
                return rook_1_last + rook_1_last[0] + str(int(rook_2_last[1]) - 1)
            else:
                if chess.square_distance(chess.parse_square(rook_2_last[0] + str(int(rook_1_last[1]) - 1)),
                                         chess.parse_square(black_king_last)) == 1 or rook_2_last[0] + str(int(rook_1_last[1]) - 1)==white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[0] and row != \
                                rook_2_last[0] and rook_2_last + row + rook_2_last[1]!=penultimate2:
                            # if attack_column_or_row == 0:
                            return rook_2_last + row + rook_2_last[1]
                            # return rook_2_last + row + rook_2_last[1]
                return rook_2_last + rook_2_last[0] + str(int(rook_1_last[1]) - 1)
        else:
            if rook_1_last[0] > rook_2_last[0]:
                if chess.square_distance(chess.parse_square(chr(ord(rook_2_last[0]) - 1) + rook_1_last[1]),
                                         chess.parse_square(black_king_last)) == 1 or  chr(ord(rook_2_last[0]) - 1) + rook_1_last[1] == white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[1] and row != \
                                rook_2_last[1] and rook_1_last + row + rook_1_last[1]!=penultimate2:
                            # if attack_column_or_row == 0:
                            return rook_1_last + rook_1_last[0] + row
                            # return rook_1_last + row + rook_1_last[1]
                return rook_1_last + chr(ord(rook_2_last[0]) - 1) + rook_1_last[1]
            else:
                if chess.square_distance(chess.parse_square(chr(ord(rook_1_last[0]) - 1) + rook_2_last[1]),
                                         chess.parse_square(black_king_last)) == 1 or  chr(ord(rook_1_last[0]) - 1) + rook_2_last[1] == white_king_last:
                    for row in rows:
                        if not under_attack2(rook_1_last, rook_2_last, row) and row != rook_1_last[1] and row != \
                                rook_2_last[1] and rook_2_last + row + rook_2_last[1]!=penultimate2:
                            # if attack_column_or_row == 1:
                            return rook_2_last + rook_2_last[0] + row
                            # return rook_2_last + row + rook_2_last[1]
                return rook_2_last + chr(ord(rook_1_last[0]) - 1) + rook_2_last[1]


is_start_checkmate = False
rows = []
columns = []
attack_column_or_row = 0
attack_direction = 0
is_start_king_move = False


def under_attack(rook_1_last, rook_2_last, row):
    global attack_column_or_row
    if attack_column_or_row == 0:
        if chess.square_distance(chess.parse_square(row + rook_1_last[1]), chess.parse_square(black_king_last)) == 1:
            return True
        if chess.square_distance(chess.parse_square(row + rook_2_last[1]), chess.parse_square(black_king_last)) == 1:
            return True
    else:
        if chess.square_distance(chess.parse_square(rook_1_last[0] + row), chess.parse_square(black_king_last)) == 1:
            return True
        if chess.square_distance(chess.parse_square(rook_2_last[0] + row), chess.parse_square(black_king_last)) == 1:
            return True


def under_attack2(rook_1_last, rook_2_last, row):
    global attack_column_or_row
    if attack_column_or_row == 1:
        if chess.square_distance(chess.parse_square(row + rook_1_last[1]), chess.parse_square(black_king_last)) == 1:
            return True
        if chess.square_distance(chess.parse_square(row + rook_2_last[1]), chess.parse_square(black_king_last)) == 1:
            return True
    else:
        if chess.square_distance(chess.parse_square(rook_1_last[0] + row), chess.parse_square(black_king_last)) == 1:
            return True
        if chess.square_distance(chess.parse_square(rook_2_last[0] + row), chess.parse_square(black_king_last)) == 1:
            return True

def under_attack3(rook_last, row):
    global attack_column_or_row
    if attack_column_or_row == 1:
        if chess.square_distance(chess.parse_square(row + rook_last[1]), chess.parse_square(black_king_last)) == 1:
            return True
    else:
        if chess.square_distance(chess.parse_square(rook_last[0] + row), chess.parse_square(black_king_last)) == 1:
            return True

# def move_to_other_corner(legal_moves):
#     global white_king_last
#     global king_path
#     global is_king_path
#     if (white_king_last == "a2" or white_king_last == "h7") and chess.square_distance(chess.parse_square(king_path[0]), chess.parse_square(black_king_last)) == 1:
#         king_path = astar(white_king_last, "a8", [black_king_last])
#     elif (white_king_last == "h2" or white_king_last == "b8") and chess.square_distance(chess.parse_square(king_path[0]), chess.parse_square(black_king_last)) == 1:
#         king_path = astar(white_king_last, "h8", [black_king_last])
#     elif (white_king_last == "a7" or white_king_last == "g1") and chess.square_distance(chess.parse_square(king_path[0]), chess.parse_square(black_king_last)) == 1:
#         king_path = astar(white_king_last, "a1", [black_king_last])
#     elif (white_king_last == "h7" or white_king_last == "b1") and chess.square_distance(chess.parse_square(king_path[0]), chess.parse_square(black_king_last)) == 1:
#         king_path = astar(white_king_last, "h1", [black_king_last])
#     is_king_path = 1
#     return white_king_last + king_path.pop(0)

def move_to_other_corner(legal_moves):
    global white_king_last
    global king_path
    global is_king_path
    # return white_king_to_opposite_corner(legal_moves)

    # if white_king_last == "a2" or white_king_last == "h7":
    #     king_path = astar(white_king_last, "a8", [black_king_last])
    # elif white_king_last == "h2" or white_king_last == "b8":
    #     king_path = astar(white_king_last, "h8", [black_king_last])
    # elif white_king_last == "a7" or white_king_last == "g1":
    #     king_path = astar(white_king_last, "a1", [black_king_last])
    # elif white_king_last == "h7" or white_king_last == "b1":
    #     king_path = astar(white_king_last, "h1", [black_king_last])
    # is_king_path = 1
    return white_king_last + king_path.pop(0)


def move_rook(rook1_danger, rook2_danger, legal_moves):
    # print("halo?")
    global rook_1_last
    global rook_2_last
    global white_king_last
    global king_path
    global is_king_path
    global black_king_block
    global is_start_checkmate
    global attack_column_or_row
    global rows
    global king_ooo
    global attack_direction
    global is_start_king_move
    global bad_corner
    global columns
    # if rook1_danger == 1 or rook2_danger == 1:

    # elif (rook_2_last+rook_1_last[0]+rook_2_last[1]) in legal_moves:
    #     return chess.Move.from_uci(rook_2_last+rook_1_last[0]+rook_2_last[1])
    # elif (rook_2_last+rook_2_last[0]+rook_1_last[1]) in legal_moves:
    #     return chess.Move.from_uci(rook_2_last+rook_2_last[0]+rook_1_last[1])
    # elif rook1_danger == 1:
    # else:
    if is_king_path == 1:
        if king_path:
            square = king_path[0]
            if len(king_path) == 1:
                is_king_path = 0
                king_path = []
                return white_king_last + square
            king_path = king_path[1:]
            if chess.Move.from_uci(white_king_last + square) in legal_moves:
                return white_king_last + square
            else:
                # return move_to_other_corner(legal_moves)
                return white_king_to_opposite_corner(legal_moves)
        else:
            is_king_path = 0
    elif is_king_path == 2:
        if king_path:
            print(king_path, "path")
            square = king_path[0]
            if len(king_path) == 1:
                is_king_path = 0
                king_path = []
                return white_king_last + square
            king_path = king_path[1:]
            #if white_king_last+square in legal_moves:
            if chess.Move.from_uci(white_king_last + square) in legal_moves:
                return white_king_last + square
            else:
                # return move_to_other_corner(legal_moves)
                return white_king_to_opposite_corner(legal_moves)
        else:
            print(king_ooo, "oooo")
            if len(king_ooo) == 1:
                is_king_path = 0
            return king_ooo.pop(0)

    if black_king_block == 1:
        return rooks_to_opposite_site(2)
    if not is_start_king_move:
        if (rook_1_last[0] == rook_2_last[0] and rook_1_last[0] == white_king_last[0]) and not are_rooks_neighbours(
                rook_1_last, rook_2_last):
            return random_king_move(legal_moves, 0)
        elif (rook_1_last[1] == rook_2_last[1] and rook_1_last[1] == white_king_last[1]) and not are_rooks_neighbours(
                rook_1_last, rook_2_last):
            return random_king_move(legal_moves, 1)

        elif not are_rooks_in_same_column_or_row(rook_1_last, rook_2_last):
            # print(legal_moves, rook_1_last, rook_2_last, white_king_last)
            # move = chess.Move.from_uci("a1a8")
            # if (chess.Move.from_uci(rook_1_last + rook_1_last[0] + rook_2_last[1])) in legal_moves:
            #     print("halo")
            if (chess.Move.from_uci(rook_1_last + rook_1_last[0] + rook_2_last[1])) in legal_moves and white_king_last[
                0] != rook_1_last[0]:
                return rook_1_last + rook_1_last[0] + rook_2_last[1]
            elif (chess.Move.from_uci(rook_1_last + rook_2_last[0] + rook_1_last[1])) in legal_moves and \
                    white_king_last[1] != rook_1_last[1]:
                return rook_1_last + rook_2_last[0] + rook_1_last[1]
            else:
                return print("No legal moves available.")
        elif not are_rooks_neighbours(rook_1_last, rook_2_last):  # or is_rook_on_site(rook_2_last):

            if column_or_row(rook_1_last, rook_2_last):
                # if is_rook_on_site(rook_2_last):
                #     if rook_2_last + rook_2_last[0]+"1" in legal_moves:
                #         return rook_2_last + rook_2_last[0] + "1"
                #     else:
                #         return rook_2_last + rook_2_last[0] + "8"
                if rook_1_last[1] < rook_2_last[1]:
                    return rook_1_last + rook_1_last[0] + str(int(rook_2_last[1]) - 1)
                else:
                    return rook_1_last + rook_1_last[0] + str(int(rook_2_last[1]) + 1)
            else:
                # if is_rook_on_site(rook_2_last):
                #     if rook_2_last + "a" + rook_2_last[1] in legal_moves:
                #         return rook_2_last + "a" + rook_2_last[1]
                #     else:
                #         return rook_2_last + "h" + rook_2_last[1]
                if rook_1_last[0] < rook_2_last[0]:
                    return rook_1_last + chr(ord(rook_2_last[0]) - 1) + rook_1_last[1]
                else:
                    return rook_1_last + chr(ord(rook_2_last[0]) + 1) + rook_1_last[1]
        if not column_or_row(rook_1_last, rook_2_last):
            attack_column_or_row = 1
        if are_rooks_neighbours(rook_1_last, rook_2_last) and not is_king_in_opposite_corner(white_king_last):
            is_start_king_move = True
            return white_king_to_opposite_corner(legal_moves)
    if not is_start_checkmate:
        is_start_checkmate = True
        if attack_column_or_row == 1:
            if black_king_last[1] < rook_1_last[1]:
                attack_direction = 1
            if white_king_last[1] == 1:
                columns = ["2", "3", "8", "7"]
            else:
                columns = ["1", "2", "7", "6"]
            if white_king_last[0] == "a":
                rows = ["b", "c", "h", "g"]
            else:
                rows = ["a", "b", "g", "f"]
            if not bad_corner:
                bad_corner = True
                # for row in rows:
                #     if not under_attack(rook_1_last, rook_2_last, row):
                #         if rook_1_last[1] > rook_2_last[1]:
                #             if attack_direction == 1:
                #                 return rook_1_last + row + rook_1_last[1]
                #             else:
                #                 return rook_2_last + row + rook_2_last[1]
                #         else:
                #             if attack_direction == 1:
                #                 return rook_2_last + row + rook_2_last[1]
                #             else:
                #                 return rook_1_last + row + rook_1_last[1]
        else:
            if black_king_last[0] < rook_1_last[0]:
                attack_direction = 1
            if white_king_last[0] == "a":
                columns = ["b", "c", "h", "g"]
            else:
                columns = ["a", "b", "g", "f"]
            if white_king_last[1] == "1":
                rows = ["2", "3", "8", "7"]
            else:
                rows = ["1", "2", "7", "6"]
            if not bad_corner:
                bad_corner = True
                # for row in rows:
                #     if not under_attack(rook_1_last, rook_2_last, row):
                #         if rook_1_last[0] > rook_2_last[0]:
                #             if attack_direction == 1:
                #                 return rook_1_last + rook_1_last[0] + row
                #             else:
                #                 return rook_2_last + rook_2_last[0] + row
                #         else:
                #             if attack_direction == 1:
                #                 return rook_2_last + rook_2_last[0] + row
                #             else:
                #                 return rook_1_last + rook_1_last[0] + row
    if bad_corner:
        return start_checkmate(legal_moves)
    return "a1a8"
    # if not is_king_in_opposite_corner(white_king_last):
    #     if ()
    #
    # global white_king_last
    # if rook_last[0] == white_king_last[0]:
    #     return chess.Move.from_uci("a1a8")


def what_piece_is_moved(move):
    global white_king_last
    global black_king_last
    global rook_1_last
    global rook_2_last
    if move.from_square == chess.parse_square(white_king_last):
        return "white_king"
    elif move.from_square == chess.parse_square(black_king_last):
        return "black_king"
    elif move.from_square == chess.parse_square(rook_1_last):
        return "rook_1"
    elif move.from_square == chess.parse_square(rook_2_last):
        return "rook_2"
    return None


def update_global_last_position(new_position):
    global white_king_last
    global black_king_last
    global rook_1_last
    global rook_2_last
    global penultimate
    global penultimate2
    penultimate2 = penultimate
    penultimate = str(new_position)
    piece = what_piece_is_moved(new_position)
    new_position = new_position.uci()[2:4]
    if piece == "white_king":
        white_king_last = new_position
    elif piece == "black_king":
        black_king_last = new_position
    elif piece == "rook_1":
        rook_1_last = new_position
    elif piece == "rook_2":
        rook_2_last = new_position


def stairs_move(legal_moves):
    global white_king_last
    global black_king_last
    global rook_1_last
    global rook_2_last
    black_king_square = chess.parse_square(black_king_last)
    white_king_square = chess.parse_square(white_king_last)
    rook_1_square = chess.parse_square(rook_1_last)
    rook_2_square = chess.parse_square(rook_2_last)
    rook1_danger = 0
    rook2_danger = 0
    # if chess.square_distance(black_king_square, rook_1_square) == 1 and rook_1_last[0]!=rook_2_last[0] and rook_1_last[1]!=rook_2_last[1]:
    #     rook1_danger = 1
    # if chess.square_distance(black_king_square, rook_2_square) == 1 and rook_1_last[0]!=rook_2_last[0] and rook_1_last[1]!=rook_2_last[1]:
    #     rook2_danger = 1
    return move_rook(rook1_danger, rook2_danger, legal_moves)


def move_piece_randomly(board, label, rook_list_move, player_color):
    global white_king_last
    global black_king_last
    global rook_1_last
    global rook_2_last
    if not board.is_game_over():
        legal_moves = list(board.legal_moves)
        random_move = random.choice(legal_moves)
        # print(legal_moves)
        if player_color == chess.BLACK:  # If it's black player's turn
            user_input = input("Enter your King move (e.g., 'f8'): ")
            if user_input:
                target_square = chess.parse_square(user_input)
                king_from_square = chess.parse_square(black_king_last)
                move = chess.Move(king_from_square, target_square)
                print(move)
                # print(legal_moves)
                if move in legal_moves:
                    random_move = move
            black_king_last = chess.square_name(random_move.to_square)
        else:
            random_move = chess.Move.from_uci(stairs_move(legal_moves))
            update_global_last_position(random_move)

            # elif legal_moves:
            #     random_move = random.choice(legal_moves)
            # else:
            #     print("No legal moves available.")
            #     return

        board.push(random_move)
        print(random_move)
        update_board_image(board, label)  # Update the board image after the move


rook_list_move = ["a1a8", "a8d8"]

board = chess.Board()
board.clear()

white_king_last = "c8"
black_king_last = "c6"
rook_1_last = "b8"
rook_2_last = "d8"

board.set_piece_at(chess.parse_square(white_king_last), chess.Piece(chess.KING, chess.WHITE))
board.set_piece_at(chess.parse_square(black_king_last), chess.Piece(chess.KING, chess.BLACK))
board.set_piece_at(chess.parse_square(rook_1_last), chess.Piece(chess.ROOK, chess.WHITE))
board.set_piece_at(chess.parse_square(rook_2_last), chess.Piece(chess.ROOK, chess.WHITE))

root = tk.Tk()
root.title("2 rooks vs king")

svg_board = chess.svg.board(board, size=640, coordinates=False)
render_svg = cairosvg.svg2png(bytestring=svg_board)
image = Image.open(BytesIO(render_svg))
photo_image = ImageTk.PhotoImage(image)

label = tk.Label(root, image=photo_image)
label.pack()

# update_board_image(board, label)

while not board.is_game_over():
    if not board.turn:  # Black moves
        move_piece_randomly(board, label, rook_list_move, chess.BLACK)
    else:  # White moves
        move_piece_randomly(board, label, rook_list_move, chess.WHITE)
        # legal_moves = list(board.legal_moves)

    root.update()  # GUI update !!!!
    time.sleep(.1)

print("Game Over")
# move_black_king_randomly(board, label)

root.mainloop()
