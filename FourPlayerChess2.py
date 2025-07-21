import tkinter as tk

"""
This is a four-player chess game, like the variant in chess.com. I wrote this during the
start of Year 13 because me and my friends wanted to play four-player chess on chess.com, but
there was no simple way to play locally, instead needing a constant internet connection.
However this was near the same time as Covid, so eventually Sixth-form was all study from home,
so this project eventually stopped being developed beyond its current state. By the time Sixth-
form was back in-person there was no reason to complete the project, so its left in this
incomplete state.

Currenlty it supports allowing pieces to take legal moves, and allows promotion when
reaching the centre. It doesn't have check or checkmate detection, won't stop an illegal
King position and doesn't stop pieces from moving outside their turn.

@author: Hamed Sedky
@created: 2020
"""

class Piece:
    def __init__(self, name, colour, x, y):
        self.name = name
        self.colour = colour

        self.x = x
        self.y = y

        if self.name == "Pawn":
            if self.x == 98:
                self.dx = 1
                self.dy = 0
            elif self.x == 109:
                self.dx = -1
                self.dy = 0
            elif self.y == 2:
                self.dx = 0
                self.dy = 1
            elif self.y == 13:
                self.dx = 0
                self.dy = -1
            
        self.start_pos = (self.x, self.y)

        self.number_of_moves = 0
    def __str__(self):
        if self.name == "Rook":
            return "♜"
        elif self.name == "Knight":
            return "♞"
        elif self.name == "Bishop":
            return "♝"
        elif self.name == "Queen":
            return "♛"
        elif self.name == "King":
            return "♚"
        elif self.name == "Pawn":
            return "♟"
    def get_legal_moves(self):
        moves = []

        if self.name == "Rook":
            moves.extend(self.get_legal_moves_for_rook())
        elif self.name == "Knight":
            moves.extend(self.get_legal_moves_for_knight())
        elif self.name == "Bishop":
            moves.extend(self.get_legal_moves_for_bishop())
        elif self.name == "Queen":
            moves.extend(self.get_legal_moves_for_rook())
            moves.extend(self.get_legal_moves_for_bishop())
        elif self.name == "King":
            moves.extend(self.get_moves_for_king())
        elif self.name == "Pawn":
            moves.extend(self.get_legal_moves_for_pawn())

        return moves
    def get_legal_moves_for_rook(self):
        moves = []

        for i in range(4):
            for d in range(1, 14):
                if i == 0:
                    x, y = self.x + d, self.y
                elif i == 1:
                    x, y = self.x - d, self.y
                elif i == 2:
                    x, y = self.x, self.y + d
                elif i == 3:
                    x, y = self.x, self.y - d

                tile = f"{chr(x)}{y}"

                if self.is_out_bounds(x, y) is True:
                    break
                elif self.is_ally_on_tile(tile) is True:
                    break

                moves.append(tile)

                if self.is_tile_empty(tile) is False:
                    break

        return moves
    def get_legal_moves_for_knight(self):
        moves = []

        for i in range(8):
            if i == 0:
                x, y = self.x + 2, self.y + 1
            elif i == 1:
                x, y = self.x + 2, self.y - 1
            elif i == 2:
                x, y = self.x - 2, self.y + 1
            elif i == 3:
                x, y = self.x - 2, self.y - 1
            elif i == 4:
                x, y = self.x + 1, self.y + 2
            elif i == 5:
                x, y = self.x - 1, self.y + 2
            elif i == 6:
                x, y = self.x + 1, self.y - 2
            elif i == 7:
                x, y = self.x - 1, self.y - 2

            tile = f"{chr(x)}{y}"

            if self.is_out_bounds(x, y) is True:
                continue
            elif self.is_ally_on_tile(tile) is True:
                continue

            moves.append(tile)

        return moves
    def get_legal_moves_for_bishop(self):
        moves = []

        for i in range(4):
            for d in range(1, 14):
                if i == 0:
                    x, y = self.x + d, self.y + d
                elif i == 1:
                    x, y = self.x + d, self.y - d
                elif i == 2:
                    x, y = self.x - d, self.y + d
                elif i == 3:
                    x, y = self.x - d, self.y - d

                tile = f"{chr(x)}{y}"

                if self.is_out_bounds(x, y) is True:
                    break
                elif self.is_ally_on_tile(tile) is True:
                    break

                moves.append(tile)

                if self.is_tile_empty(tile) is False:
                    break

        return moves
    def get_legal_moves_for_pawn(self):
        moves = []

        for i in range(2):
            if i == 0:
                x, y = self.x + self.dx, self.y + self.dy
            elif i == 1:
                if (self.x, self.y) == self.start_pos:
                    x, y = self.x + 2 * self.dx, self.y + 2 * self.dy
                else:
                    break

            tile = f"{chr(x)}{y}"

            if self.is_out_bounds(x, y) is True:
                break
            elif self.is_tile_empty(tile) is False:
                break

            moves.append(tile)
        
        for i in range(2):
            x, y = self.x + self.dx, self.y + self.dy

            if i == 0:
                if self.dx == 0:
                    x += 1
                elif self.dy == 0:
                    y += 1
            elif i == 1:
                if self.dx == 0:
                    x -= 1
                elif self.dy == 0:
                    y -= 1

            tile = f"{chr(x)}{y}"

            if self.is_out_bounds(x, y) is True:
                continue
            elif self.is_tile_empty(tile) is True or self.is_ally_on_tile(tile) is True:
                continue

            moves.append(tile)

        return moves
    def get_moves_for_king(self):
        moves = []

        for i in range(8):
            if i == 0:
                x, y = self.x + 1, self.y
            elif i == 1:
                x, y = self.x - 1, self.y
            elif i == 2:
                x, y = self.x, self.y + 1
            elif i == 3:
                x, y = self.x, self.y - 1
            elif i == 4:
                x, y = self.x + 1, self.y + 1
            elif i == 5:
                x, y = self.x + 1, self.y - 1
            elif i == 6:
                x, y = self.x - 1, self.y + 1
            elif i == 7:
                x, y = self.x - 1, self.y - 1

            tile = f"{chr(x)}{y}"

            if self.is_out_bounds(x, y) is True:
                continue
            elif self.is_ally_on_tile(tile) is True:
                continue

            moves.append(tile)

        return moves
    def get_castling_moves_for_king(self):
        if self.name != "King":
            raise Exception("Castling is only for kings")

        moves = []

        if self.number_of_moves != 0:
            return moves

        if self.x in (97, 110):
            KingSide = f"{chr(self.x)}11"
            QueenSide = f"{chr(self.x)}4"
        elif self.y in (1, 14):
            KingSide = f"d{self.y}"
            QueenSide = f"k{self.y}"

        for tile in (KingSide, QueenSide):
            if self.is_tile_empty(tile) is True:
                continue

            piece = Board[tile]

            if piece.name != "Rook" or piece.colour != self.colour:
                continue
            elif piece.number_of_moves != 0:
                continue

            x = ord(tile[0])
            y = int(tile[1:])

            Dx = x - self.x
            Dy = y - self.y

            X = abs(Dx)
            Y = abs(Dy)

            dx = Dx // (X if X > 0 else 1)
            dy = Dy // (Y if Y > 0 else 1)

            R = max(abs(Dx), abs(Dy))

            for i in range(1, R):
                x -= dx
                y -= dy

                T = f"{chr(x)}{y}"

                if self.is_tile_empty(T) is False:
                    break
            else:
                moves.append(f"{chr(self.x + 2 * dx)}{self.y + 2 * dy}")

        return moves
    def is_out_bounds(self, x, y):
        if x <= 96 or y <= 0:
            return True
        elif x > 110 or y > 14:
            return True
        elif (x <= 99 or x >= 108) and (y <= 3 or y >= 12):
            return True
        else:
            return False
    def is_ally_on_tile(self, tile):
        piece = Board.get(tile, "")

        if piece == "":
            return False
        elif piece.colour == self.colour:
            return True
        else:
            return False
    def is_tile_empty(self, tile):
        if tile in Board:
            return False
        else:
            return True
    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

