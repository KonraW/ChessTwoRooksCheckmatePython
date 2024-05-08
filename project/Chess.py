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

def is_valid_move(x1, y1, x2, y2):
    # Sprawdzenie czy ruch jest dozwolony dla królowej
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return (dx == dy or x1 == x2 or y1 == y2)

def is_valid_position(x, y, obstacles):
    return (x, y) not in obstacles

def astar(start, goal, obstacles):
    start_x, start_y = ord(start[0]) - ord('a'), int(start[1]) - 1
    goal_x, goal_y = ord(goal[0]) - ord('a'), int(goal[1]) - 1

    open_list = []
    closed_list = []

    start_node = Node(start_x, start_y)
    goal_node = Node(goal_x, goal_y)

    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            path = []
            while current_node is not None:
                path.append((chr(current_node.x + ord('a')), current_node.y + 1))
                current_node = current_node.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.x + new_position[0], current_node.y + new_position[1])

            if node_position[0] < 0 or node_position[0] >= 8 or node_position[1] < 0 or node_position[1] >= 8:
                continue

            if not is_valid_move(current_node.x, current_node.y, node_position[0], node_position[1]):
                continue

            if not is_valid_position(node_position[0], node_position[1], obstacles):
                continue

            new_node = Node(node_position[0], node_position[1], current_node)

            children.append(new_node)

        for child in children:
            for closed_child in closed_list:
                if child.x == closed_child.x and child.y == closed_child.y:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.x - goal_node.x) ** 2) + ((child.y - goal_node.y) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child.x == open_node.x and child.y == open_node.y and child.g > open_node.g:
                    continue

            open_list.append(child)

    return None

# Przykładowe użycie:
start = "a1"
goal = "e8"
obstacles = [("a", 3), ("b", 4)]  # Przeszkody w postaci listy krotek (x, y)

droga = astar(start, goal, obstacles)
print(droga)



class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

def is_valid_move(x1, y1, x2, y2):
    # Sprawdzenie czy ruch jest dozwolony dla królowej
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return (dx == dy or x1 == x2 or y1 == y2)

def astar(start, goal):
    start_x, start_y = ord(start[0]) - ord('a'), int(start[1]) - 1
    goal_x, goal_y = ord(goal[0]) - ord('a'), int(goal[1]) - 1

    open_list = []
    closed_list = []

    start_node = Node(start_x, start_y)
    goal_node = Node(goal_x, goal_y)

    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node.x == goal_node.x and current_node.y == goal_node.y:
            path = []
            while current_node is not None:
                path.append((chr(current_node.x + ord('a')), current_node.y + 1))
                current_node = current_node.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.x + new_position[0], current_node.y + new_position[1])

            if node_position[0] < 0 or node_position[0] >= 8 or node_position[1] < 0 or node_position[1] >= 8:
                continue

            if not is_valid_move(current_node.x, current_node.y, node_position[0], node_position[1]):
                continue

            new_node = Node(node_position[0], node_position[1], current_node)

            children.append(new_node)

        for child in children:
            for closed_child in closed_list:
                if child.x == closed_child.x and child.y == closed_child.y:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.x - goal_node.x) ** 2) + ((child.y - goal_node.y) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child.x == open_node.x and child.y == open_node.y and child.g > open_node.g:
                    continue

            open_list.append(child)

    return None

# Przykładowe użycie:
start = "a1"
goal = "e8"
droga = astar(start, goal)
print(droga)





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





def white_king_to_opposite_corner(legal_moves):
    global black_king_last
    global white_king_last
    row_distance = (int(white_king_last[1]) - int(black_king_last[1]))
    column_distance = (ord(white_king_last[0]) - ord(black_king_last[0]))
    vector = [0, 0]
    if row_distance > 0:
        vector[0] = 1
    elif row_distance < 0:
        vector[0] = -1
    elif row_distance == 0:
        vector[0] = 0
    if column_distance > 0:
        vector[1] = 1
    elif column_distance < 0:
        vector[1] = -1
    elif column_distance == 0:
        vector[1] = 0

    return find_opposite_corner(vector)

    print(vector)
    return "a1a8"


# def is_rook_on_site(rook_2_last):
#     if rook_2_last[0] == "a" or rook_2_last[1] == "h" or rook_2_last == "a8" or rook_2_last == "h8":
#         return False
#     return True


def move_rook(rook1_danger, rook2_danger, legal_moves):
    print("halskdflasj")
    global rook_1_last
    global rook_2_last
    global white_king_last
    # if rook1_danger == 1 or rook2_danger == 1:

    # elif (rook_2_last+rook_1_last[0]+rook_2_last[1]) in legal_moves:
    #     return chess.Move.from_uci(rook_2_last+rook_1_last[0]+rook_2_last[1])
    # elif (rook_2_last+rook_2_last[0]+rook_1_last[1]) in legal_moves:
    #     return chess.Move.from_uci(rook_2_last+rook_2_last[0]+rook_1_last[1])
    # elif rook1_danger == 1:
    # else:
    if (black_king_block == 1):
        return rooks_to_opposite_site(2)

    if (rook_1_last[0] == rook_2_last[0] and rook_1_last[0] == white_king_last[0]) and not are_rooks_neighbours(
            rook_1_last, rook_2_last):
        return random_king_move(legal_moves, 0)
    elif (rook_1_last[1] == rook_2_last[1] and rook_1_last[1] == white_king_last[1]) and not are_rooks_neighbours(
            rook_1_last, rook_2_last):
        return random_king_move(legal_moves, 1)

    elif not are_rooks_in_same_column_or_row(rook_1_last, rook_2_last):
        if (rook_1_last + rook_1_last[0] + rook_2_last[1]) in legal_moves and white_king_last[0] != rook_1_last[0]:
            return rook_1_last + rook_1_last[0] + rook_2_last[1]
        elif (rook_1_last + rook_2_last[0] + rook_1_last[1]) in legal_moves and white_king_last[1] != rook_1_last[1]:
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
    elif are_rooks_neighbours(rook_1_last, rook_2_last) and not is_king_in_opposite_corner(white_king_last):
        return white_king_to_opposite_corner(legal_moves)
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
        if player_color == chess.BLACK:  # If it's black player's turn
            user_input = input("Enter your King move (e.g., 'f8'): ")
            if user_input:
                target_square = chess.parse_square(user_input)
                king_from_square = chess.parse_square(black_king_last)
                move = chess.Move(king_from_square, target_square)
                print(move)
                print(legal_moves)
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

white_king_last = "e1"
black_king_last = "e8"
rook_1_last = "a1"
rook_2_last = "h1"

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

while not board.is_game_over():
    if not board.turn:  # Black moves
        move_piece_randomly(board, label, rook_list_move, chess.BLACK)
    else:  # White moves
        move_piece_randomly(board, label, rook_list_move, chess.WHITE)
        # legal_moves = list(board.legal_moves)

    root.update()  # GUI update !!!!
    time.sleep(3)

# move_black_king_randomly(board, label)

root.mainloop()
