import chess
import random
import time
import chess.svg
import cairosvg
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO


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

def move_rook(rook1_danger, rook2_danger, legal_moves):
    global rock_1_last
    global rock_2_last
    global white_king_last
    if rook1_danger == 1 or rook2_danger == 1:
        if (rock_1_last+rock_1_last[0]+rock_2_last[1]) in legal_moves and white_king_last[0] != rock_1_last[0]:
            return chess.Move.from_uci(rock_1_last+rock_1_last[0]+rock_2_last[1])
        elif (rock_1_last+rock_2_last[0]+rock_1_last[1]) in legal_moves and white_king_last[1] != rock_1_last[1]:
            return chess.Move.from_uci(rock_1_last+rock_2_last[0]+rock_1_last[1])
        else:
            return print("No legal moves available.")
        # elif (rock_2_last+rock_1_last[0]+rock_2_last[1]) in legal_moves:
        #     return chess.Move.from_uci(rock_2_last+rock_1_last[0]+rock_2_last[1])
        # elif (rock_2_last+rock_2_last[0]+rock_1_last[1]) in legal_moves:
        #     return chess.Move.from_uci(rock_2_last+rock_2_last[0]+rock_1_last[1])
    # elif rook1_danger == 1:
    else:
        if ((rock_1_last[0]==rock_2_last[0] and rock_1_last[0]==white_king_last[0]) or (rock_1_last[1]==rock_2_last[1] and rock_1_last[1]==white_king_last[1])) and  (chess.square_distance(chess.parse_square(rock_1_last), chess.parse_square(rock_2_last)) != 1):
            return chess.Move.from_uci(rock_1_last+rock_1_last[0]+rock_2_last[1])
        if not is_king_in_opposite_corner(white_king_last):
            if ()


    global white_king_last
    if rook_last[0] == white_king_last[0]:
        return chess.Move.from_uci("a1a8")


def stairs_move(legal_moves):
    global white_king_last
    global black_king_last
    global rock_1_last
    global rock_2_last
    black_king_square = chess.parse_square(black_king_last)
    white_king_square = chess.parse_square(white_king_last)
    rock_1_square = chess.parse_square(rock_1_last)
    rock_2_square = chess.parse_square(rock_2_last)
    rook1_danger = 0
    rook2_danger = 0
    if chess.square_distance(black_king_square, rock_1_square) == 1 and rock_1_last[0]!=rock_2_last[0] and rock_1_last[1]!=rock_2_last[1]:
        rook1_danger = 1
    if chess.square_distance(black_king_square, rock_2_square) == 1 and rock_1_last[0]!=rock_2_last[0] and rock_1_last[1]!=rock_2_last[1]:
        rook2_danger = 1
    return move_rook(rook1_danger, rook2_danger, legal_moves)


def move_piece_randomly(board, label, rock_list_move, player_color):
    global white_king_last
    global black_king_last
    global rock_1_last
    global rock_2_last
    if not board.is_game_over():
        legal_moves = list(board.legal_moves)
        random_move = random.choice(legal_moves)
        if player_color == chess.BLACK:  # If it's black player's turn
            user_input = input("Enter your King move (e.g., 'f8'): ")
            if user_input:
                target_square = chess.parse_square(user_input)
                king_from_square = chess.parse_square(white_king_last)
                move = chess.Move(king_from_square, target_square)
                print(move)
                print(legal_moves)
                if move in legal_moves:
                    random_move = move
            white_king_last = chess.square_name(random_move.to_square)
        else:
            random_move = stairs_move(legal_moves)
            # elif legal_moves:
            #     random_move = random.choice(legal_moves)
            # else:
            #     print("No legal moves available.")
            #     return

        board.push(random_move)
        print(random_move)
        update_board_image(board, label)  # Update the board image after the move


rock_list_move = ["a1a8", "a8d8"]

board = chess.Board()
board.clear()

white_king_last = "e1"
black_king_last = "e8"
rock_1_last = "a1"
rock_2_last = "h1"

board.set_piece_at(chess.parse_square(white_king_last), chess.Piece(chess.KING, chess.WHITE))
board.set_piece_at(chess.parse_square(black_king_last), chess.Piece(chess.KING, chess.BLACK))
board.set_piece_at(chess.parse_square(rock_1_last), chess.Piece(chess.ROOK, chess.WHITE))
board.set_piece_at(chess.parse_square(rock_2_last), chess.Piece(chess.ROOK, chess.WHITE))

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
        move_piece_randomly(board, label, rock_list_move, chess.BLACK)
    else:  # White moves
        move_piece_randomly(board, label, rock_list_move, chess.WHITE)
        legal_moves = list(board.legal_moves)

    root.update()  # GUI update !!!!
    time.sleep(3)

# move_black_king_randomly(board, label)

root.mainloop()