pieces = ("Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook")
Board = {}

#♜♞♝♛♚♟

Red = "#980000"
Blue = "blue"
Orange = "dark orange"
Green = "green"



class Application:
    def __init__(self, master = None):
        self.master = tk.Tk() if master == None else master
        self.master.title("4 Player Chess")
        self.master.minsize(350, 350)

        self.canvas = tk.Canvas(self.master, highlightthickness = 0, bg = "#3D3D3D")
        self.canvas.pack(fill = "both", expand = True)

        self.legal_moves = []
        self.selected_tile = ""

        self.create_chess_board()
        self.canvas.create_text(0, 0, tag = ("Mpiece", "movable"))

        self.create_options_menu()

        self.main()

        self.canvas.bind("<Configure>", self.redraw_interface)
    def create_chess_board(self):
        for x in range(14):
            for y in range(14):
                tag = f"{chr(97 + x)}{14 - y}"
                colour = "#212121" if (x + y) % 2 == 0 else "grey"

                if (x <= 2 or x >= 11) and (y <= 2 or y >= 11):
                    continue

                func = (lambda tag: lambda event: self.on_click(event, tag))(tag)

                self.canvas.create_rectangle(0, 0, 0, 0, fill = colour, tag = (tag, "U:" + tag), width = 0)
                self.canvas.create_text(0, 0, tag = ("piece", "T:" + tag, "U:" + tag))
                self.canvas.create_polygon(0, 0, 0, 0, tag = ("U:" + tag, "M:" + tag), fill = "")

                self.canvas.tag_bind("U:" + tag, "<Button-1>", func)

        self.canvas.create_oval(0, 0, 0, 0, tag = "centre", fill = "white", outline = "")
    def create_options_menu(self):
        self.canvas.create_polygon(0, 0, 0, 0, state = "hidden", fill = "cyan", tag = ("options", "op"), smooth = True)

        for Id, piece in enumerate(("Queen", "Rook", "Bishop", "Knight")):
            tag = f"op_T{Id}"

            if piece == "Queen":
                piece_icon = "♛"
            elif piece == "Rook":
                piece_icon = "♜"
            elif piece == "Bishop":
                piece_icon = "♝"
            elif piece == "Knight":
                piece_icon = "♞"

            self.canvas.create_text(0, 0, text = piece_icon, tag = ("op_text", tag, "op"), fill = "dark cyan", state = "hidden")
            
            enter_func = (lambda tag, piece: lambda event: self.on_option_enter(tag, piece))(tag, piece_icon)
            click_func = (lambda piece: lambda event: self.on_option_click(piece))(piece)
            leave_func = (lambda tag: lambda event: self.on_option_leave(tag))(tag)

            self.canvas.tag_bind(tag, "<Enter>", enter_func)
            self.canvas.tag_bind(tag, "<Button-1>", click_func)
            self.canvas.tag_bind(tag, "<Leave>", leave_func)
    def main(self):
        Board.clear()
        self.set_pieces_on_board()
    def set_pieces_on_board(self):
        for index, piece_type in enumerate(pieces):
            red_pos = f"{chr(100 + index)}1"
            red_piece = Piece(piece_type, Red, 100 + index, 1)

            blue_pos = f"a{4 + index}"
            blue_piece = Piece(piece_type, Blue, 97, 4 + index)

            orange_pos = f"{chr(100 + index)}14"
            orange_piece = Piece(piece_type, Orange, 100 + index, 14)

            green_pos = f"n{4 + index}"
            green_piece = Piece(piece_type, Green, 110, 4 + index)


            red_pawn_pos = f"{chr(100 + index)}2"
            red_pawn = Piece("Pawn", Red, 100 + index, 2)

            blue_pawn_pos = f"b{4 + index}"
            blue_pawn = Piece("Pawn", Blue, 98, 4 + index)

            orange_pawn_pos = f"{chr(100 + index)}13"
            orange_pawn = Piece("Pawn", Orange, 100 + index, 13)

            green_pawn_pos = f"m{4 + index}"
            green_pawn = Piece("Pawn", Green, 109, 4 + index)


            Board[red_pos] = red_piece
            Board[blue_pos] = blue_piece
            Board[orange_pos] = orange_piece
            Board[green_pos] = green_piece

            Board[red_pawn_pos] = red_pawn
            Board[blue_pawn_pos] = blue_pawn
            Board[orange_pawn_pos] = orange_pawn
            Board[green_pawn_pos] = green_pawn
    def redraw_interface(self, event):
        width = event.width
        height = event.height

        mid_x = width / 2
        mid_y = height / 2

        length = min(width, height) / 2 - 25

        self.draw_chess_board(mid_x - length, mid_y - length, mid_x + length, mid_y + length)

        if self.canvas.itemcget("options", "state") != "hidden":
            self.draw_option_menu()
    def draw_chess_board(self, x1, y1, x2, y2):
        board_width = abs(x2 - x1)
        board_height = abs(y2 - y1)

        tile_width = board_width / 14
        tile_height = board_height / 14

        hexagon_length_x = tile_width / 4
        hexagon_length_y = tile_height / 4.5

        for x in range(14):
            for y in range(14):
                tag = f"{chr(97 + x)}{14 - y}"

                if (x <= 2 or x >= 11) and (y <= 2 or y >= 11):
                    continue

                piece = Board.get(tag, "")
                if piece != "":
                    colour = piece.colour
                else:
                    colour = ""

                mid_x = x1 + tile_width * (x + .5)
                mid_y = y1 + tile_height * (y + .5)

                self.canvas.coords(tag, x1 + x * tile_width, y1 + y * tile_height, x1 + (x + 1) * tile_width, y1 + (y + 1) * tile_height)
                self.canvas.coords("T:" + tag, mid_x, mid_y)

                self.canvas.itemconfigure("T:" + tag, text = piece, fill = colour)

                self.redraw_hexagon(f"M:" + tag, mid_x, mid_y, hexagon_length_x, hexagon_length_y)

        font_size = int(min(tile_width, tile_height) / 1.25)
        self.canvas.itemconfigure("piece", font = ("Arial Unicode MS", font_size))
        self.canvas.itemconfigure("Mpiece", font = ("Arial Unicode MS", int(font_size * 1.45)))

        Lx = hexagon_length_x / 3.5
        Ly = hexagon_length_x / 3.5
        Mx = (x1 + x2) / 2
        My = (y1 + y2) / 2
        self.canvas.coords("centre", Mx - Lx, My - Ly, Mx + Lx, My + Ly)
    def on_click(self, event, tile):
        if self.canvas.itemcget("options", "state") != "hidden":
            return

        if tile in self.legal_moves:
            self.move_piece(self.selected_tile, tile)
            return

        if self.legal_moves != [] and tile not in self.legal_moves:
            self.clear_move_options()

        if tile not in Board:
            return

        piece = Board[tile]
        self.legal_moves.extend(piece.get_legal_moves())

        if piece.name == "King":
            self.legal_moves.extend(piece.get_castling_moves_for_king())

        self.display_move_options()
        self.selected_tile = tile

        self.mouse_x = event.x
        self.mouse_y = event.y

        self.canvas.itemconfigure("T:" + tile, text = "")

        self.canvas.itemconfigure("movable", text = piece, fill = piece.colour)
        self.canvas.coords("movable", self.mouse_x, self.mouse_y)

        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
    def on_mouse_drag(self, event):
        x = event.x
        y = event.y

        dx = x - self.mouse_x
        dy = y - self.mouse_y

        self.canvas.move("movable", dx, dy)

        self.mouse_x += dx
        self.mouse_y += dy
    def on_mouse_release(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        overlap = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        invalid = False
        if len(overlap) <= 1:
            invalid = True
        else:
            tile = self.canvas.gettags(overlap[0])[0]
            if tile in self.legal_moves:
                self.move_piece(self.selected_tile, tile)
            else:
                invalid = True

        if invalid is True:
            piece = Board[self.selected_tile]
            self.canvas.itemconfigure("T:" + self.selected_tile, text = piece, fill = piece.colour)

        self.canvas.coords("movable", 0, 0)
        self.canvas.itemconfigure("movable", fill = "")
    def redraw_hexagon(self, tag, mid_x, mid_y, length_x, length_y):
        x1 = mid_x - length_x
        x2 = mid_x + length_x

        y1 = mid_y - length_y
        y2 = mid_y + length_y

        Q1_x = (x1 + mid_x) / 2
        Q3_x = (x2 + mid_x) / 2

        points = (
            x1, mid_y,
            Q1_x, y1,
            Q3_x, y1,
            x2, mid_y,
            Q3_x, y2,
            Q1_x, y2
        )

        self.canvas.coords(tag, *points)
    def redraw_round_rect(self, tag, x1, y1, x2, y2, radius = 25):
        mid_x = (x1 + x2) / 2

        Q1_x = (mid_x + (mid_x + (x1 + mid_x) / 2) / 2) / 2
        Q3_x = (mid_x + (mid_x + (mid_x + x2) / 2) / 2) / 2

        points = [
            x1+radius, y1,
            x1+radius, y1,
            Q1_x, y1,
            Q1_x, y1,
            mid_x, y1-radius,
            mid_x, y1-radius,
            Q3_x, y1,
            Q3_x, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]

        self.canvas.coords(tag, points)
    def clear_move_options(self):
        for tile in self.legal_moves:
            self.canvas.itemconfigure("M:" + tile, fill = "", width = 0, outline = "")
        self.legal_moves.clear()
    def display_move_options(self):
        for tile in self.legal_moves:
            if tile in Board:
                self.canvas.itemconfigure("M:" + tile, outline = "#73FDEA", width = 6)
            else:
                self.canvas.itemconfigure("M:" + tile, fill = "#73FDEA")
    def move_piece(self, old_tile, new_tile):
        piece = Board[old_tile]
        colour = piece.colour

        piece.number_of_moves += 1

        new_x = ord(new_tile[0])
        new_y = int(new_tile[1:])

        piece.update_position(new_x, new_y)

        self.canvas.itemconfigure("T:" + old_tile, text = "")
        self.canvas.itemconfigure("T:" + new_tile, text = piece, fill = colour)

        Board[new_tile] = piece
        del Board[old_tile]

        self.clear_move_options()

        if piece.name == "Pawn":
            x, y = piece.start_pos

            if (piece.dy == 0 and new_x == x + 6 * piece.dx) or (piece.dx == 0 and new_y == y + 6 * piece.dy):
                self.new_tile = (new_x, new_y, new_tile)
                self.canvas.itemconfigure("op", state = "normal")
                self.draw_option_menu()

        if piece.name == "King" and piece.number_of_moves == 1:
            x, y = piece.start_pos

            dx = new_x - x
            dy = new_y - y

            if not(abs(dx) == 2 or abs(dy) == 2):
                return

            if dx == 2:
                X = 107
                Y = y
            elif dx == -2:
                X = 100
                Y = y
            elif dy == 2:
                X = x
                Y = 11
            elif dy == -2:
                X = x
                Y = 4

            old_rook_tile = f"{chr(X)}{Y}"
            new_rook_tile = f"{chr(x + dx // 2)}{y + dy // 2}"
            self.move_piece(old_rook_tile, new_rook_tile)
    def draw_option_menu(self):
        x = self.new_tile[0]
        y = self.new_tile[1]

        tile1 = f"{chr(x - 1)}{y - 1}"
        tile2 = f"{chr(x + 1)}{y - 1}"

        x1, y1 = self.canvas.coords(tile1)[0:2]
        x2, y2 = self.canvas.coords(tile2)[2:]

        self.redraw_round_rect("options", x1, y1, x2, y2, radius = 15)

        width = (x2 - x1) / 4
        height = (y2 - y1) / 4

        size = int(min(width, height) * 3)
        self.canvas.itemconfigure("op_text", font = ("Arial Unicode MS", size))
        self.font_size = size

        mid_y = (y1 + y2) / 2

        for Id in range(4):
            self.canvas.coords(f"op_T{Id}", x1 + width * (Id + 1/2), mid_y)

        self.canvas.move("op", 0, 10)
    def on_option_enter(self, tag, icon):
        self.canvas.itemconfigure(tag, font = ("Arial Unicode MS", int(self.font_size * 1.6)))

        tile = self.new_tile[2]
        self.canvas.itemconfigure("T:" + tile, text = icon)
    def on_option_click(self, piece_name):
        tile = self.new_tile[2]

        Board[tile].name = piece_name

        self.canvas.itemconfigure("op", state = "hidden")
    def on_option_leave(self, tag):
        self.canvas.itemconfigure(tag, font = ("Arial Unicode MS", self.font_size))

        tile = self.new_tile[2]

        if Board[tile].name != "Pawn":
            return

        self.canvas.itemconfigure("T:" + tile, text = "♟")

def main():
    root = tk.Tk()
    app = Application(root)

if __name__ == "__main__":
    main()