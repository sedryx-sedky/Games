import tkinter as tk
import random

"""
A simple Tetris game built with Tkinter. I wrote this back in Sixth-form during Year 12.

@author: Hamed Sedky
@created: 2020
"""

BlockData = {
    "S": ((1, 0, 2, 0, 0, 1, 1, 1), (0, 0, 0, 1, 1, 1, 1, 2)),
    "T": ((1, 0, 0, 1, 1, 1, 2, 1), (0, 0, 0, 1, 0, 2, 1, 1), (0, 0, 1, 0, 2, 0, 1, 1), (1, 0, 1, 1, 1, 2, 0, 1)),
    "I": ((0, 0, 1, 0, 2, 0, 3, 0), (0, 0, 0, 1, 0, 2, 0, 3)),
    "O": ((0, 0, 1, 0, 0, 1, 1, 1),),
    "L": ((0, 1, 1, 1, 2, 1, 2, 0), (0, 0, 0, 1, 0, 2, 1, 2), (0, 0, 0, 1, 1, 0, 2, 0), (0, 0, 1, 0, 1, 1, 1, 2)),
    "BL": ((0, 0, 0, 1, 1, 1, 2, 1), (0, 0, 0, 1, 0, 2, 1, 0), (0, 0, 1, 0, 2, 0, 2, 1), (1, 0, 1, 1, 1, 2, 0, 2)),
    "BS": ((0, 0, 1, 0, 1, 1, 2, 1), (1, 0, 1, 1, 0, 1, 0, 2)),
}

COLOURS = {
    "S": "green",
    "T": "purple",
    "I": "light blue",
    "O": "yellow",
    "L": "orange",
    "BL": "blue",
    "BS": "red",
}

COLOURS = {
    "S": "#61D836",
    "T": "#7816C4",
    "I": "cyan",
    "O": "#ffff00",
    "L": "#FFAF00",
    "BL": "#3D14FF",
    "BS": "#FF0063",
}

BLOCKS = ["S","T","O","I","L","BL","BS"]
GHOST_COLOUR = "#BBB5BB" #"#9F9F9F"

WIDTH = 10
HEIGHT = 20

Left = (";", "Left", )
Right = ("\\", "Right")
Up = ("[", "Up")
Down = ("'", "Down")

Hold_btn = ("Return", "bracketright")

Default_timer = 45 #30#200#45#55 #65 #500
Default_delay = 70#90#35 #90 #100
Counter = 1

Boxes_Colour = "#D41876" #"#00AB8E"
InteriorBoxesColour = "#970E53" #"#006C65"

W = {0:"#006C65", 1:"#73FDEA", 2:"#00AB8E", 3:"#16E7CF"}
#W = ["#FF968D", "#EE220C", "#FF644E", "#B51700"]

