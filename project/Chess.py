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

# def is_black_king_near_rook(board):
#     black_king_square = board.king(chess.BLACK)
#     rock_1_square = chess.parse_square(rock_1_last)
#     rock_2_square = chess.parse_square(rock_2_last)
#     if chess.square_distance(black_king_square, rock_1_square) == 1:
#         save_rook(board, rock_1_square)
#         return True
#     if chess.square_distance(black_king_square, rock_2_square) == 1:
#         save_rook(board, rock_2_square)
#         return True
#     return False

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
            if legal_moves:
                random_move = random.choice(legal_moves)
            else:
                print("No legal moves available.")
                return

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
board.set_piece_at(chess.parse_square(rock_1_last) , chess.Piece(chess.ROOK, chess.WHITE))
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