class Application:
    def __init__(self, master = None):
        self.master = tk.Tk() if master == None else master
        self.master.title("Tetris")
        self.master.minsize(750,755)
        #self.master.resizable(False, False)

        self.w = 0
        self.State = "disabled"

        #self.Mouse = pynput.mouse.Controller()
        #grey
        self.canvas = tk.Canvas(self.master, highlightthickness = 0, bg = "#5E5E5E", cursor = "")
        self.canvas.pack(fill = "both", expand = True)

        self.use_colour = False

        self.ignore_user_input = False
        self.game_over = False
        self.game_paused = False

        self.timer = Default_timer
        self.delay = Default_delay
        self.counter = Counter
        self.move_counter = 0

        self.Score = 0
        self.HighScore = 0

        self.X = WIDTH // 2
        self.Y = -1

        self.next_block = []
        self.hold_block = []

        self.block = []
        self.coords = []
        self.ghost = []
        self.ghost_coords = []

        for y in range(HEIGHT):
            for x in range(WIDTH):
                pos = "{},{}".format(x, y)
                self.create_round_rect(0, 0, 0, 0, radius = 10, tag = (pos, "uni"), fill = "", width = .25, outline = "")

        self.create_round_rect(0, 0, 0, 0, fill = "", width = 1, outline = "white", tag = "game_box")

        self.create_round_rect(0, 0, 0, 0, fill = Boxes_Colour, outline = "", tag = "main_next_box")
        self.canvas.create_text(0, 0, text = "Next", font = ("cmu serif", 20, "bold"), tag = "next_label")

        for i in range(4):
            tag = "next{}".format(i + 1)
            self.create_round_rect(0, 0, 0, 0, fill = InteriorBoxesColour, tag = tag)

        self.create_round_rect(0, 0, 0, 0, fill = Boxes_Colour, outline = "", tag = "score_box")
        self.create_round_rect(0, 0, 0, 0, fill = InteriorBoxesColour, outline = "", tag = "score_box2")
        self.canvas.create_text(0, 0, text = "Score", font = ("cmu serif", 25, "bold"), tag = "score_label")
        self.canvas.create_text(0, 0, text = str(self.Score), font = ("cmu serif", 20), tag = "score")

        self.create_round_rect(0, 0, 0, 0, fill = Boxes_Colour, outline = "", tag = "highscore_box")
        self.create_round_rect(0, 0, 0, 0, fill = InteriorBoxesColour, outline = "", tag = "highscore_box2")
        self.canvas.create_text(0, 0, text = "HighScore", font = ("cmu serif", 20, "bold"), tag = "highscore_label")
        self.canvas.create_text(0, 0, text = str(self.HighScore), font = ("cmu serif", 20), tag = "highscore")

        self.canvas.create_rectangle(0, 0, 0, 0, fill = "", width = 0, tag = "game_over_underlay")
        self.canvas.create_text(0, 0, text = "Game Over", font = ("cmu serif", 70, "bold"), fill = "", tag = "game_over")
        self.canvas.create_text(0, 0, text = "", font = ("cmu serif", 30, "bold"), fill = "", tag = "game_over_score")
        self.canvas.create_text(0, 0, text = "New Highscore", font = ("cmu serif", 20), fill = "", tag = "game_over_new_highscore")

        self.create_round_rect(0, 0, 0, 0, fill = Boxes_Colour, outline = "", tag = "HOLD_BOX")
        self.create_round_rect(0, 0, 0, 0, fill = InteriorBoxesColour, outline = "", tag = "hold_box2")
        self.canvas.create_text(0, 0, text = "Hold", font = ("cmu serif", 20, "bold"), tag = "hold_label")

        for y in range(4):
            for x in range(4):
                next_box1 = "N1_{},{}".format(x, y)
                next_box2 = "N2_{},{}".format(x, y)
                next_box3 = "N3_{},{}".format(x, y)
                next_box4 = "N4_{},{}".format(x, y)

                hold_box = "H_{},{}".format(x, y)

                self.create_round_rect(0, 0, 0, 0, fill = "", width = .25, outline = "", tag = (next_box1, "next_box", "uni"))
                self.create_round_rect(0, 0, 0, 0, fill = "", width = .25, outline = "", tag = (next_box2, "next_box", "uni"))
                self.create_round_rect(0, 0, 0, 0, fill = "", width = .25, outline = "", tag = (next_box3, "next_box", "uni"))
                self.create_round_rect(0, 0, 0, 0, fill = "", width = .25, outline = "", tag = (next_box4, "next_box", "uni"))

                self.create_round_rect(0, 0, 0, 0, radius = 10, fill = "", width = .25, outline = "", tag = (hold_box, "hold_box", "uni"))

        self.canvas.create_text(0, 0, text = "Paused", fill = "", font = ("cmu serif", 100, "bold"), tag = "paused")

        self.canvas.bind("<Configure>", self.RedrawGraphicalUserInterface)
        self.RedrawGraphicalUserInterface()

        self.master.bind("<Key>", self.KeyHandler)
        self.master.bind("<FocusOut>", self.OnFocusOut)

        self.mouse_x = 300
        self.mouse_y = 500

        #self.Mouse.position = (self.mouse_x, self.mouse_y)

        if False:
            self.master.bind("<Motion>", lambda event: self.OnMouseMove())
            self.master.bind("<Button-1>", lambda event: self.RotateShape())
            self.master.bind("<Button-2>", lambda event: self.pushBlockDown())
            #self.master.bind("<ButtonRelease-1>", lambda event: self.CreateHoldBlock())

            self.fullscreen = True
            self.master.bind("<Escape>", lambda event: self.OnEscapeKey())
            self.master.bind("<BackSpace>", lambda event: self.master.destroy())
            #self.master.bind("a", lambda event: self.OnKey())

            self.master.attributes("-fullscreen", True)

        self.BLOCKS_copy = BLOCKS.copy()

        self.canvas.itemconfigure("uni", state = self.State)

        self.CreateNextBlockInit()
        self.CreateBlock()
    def CreateBlock(self):
        self.block.clear()
        self.block.extend(self.next_block[0:5])
        self.CreateNextBlock()

        self.coords.clear()
        self.ghost.clear()
        self.ghost_coords.clear()
        self.ghost.extend(self.block)
        self.ghost[1] = (GHOST_COLOUR, "")

        if self.can_display_block(self.block, self.coords) is False:
            self.ignore_user_input = True
            self.game_over = True

            self.canvas.itemconfigure("game_over_underlay", fill = "black")
            self.canvas.itemconfigure("game_over", fill = "red")
            self.canvas.itemconfigure("game_over_score", text = str(self.Score), fill = "red")

            if self.Score > self.HighScore:
                self.canvas.itemconfigure("game_over_new_highscore", fill = "orange")
                self.HighScore = self.Score
            return

        self.ghost_coords.extend(self.coords.copy())

        self.create_ghost()

        self.display_block(self.block, self.coords)

        self.MoveBlockDown()
    def CreateNextBlockInit(self):
        for block_type in random.sample(BLOCKS, 4):
            #colour = COLOURS[block_type]
            #self.BLOCKS_copy.remove(block_type)

            colourActive = COLOURS[block_type]
            colourDisabled = W[self.w]
            self.w = (self.w + 1) % 4

            rotation = 0
            self.next_block.extend([block_type, (colourActive, colourDisabled), rotation, self.X, self.Y])
    def CreateNextBlock(self):
        for _ in range(5):
            self.next_block.pop(0)

        block_type = random.choice(self.BLOCKS_copy)
        #self.BLOCKS_copy.remove(block_type)
        #self.BLOCKS_copy = BLOCKS.copy()
        colourActive = COLOURS[block_type]
        colourDisabled = W[self.w]
        self.w = (self.w + 1) % 4

        rotation = 0
        self.next_block.extend([block_type, (colourActive, colourDisabled), rotation, self.X, self.Y])

        self.canvas.itemconfigure("next_box", fill = "", outline = "", disabledfill = "", disabledoutline = "")

        for i in range(4):
            pos = 5 * i
            block_type = self.next_block[pos]
            blockCoords = BlockData[block_type][0]

            colour = self.next_block[pos + 1]

            for index, x in enumerate(blockCoords):
                if index % 2 == 1:
                    continue
                y = blockCoords[index + 1]

                tag = "N{}_{},{}".format(i + 1, x, y)
                self.canvas.itemconfigure(tag, fill = colour[0], disabledfill = colour[1], outline = "black", disabledoutline = "black")
    def CreateHoldBlock(self):
        block_type, colour, rotation, X, Y = self.block[0:5]
        blockCoords = BlockData[block_type][rotation]

        self.master.after_cancel(self.after_id)

        for index, tag in enumerate(self.coords):
            self.canvas.itemconfigure(tag, fill = "", disabledfill = "", outline = "", disabledoutline = "")
            self.canvas.itemconfigure(self.ghost_coords[index], fill = "", outline = "", disabledfill = "", disabledoutline = "")

        if self.hold_block != []:
            hold_block_type, hold_colour, hold_rotation = self.hold_block
            hold_blockCoords = BlockData[hold_block_type][hold_rotation]

            overlap = False

            hold_coords = []
            for index, x in enumerate(hold_blockCoords):
                if index % 2 == 1:
                    continue
                y = hold_blockCoords[index + 1]

                x += X
                y += Y

                tag = "{},{}".format(x, y)

                tag_colour = self.canvas.itemcget(tag, "fill")
                if tag_colour not in ("", GHOST_COLOUR):
                    overlap = True
                    break

                hold_coords.append(tag)

            hold_block = [hold_block_type, hold_colour, hold_rotation, X, Y]
            if overlap is True or self.can_display_block(hold_block, hold_coords) is False:
                self.create_ghost()

                for tag in self.coords:
                    self.canvas.itemconfigure(tag, fill = colour[0], outline = "black", disabledfill = colour[1], disabledoutline = "black")
                self.MoveBlockDown()
                return
            else:
                self.hold_block.clear()
                self.hold_block.extend([block_type, colour, rotation])

                self.block.clear()
                self.ghost.clear()

                hold_block[3] = X
                hold_block[4] = Y

                self.block.extend(hold_block.copy())
                self.ghost.extend(hold_block.copy())
                self.ghost[1] = (GHOST_COLOUR, "")

                self.coords.clear()
                self.ghost_coords.clear()

                self.coords.extend(hold_coords.copy())
                self.ghost_coords.extend(hold_coords.copy())

                self.create_ghost()
                for tag in self.coords:
                    self.canvas.itemconfigure(tag, fill = hold_colour[0], outline = "black", disabledfill = hold_colour[1], disabledoutline = "black")
                self.MoveBlockDown()

        self.canvas.itemconfigure("hold_box", fill = "", outline = "", disabledfill = "", disabledoutline = "")

        for index, x in enumerate(blockCoords):
            if index % 2 == 1:
                continue
            y = blockCoords[index + 1]

            tag = "H_{},{}".format(x, y)

            self.canvas.itemconfigure(tag, fill = colour[0], outline = "black", disabledfill = colour[1], disabledoutline = "black")

        if self.hold_block == []:
            self.hold_block.extend([block_type, colour, rotation])

            self.CreateBlock()

            dx = X - self.X
            dy = Y - self.Y

            self.MoveBlock(dx, dy)
    def RedrawGraphicalUserInterface(self, event = None):
        if event == None:
            width = 750
            height = 755
        else:
            width = event.width
            height = event.height

        if width > 750 or height > 755:
            X = width // 2
            Y = height // 2

            dx = X + 375 - 150 - self.Qx
            dy = Y + 377.5 - 4 - self.Qy

            self.canvas.move("all", dx, dy)
            self.Qx += dx
            self.Qy += dy
            return

        box_width = (width - 312) / WIDTH
        box_height = (height - 5) / HEIGHT

        self.A = box_width
        self.B = box_height

        X, Y = 156, 7
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pos = "{},{}".format(x, y)
                self.create_round_rect(X, Y, X + box_width, Y + box_height, radius = 10, tagOrId = pos)

                Y += box_height - .5
            X += box_width
            Y = 7

        self.create_round_rect(150, 4, width - 150 - 1, height - 4, radius = 25, tagOrId = "game_box")
        self.Qx = width - 150
        self.Qy = height - 4

        self.canvas.coords("paused", width // 2, height // 2)

        next_x1 = width - 140
        next_y1 = 100
        next_x2 = width - 15
        next_y2 = height - 225

        self.canvas.coords("next_label", (width + width - 150) // 2, 115)
        self.create_round_rect(next_x1, next_y1, next_x2, next_y2, tagOrId = "main_next_box")

        NextBox_height = (height - 225 - 25) // 4 - 35

        nextBox_width = (next_x2 - next_x1 - 24) / 4
        nextBox_height = (NextBox_height - 4) / 4

        for i in range(4):
            Y = 130 + 100 * i
            self.create_round_rect(next_x1 + 10, Y, next_x2 - 10, Y + NextBox_height, tagOrId = "next{}".format(i + 1))

            Y += 4

            X2, Y2 = next_x1 + 14, Y
            for x in range(4):
                for y in range(4):
                    tag = "N{}_{},{}".format(i + 1, x, y)
                    self.create_round_rect(X2, Y2, X2 + nextBox_width, Y2 + nextBox_height, radius = 10, tagOrId = tag)
                    Y2 += nextBox_height - 1
                X2 += nextBox_width - 1
                Y2 = Y

        mid_x = width // 2
        mid_y = 250
        self.canvas.coords("game_over_underlay", 150, mid_y - 25, width - 150, mid_y + 65)
        self.canvas.coords("game_over", mid_x, mid_y)
        self.canvas.coords("game_over_score", mid_x, mid_y + 45)
        self.canvas.coords("game_over_new_highscore", mid_x - 115, mid_y + 45)

        mid_y = height // 2

        x = 75
        y = 400
        self.create_round_rect(x - 55, y - 50, x + 55, y + 50, tagOrId = "score_box")
        self.create_round_rect(x - 50, y - 20, x + 50, y + 45, tagOrId = "score_box2")

        self.canvas.coords("score_label", x, y - 37)
        self.canvas.coords("score", x, y + 12.5)

        y += 125
        self.create_round_rect(x - 55, y - 50, x + 55, y + 50, tagOrId = "highscore_box")
        self.create_round_rect(x - 50, y - 20, x + 50, y + 45, tagOrId = "highscore_box2")

        self.canvas.coords("highscore_label", x, y - 37)
        self.canvas.coords("highscore", x, y + 12.5)

        x3 = 75
        y3 = 200

        self.create_round_rect(x3 - 55, y3 - 50, x + 55, y3 + 55, tagOrId = "HOLD_BOX")
        self.canvas.coords("hold_label", x3, y3 - 35)

        x5 = x3 - 50
        x6 = x3 + 50
        y5 = y3 - 20
        y6 = y3 + 50
        self.create_round_rect(x5, y5, x6, y6, tagOrId = "hold_box2")

        holdBox_width = (x6 - x5 - 4) / 4
        holdBox_height = (y6 - y5 - 3) / 4

        x5 += 2
        y5 += 1

        X2, Y2 = x5, y5
        for y in range(4):
            for x in range(4):
                hold_box = "H_{},{}".format(x, y)
                self.create_round_rect(X2, Y2, X2 + holdBox_width, Y2 + holdBox_height, radius = 10, tagOrId = hold_box)
                X2 += holdBox_width
            Y2 += holdBox_height
            X2 = x5
    def KeyHandler(self, event):
        key = event.keysym

        if key == "Tab":
            self.State = "normal" if self.State == "disabled" else "disabled"
            self.canvas.itemconfigure("uni", state = self.State)

        if self.game_over is True and key == "space":
            self.game_over = False
            self.master.after(55, self.clear_text_on_screen)

        if self.game_paused is True and key == "p":
            self.UnpauseGame()
            return

        if self.ignore_user_input is True:
            return

        if key in Left:
            self.MoveBlock(-1, 0)
        elif key in Right:
            self.MoveBlock(1, 0)
        elif key in Down:
            self.MoveBlock(0, 1)
        elif key in Up:
            self.RotateShape()
        elif key == "space":
            self.pushBlockDown()
        elif key in Hold_btn:
            self.CreateHoldBlock()
        elif key == "p":
            self.PauseGame()
    def OnFocusOut(self, event):
        if self.game_over is False and self.game_paused is False:
            self.PauseGame()
    def MoveBlock(self, delta_x, delta_y):
        if self.block == []:
            return False

        self.block[3] += delta_x
        self.block[4] += delta_y

        return_value = self.can_display_block(self.block, self.coords)

        if return_value is False:
            self.block[3] -= delta_x
            self.block[4] -= delta_y
            return False

        if delta_x != 0 and self.move_counter <= 5:
            self.master.after_cancel(self.after_id)
            self.after_id = self.master.after(self.delay, self.MoveBlockDown)

        if delta_x != 0:
            self.create_ghost()

        self.display_block(self.block, self.coords)

        self.move_counter += 1
        return True
    def MoveBlockDown(self):
        if self.move_counter != 0:
            self.move_counter = 0

        return_value = self.MoveBlock(0, 1)

        if return_value is False:
            self.master.after_cancel(self.after_id)
            self.CheckForCompleteRow()
        else:
            self.after_id = self.master.after(self.timer, self.MoveBlockDown)
    def RotateShape(self):
        if self.block == []:
            return

        block_type, colour, rotation, X, Y = self.block
        temp_var = self.block[2]
        self.block[2] += 1

        return_value = self.can_display_block(self.block, self.coords)

        if return_value is False and self.block:
            self.block[2] = temp_var
            return

        if self.move_counter <= 5:
            self.master.after_cancel(self.after_id)
            self.after_id = self.master.after(self.delay, self.MoveBlockDown)

        self.move_counter += 1

        self.create_ghost()

        self.display_block(self.block, self.coords)
    def can_display_block(self, block, coords):
        block_type, colour, rotation, X, Y = block[0:5]

        try:
            blockCoords = BlockData[block_type][rotation]
        except:
            block[2] = 0
            blockCoords = BlockData[block_type][0]

        for index, x in enumerate(blockCoords):
            if index % 2 == 1:
                continue
            y = blockCoords[index + 1]

            x += X
            y += Y

            tag = "{},{}".format(x, y)

            if x < 0 or x >= WIDTH:
                return False
            elif y < -1 or y >= HEIGHT:
                return False
            elif self.canvas.itemcget(tag, "fill") not in ("", GHOST_COLOUR) and tag not in coords:
                return False

        return True
    def display_block(self, block, coords):
        if self.can_display_block(block, coords) is False:
            return False

        for tag in coords:
            self.canvas.itemconfigure(tag, fill = "", disabledfill = "", outline = "", disabledoutline = "")

        block_type, colour, rotation, X, Y = block[0:5]
        blockCoords = BlockData[block_type][rotation]

        coords.clear()
        for index, x in enumerate(blockCoords):
            if index % 2 == 1:
                continue
            y = blockCoords[index + 1]

            x += X
            y += Y

            tag = "{},{}".format(x, y)

            self.canvas.itemconfigure(tag, fill = colour[0], disabledfill = colour[1], outline = "black", disabledoutline = "black", width = .25)
            coords.append(tag)
        return True
    def pushBlockDown(self):
        self.master.after_cancel(self.after_id)
        self.block[4] = self.ghost[4]

        for tag in self.coords:
            self.canvas.itemconfigure(tag, fill = "", disabledfill = "", outline = "", disabledoutline = "")

        return_value = self.display_block(self.block, self.coords)
        self.CheckForCompleteRow()
    def create_ghost(self):
        self.ghost[2] = self.block[2]
        self.ghost[3] = self.block[3]
        self.ghost[4] = self.block[4]

        for tag in self.coords:
            self.canvas.itemconfigure(tag, fill = "", disabledfill = "", outline = "", disabledoutline = "")

        value = True
        while value:
            self.ghost[4] += 1
            value = self.can_display_block(self.ghost, self.ghost_coords)

        self.ghost[4] -= 1

        if False and self.ghost[4] == self.block[4]:
            return
        self.display_block(self.ghost, self.ghost_coords)
    def PauseGame(self):
        self.game_paused = True
        self.ignore_user_input = True

        self.master.after_cancel(self.after_id)

        self.canvas.itemconfigure("paused", fill = "red")
        self.canvas.itemconfigure("game_box", fill = "#1F1F1F")
    def UnpauseGame(self):
        self.game_paused = False
        self.ignore_user_input = False

        self.canvas.itemconfigure("paused", fill = "")
        self.canvas.itemconfigure("game_box", fill = "")

        self.after_id = self.master.after(5, self.MoveBlockDown)
    def CheckForCompleteRow(self):
        completed_rows_list = []
        blankRow = ["" for i in range(WIDTH)]

        self.block.clear()
        self.coords.clear()

        rows_completed = 0

        for y in range(HEIGHT):
            completed_row = True
            for x in range(WIDTH):
                tag = "{},{}".format(x, y)

                colour = self.canvas.itemcget(tag, "fill")

                if colour == "":
                    completed_row = False
                    break

            if completed_row is True:
                completed_rows_list.append(y)
                rows_completed += 1

        if completed_rows_list != []:
            self.ignore_user_input = True
            self.Score += rows_completed ** 2

            if False and self.Score >= 10 * self.counter:
                self.State = "normal" if self.State == "disabled" else "disabled"
                self.canvas.itemconfigure("uni", state = self.State)

                self.counter += 1

            self.canvas.itemconfigure("score", text = self.Score, font = ("cmu serif", 45))
            self.master.after(50, lambda: self.canvas.itemconfigure("score", font = ("cmu serif", 20)))
            self.DeleteRow(completed_rows_list, 0)
        else:
            self.CreateBlock()
    def DeleteRow(self, completed_rows_list, x):
        for y in completed_rows_list:
            tag = "{},{}".format(x, y)
            self.canvas.itemconfigure(tag, fill = "", disabledfill = "", outline = "", disabledoutline = "")

        x += 1
        if x < WIDTH:
            self.master.after(10, self.DeleteRow, completed_rows_list, x)
        else:
            self.MoveRowsDown(completed_rows_list, len(completed_rows_list), 0)
    def MoveRowsDown(self, completed_rows_list, length, pos):
        Y = completed_rows_list[pos]
        pos += 1
        for y in range(Y, -1, -1):
            for x in range(WIDTH):
                old_tag = "{},{}".format(x, y - 1)
                tag = "{},{}".format(x, y)

                colourActive = self.canvas.itemcget(old_tag, "fill")
                colourDisabled = self.canvas.itemcget(old_tag, "disabledfill")

                if colourActive == "":
                    outlineActive = ""
                else:
                    outlineActive = "black"

                if colourDisabled == "":
                    outlineDisabled = ""
                else:
                    outlineDisabled = "black"

                self.canvas.itemconfigure(tag, fill = colourActive, outline = outlineActive, disabledfill = colourDisabled, disabledoutline = outlineDisabled)
        if pos < length:
            self.master.after(10, self.MoveRowsDown, completed_rows_list, length, pos)
        else:
            self.ignore_user_input = False
            self.CreateBlock()
    def clear_text_on_screen(self):
        self.canvas.itemconfigure("game_over_underlay", fill = "")
        self.canvas.itemconfigure("game_over", fill = "")
        self.canvas.itemconfigure("game_over_score", fill = "")
        self.canvas.itemconfigure("game_over_new_highscore", fill = "")

        self.ResetAnimation(0)
    def ResetAnimation(self, x):
        #for y in range(HEIGHT):
            #tag = "{},{}".format(x, y)
            #self.canvas.itemconfigure(tag, fill = "white", outline = "black")

        for y in range(HEIGHT):
            X = x if y % 2 == 0 else (WIDTH - 1 - x)
            tag = "{},{}".format(X, y)
            self.canvas.itemconfigure(tag, fill = "white", outline = "black", disabledfill = "white", disabledoutline = "black")

        x += 1

        if x != WIDTH:
            self.master.after(15, self.ResetAnimation, x)
        else:
            self.master.after(5, self.restart_animation, WIDTH - 1)
    def restart_animation(self, x):
        for y in range(HEIGHT):
            tag = "{},{}".format(x, y)
            self.canvas.itemconfigure(tag, fill = "", disabledfill = "", outline = "", disabledoutline = "")

        x -= 1

        if x >= 0:
            self.master.after(15, self.restart_animation, x)
        else:
            self.restart_variables()
            return
    def restart_variables(self):
        self.timer = Default_timer
        self.delay = Default_delay
        self.counter = Counter

        self.ignore_user_input = False

        self.Score = 0
        self.canvas.itemconfigure("score", text = "0")
        self.canvas.itemconfigure("highscore", text = self.HighScore)

        self.hold_block.clear()
        self.next_block.clear()
        self.block.clear()
        self.ghost.clear()
        self.coords.clear()
        self.ghost_coords.clear()

        self.canvas.itemconfigure("hold_box", fill = "", outline = "", disabledfill = "", disabledoutline = "")

        self.BLOCKS_copy = BLOCKS.copy()

        self.CreateNextBlockInit()
        self.CreateBlock()
    def create_round_rect(self, x1, y1, x2, y2, radius = 40, tagOrId = "", **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
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

        if tagOrId != "":
            self.canvas.coords(tagOrId, points)
        else:
            self.canvas.create_polygon(points, smooth = True, **kwargs)
    def OnMouseMove(self):
        x, y = self.Mouse.position

        delta_x = x - self.mouse_x
        delta_y = y - self.mouse_y

        try:
            Y = self.block[4]
        except:
            Y = 2

        if abs(delta_x) <= 1.4 * Y + 3:
            return
        if False and abs(delta_y) <= 75:
            return

        self.mouse_x = x
        self.mouse_y = y

        norm_x = 1 if delta_x > 0 else -1
        norm_y = 0 if delta_y > 0 else -1

        self.MoveBlock(norm_x, 0)
        self.OnKey()
    def OnEscapeKey(self):
        self.fullscreen = not self.fullscreen
        self.master.attributes("-fullscreen", self.fullscreen)
    def OnKey(self):
        x, y = self.Mouse.position
        #print(x, y)

        if (10 < x and x < 1425) and (100 < y and y < 840):
            return

        if x <= 10:
            X = 1420
        elif x >= 1425:
            X = 20
        else:
            X = x

        if y <= 350:
            Y = 820
        elif y >= 840:
            Y = 370
        else:
            Y = y

        self.Mouse.position = (X, Y)
        self.mouse_x = X
        self.mouse_y = Y

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
