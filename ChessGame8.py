import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

"""
I wrote this Chess game during Sixth-form, in Year 12. I had written other Chess games proir
to this one, but I believe this was my first time using Tkinter's Canvas for a proper project.
Looking back at is now, I think I was in a phase where I was becoming more aware of proper
programming practices, and was trying to improve my code. Although I definiatly went
overboard in terms of commenting :)

The game can auto-detect checkmate, and supports undoing moves through ctrl-z.
Fun fact: Me and my friends got in trouble numerous times in Sixth-form because we played
this against one another in class when the teachers were talking.

@author: Hamed Sedky
@created: 2019

Everything past this point is Year 12 me.
"""

class Piece:
    """This is the class where all pieces will inherit from"""
    def __init__(self, colour, position, board, MustGo):
        """Each piece must know its colour, position on the board and the dictionary
        of the board state as well as if there are any tiles it must go to in the case
        of check to protect the King. Because dictionaries and lists are pointer objects
        this means that if any class changes the dictionary or list, thne they will change for
        all classes. The idea is that the Application class will change the board dictionary
        and MustGo list when moving a piece or when it's check and that this will also change
        the objects for every other class in the program"""
        
        self.colour = colour #Black or White

        #the position taken in as an argument should always be in
        #the form "{letter}{number}""
        #by using the bulit-in ord function we will be able to get the unicode number
        #of the letter at the beginning
        #There could be a problem here as this always expects the position argument to be in the
        #form "{letter}{number}" if it isn't in this format than an error might happen
        #a format check should be implemented here
        self.x = ord(position[0])
        self.y = int(position[1:])
        #The position argument is split up into two parts an x and y coordinates

        #My variable names here are kind of bad, in the Piece class I call this dictionary
        #board while in the Application class this is actually the pieces dictionary
        #not the board dictionary
        #Just remember that when I use the board dictionary in the Piece class it
        #actaully means the pieces dictionary in the Appilcation class
        #it's a bit confusing but hopefully you understand
        self.board = board

        #When its check than the King must be protected either by moving the King himself or by
        #moving another piece between the King or just eating the attacker
        #So to do this when it is check we will have a list that will conatain tiles that
        #all pieces must go to if they can but nowhere else 
        self.MustGo = MustGo
    def UpdatePosition(self, new_pos):
        """This function will be called when the piece has moved on the board, it will simply change
        the position variables of this piece so the class knows where the piece is on the board and
        can then calculate all the legal moves that that piece can make while on that position.
        It takes the new position of the piece as an argument"""

        #This works exactly like the code in the __init__ function
        self.x = ord(new_pos[0])
        self.y = int(new_pos[1:])
    @staticmethod
    def is_out_of_bounds(coords) -> bool:
        """This function will be called on when calcualating the legal moves of any piece
        This function will simply check if the coordinates entered are out of bounds or not
        and then return either True if they are out of bounds or False if the coordinates
        entered were valid"""

        #this function expects x to be a letter so using the built-in function ord
        #will allow us to get its unicode value
        x = ord(coords[0])

        #this function expects y to be a number so we need to convert
        #it to an int as now it is currently a string
        y = int(coords[1:])

        if x < 97 or x > 104:
            #x can only be between "a" and "h" otherwise its out of bounds and not valid
            #since in unicode "a" is 97 and "z" is 104 if the value of x is less than 97
            #or greater than 104 then we know that it's not valid
            return True
        elif y < 1 or y > 8:
            #y can only be between 1 and 8 otherwise its out of bounds and not valid
            #so if the value of y is less than 1 or greater than 8 than we know that it's not valid
            return True
        else:
            #If it passed all the other tests than now we know that the x and y coordinates
            #are not out of bounds so we return true
            return False
    def is_empty(self, coords) -> bool:
        """This function simply checkes weather a given tile is empty or occuppied by
        another piece and returns True if the tile is empty and False otherwise"""

        if self.board.get(coords) == None:
            #No piece could be found at that tile so True is returned
            return True
        else:
            #A piece could be found at that tile so it is not empty so False is returned
            return False
    def has_friend_on_tile(self, coords) -> bool:
        """This function simply checks weather a given til is empty or occuppied and if
        occuppied than will check if that piece is the same colour as this piece. It will
        return True if there is an ally on that tile and False otherwise"""

        if self.is_empty(coords) is True:
            #If the tile is empty than there is no ally on that tile so
            #a False is returned
            return False
        elif self.board[coords].colour == self.colour:
            #If the colour of the piece on the given tile is the same as
            #the colour of this piece than we have found an ally and return True
            return True
        else:
            #The piece we found did not have the same colour as this piece
            #so a False is returned
            return False

class Rook(Piece):
    __type__ = "Rook"

    @staticmethod
    def __str__():
        return "♜"

    def find_legal_moves(self):
        """This function will find and return all the legal moves that the rook can do at any given
        time on the board"""

        #creating and empty list were all the moves will be stored
        moves = []

        #The Rook always has four options to move in a game
        #forwards, backwards, to the right and to the left
        for i in range(4):
            for k in range(1, 8):
                if i == 0:
                    #moving to the right
                    x,y = self.x + k, self.y
                elif i == 1:
                    #moving to the left
                    x,y = self.x - k, self.y
                elif i == 2:
                    #moving forwards
                    x,y = self.x, self.y + k
                elif i == 3:
                    #moving backwards
                    x,y = self.x, self.y - k

                coords = chr(x) + str(y)

                if self.is_out_of_bounds(coords) is True:
                    #If the x and y coordinates are out of bounds then there is no need
                    #to carry on checking our current path so we will break out of this
                    #loop and begin checking the next path
                    break
                elif self.has_friend_on_tile(coords) is True:
                    #If the current tile has an ally of this piece than there is
                    #no point continuing on this path as in Chess we can't land
                    #on our own pieces or jump over them(expect for the Knight)
                    #so we will break out of this loop and check the next path
                    break

                if self.MustGo != [] and coords not in self.MustGo:
                    #If the MustGo list is not empty than we know that pieces must move to
                    #at least one of the positions that the list says, so we check that the move
                    #is in the list and if it's not than we continue the loop but don't add this to
                    #our list of moves
                    if self.is_empty(coords) is False:
                        #We also need to check weather the current tile is empty or not, if its
                        #not empty than we know that there is a piece on that tile so we can't
                        #move any further, so we need to break out of this loop
                        #Otherwise we will have this weird glitch were pieces will be able
                        #to move through each other when the King is in check
                        break
                    else:
                        #Otherwise we know that the current tile is empty so we just continue to
                        #the next move
                        continue

                #If the current position is not out of bounds or there
                #isn't an ally piece on that position than we can add that
                #position to our list of moves
                moves.append(coords)

                if self.is_empty(coords) is False:
                    #If the current tile isn't empty than we know, beacuse of the
                    #above if-statements, that this piece must be an enemy piece
                    #we can land on enemy pieces but we can't jump over them
                    #so we must now leave this path and begin on the next one
                    break

        #returning all the possible moves that this piece can make
        #under the current board state
        return moves
    def can_go_to(self, coords) -> bool:
        """This function calculates if it is possible for the Rook to move to the given position
        given its current position on the board. This function ignores if there are any pieces
        between the given position and the Rook and just checks if it's possible not weather
        the Rook can actually go there"""

        if ord(coords[0]) == self.x or int(coords[1:]) == self.y:
            #If both coordinates have the same x or y coordinates than we know it is possible
            #for the Rook to move there so we return True
            return True
        else:
            #Otherwise we return False
            return False
 
class Knight(Piece):
    __type__ = "Knight"

    @staticmethod
    def __str__():
        return "♞"

    def find_legal_moves(self):
        """This function will find and return all the legal moves that the knight can do at any given
        time on the board"""

        #creating and empty list were all the moves will be stored
        moves = []

        #The Knight always has eight options to move in a game because of its L shape
        #attack pattern
        #This will be diffcult to explain but when you see the Knight's movement you will
        #notice that he only moves two by either the x or y coordinate and then one by the other
        #coordinate
        for i in range(8):
            if i == 0:
                x, y = self.x - 2, self.y + 1
            elif i == 1:
                x, y = self.x - 2, self.y - 1
            elif i == 2:
                x, y = self.x + 2, self.y + 1
            elif i == 3:
                x, y = self.x + 2, self.y - 1
            elif i == 4:
                x, y = self.x + 1, self.y - 2
            elif i == 5:
                x, y = self.x - 1, self.y - 2
            elif i == 6:
                x, y = self.x + 1, self.y + 2
            elif i == 7:
                x, y = self.x - 1, self.y + 2

            coords = chr(x) + str(y)

            if self.is_out_of_bounds(coords) is True:
                #If the coordinates are out of bounds than there is now point
                #adding them to the moves list to we will continue with the next move
                continue

            if self.has_friend_on_tile(coords) is True:
                #Even thought the horse can jump over piece they can't eat their
                #allies so we need to check that the coordinates given to us don't hava an ally
                #on them if they do we simply continue on with the next move
                continue

            if self.MustGo != [] and coords not in self.MustGo:
                #If the MustGo list is not empty than we know that pieces must move to
                #at least one of the positions that the list says, so we check that the move
                #is in the list and if it's not than we continue the loop but don't add this to
                #our list of moves
                continue
            
            moves.append(coords)

        #returning all the possible moves that this piece can make
        #under the current board state
        return moves
    def can_go_to(self, coords) -> bool:
        """This function calculates if it is possible for the Knight to move to the given position
        given its current position on the board"""

        #Getting the x and y coordinates
        x = ord(coords[0])
        y = int(coords[1:])

        #Getting the absolute value of the difference between the x and y coordinates of the
        #Knight and the x and y coordinates of the coords
        abs_x = abs(self.x - x)
        abs_y = abs(self.y - y)

        if (abs_x == 2 and abs_y == 1) or (abs_x == 1 and abs_y == 2):
            #Due to the Knight's L-shaped movement it always moves 2 steps one way and one step
            #the other way so if abs_x and abs_y are two or one we know that the Knight can move there
            #so we return True
            return True
        else:
            #Otherwise we return False
            return False

class Bishop(Piece):
    __type__ = "Bishop"

    @staticmethod
    def __str__():
        return "♝"

    def find_legal_moves(self):
        """This function will find and return all the legal moves that the bishop can do at any given
        time on the board"""

        #creating and empty list were all the moves will be stored
        moves = []

        #The Bishop always has four options to move in a game
        #top left, bottom left, top right, bottom right
        for i in range(4):
            for k in range(1, 8):
                if i == 0:
                    #moving top left
                    x,y = self.x - k, self.y + k
                elif i == 1:
                    #moving bottom left
                    x,y = self.x - k, self.y - k
                elif i == 2:
                    #moving top right
                    x,y = self.x + k, self.y + k
                elif i == 3:
                    #moving bottom right
                    x,y = self.x + k, self.y - k

                coords = chr(x) + str(y)

                if self.is_out_of_bounds(coords) is True:
                    #If the x and y coordinates are out of bounds then there is no need
                    #to carry on checking our current path so we will break out of this
                    #loop and begin checking the next path
                    break
                elif self.has_friend_on_tile(coords) is True:
                    #If the current tile has an ally of this piece than there is
                    #no point continuing on this path as in Chess we can't land
                    #on our own pieces or jump over them(expect for the Knight)
                    #so we will break out of this loop and check the next path
                    break

                if self.MustGo != [] and coords not in self.MustGo:
                    #If the MustGo list is not empty than we know that pieces must move to
                    #at least one of the positions that the list says, so we check that the move
                    #is in the list and if it's not than we continue the loop but don't add this to
                    #our list of moves
                    if self.is_empty(coords) is False:
                        #We also need to check weather the current tile is empty or not, if its
                        #not empty than we know that there is a piece on that tile so we can't
                        #move any further, so we need to break out of this loop
                        #Otherwise we will have this weird glitch were pieces will be able
                        #to move through each other when the King is in check
                        break
                    else:
                        #Otherwise we know that the current tile is empty so we just continue to
                        #the next move
                        continue

                #If the current position is not out of bounds or there
                #isn't an ally piece on that position than we can add that
                #position to our list of moves
                moves.append(coords)

                if self.is_empty(coords) is False:
                    #If the current tile isn't empty than we know, beacuse of the
                    #above if-statements, that this piece must be an enemy piece
                    #we can land on enemy pieces but we can't jump over them
                    #so we must now leave this path and begin on the next one
                    break

        #returning all the possible moves that this piece can make
        #under the current board state
        return moves
    def can_go_to(self, coords) -> bool:
        """This function calculates if it is possible for the Bishop to move to the given position
        given its current position on the board. This function ignores if there are any pieces
        between the given position and the Bishop and just checks if it's possible not weather
        the Bishop can actually go there"""

        #Getting the x and y coordinates
        x = ord(coords[0])
        y = int(coords[1:])

        try:
            #Calculating the gradient of the line between the given position and the Bishop's position
            gradient = (self.y - y) / (self.x - x)
        except ZeroDivisionError:
            #If both x coordinates are the same than self.x - x would equal zero but we can't
            #divide by zero so instead we will make the gradient zero
            gradient = 0

        if abs(gradient) == 1:
            #The gradient of the Bishop's movement is always 1 or -1 so if the absolute value
            #of the gradient is 1 than we know it is possible for the Bishop to move there so we
            #return True
            return True
        else:
            #Otherwise we return False
            return False

class Queen(Piece):
    __type__ = "Queen"

    @staticmethod
    def __str__():
        return "♛"

    def find_legal_moves(self):
        """This function will find and return all the legal moves that the queen can do at any given
        time on the board"""

        #creating and empty list were all the moves will be stored
        moves = []

        #The Queen has both the movements of the Rook and the Bishop so she always has eight
        #options to move at any point in the board
        #Her movement is just combining the Rook's and Bishop's movement
        for i in range(8):
            for k in range(1, 8):
                if i == 0:
                    #moving to the right
                    x,y = self.x + k, self.y
                elif i == 1:
                    #moving to the left
                    x,y = self.x - k, self.y
                elif i == 2:
                    #moving forwards
                    x,y = self.x, self.y + k
                elif i == 3:
                    #moving backwards
                    x,y = self.x, self.y - k
                elif i == 4:
                    #moving top left
                    x,y = self.x - k, self.y + k
                elif i == 5:
                    #moving bottom left
                    x,y = self.x - k, self.y - k
                elif i == 6:
                    #moving top right
                    x,y = self.x + k, self.y + k
                elif i == 7:
                    #moving bottom right
                    x,y = self.x + k, self.y - k

                coords = chr(x) + str(y)

                if self.is_out_of_bounds(coords) is True:
                    #If the x and y coordinates are out of bounds then there is no need
                    #to carry on checking our current path so we will break out of this
                    #loop and begin checking the next path
                    break
                elif self.has_friend_on_tile(coords) is True:
                    #If the current tile has an ally of this piece than there is
                    #no point continuing on this path as in Chess we can't land
                    #on our own pieces or jump over them(expect for the Knight)
                    #so we will break out of this loop and check the next path
                    break

                if self.MustGo != [] and coords not in self.MustGo:
                    #If the MustGo list is not empty than we know that pieces must move to
                    #at least one of the positions that the list says, so we check that the move
                    #is in the list and if it's not than we continue the loop but don't add this to
                    #our list of moves
                    if self.is_empty(coords) is False:
                        #We also need to check weather the current tile is empty or not, if its
                        #not empty than we know that there is a piece on that tile so we can't
                        #move any further, so we need to break out of this loop
                        #Otherwise we will have this weird glitch were pieces will be able
                        #to move through each other when the King is in check
                        break
                    else:
                        #Otherwise we know that the current tile is empty so we just continue to
                        #the next move
                        continue

                #If the current position is not out of bounds or there
                #isn't an ally piece on that position than we can add that
                #position to our list of moves
                moves.append(coords)

                if self.is_empty(coords) is False:
                    #If the current tile isn't empty than we know, beacuse of the
                    #above if-statements, that this piece must be an enemy piece
                    #we can land on enemy pieces but we can't jump over them
                    #so we must now leave this path and begin on the next one
                    break

        #returning all the possible moves that this piece can make
        #under the current board state
        return moves
    def can_go_to(self, coords) -> bool:
        """This function calculates if it is possible for the Queen to move to the given position
        given its current position on the board. This function ignores if there are any pieces
        between the given position and the Queen and just checks if it's possible not weather
        the Queen can actually go there"""

        #Getting the x and y coordinates
        x = ord(coords[0])
        y = int(coords[1:])

        try:
            #Calculating the gradient of the line between the given position and the Queen's position
            gradient = (self.y - y) / (self.x - x)
        except ZeroDivisionError:
            #If both x coordinates are the same than self.x - x would equal zero but we can't
            #divide by zero so instead we will make the gradient zero
            gradient = 0

        if  (x == self.x or y == self.y) or abs(gradient) == 1:
            #The Queen has both the movements of the Rook and the Bishop so we just have to
            #use the logic of the Rook and the Bishop and return True if it passes the test
            return True
        else:
            #Otherwise we return False
            return False

class King(Piece):
    __type__ = "King"

    @staticmethod
    def __str__():
        return "♚"

    def find_all_possible_moves(self):
        """This function is a bit different to the other functions that the other pieces have as
        instead of find all the legal moves it only finds all the possible moves the King is able
        to move too, and then later on in the program the list of possible moves will be filtered
        to find only the legal moves of the King. This is because the King's legal moves are much
        more complicated than the other pieces as the King can never be moved to a place where he
        can be eaten and must always move some where else or be protected if he is in danger"""

        #creating and empty list were all the moves will be stored
        moves = []

        #The King only has a maximum of eight positions he can move too under any board state
        for i in range(8):
            if i == 0:
                #moving to the right
                x,y = self.x + 1, self.y
            elif i == 1:
                #moving to the left
                x,y = self.x - 1, self.y
            elif i == 2:
                #moving forwards
                x,y = self.x, self.y + 1
            elif i == 3:
                #moving backwards
                x,y = self.x, self.y - 1
            elif i == 4:
                #moving top left
                x,y = self.x - 1, self.y + 1
            elif i == 5:
                #moving bottom left
                x,y = self.x - 1, self.y - 1
            elif i == 6:
                #moving top right
                x,y = self.x + 1, self.y + 1
            elif i == 7:
                #moving bottom right
                x,y = self.x + 1, self.y - 1

            coords = chr(x) + str(y)

            if self.is_out_of_bounds(coords) is True:
                #If the x and y coordinates are out of bounds then we know that position
                #isn't a possible move for the King so we go check the next move
                continue
            elif self.has_friend_on_tile(coords) is True:
                #If the current tile has an ally of this piece than we know that
                #isn't a possible move for the King because in Chess we can't land
                #on our own pieces or jump over them(expect for the Knight)
                #so we go to check the next move
                continue

            #If the current position is not out of bounds or there
            #isn't an ally piece on that position than we can add that
            #position to our list of moves
            moves.append(coords)

        #returning all the possible moves that the King can make
        #under the current board state
        return moves
    def can_go_to(self, coords) -> bool:
        """This function calculates if it is possible for the King to move to the given position
        given its current position on the board. This function ignores if there are any pieces
        between the given position and the King and just checks if it's possible not weather
        the King can actually go there"""

        #Getting the x and y coordinates
        x = ord(coords[0])
        y = int(coords[1:])

        #Calculating the difference between the King position and the given position
        diff_x = abs(self.x - x)
        diff_y = abs(self.y - y)

        #We do this because the King's movement is just the same as the Queen's movement except
        #that he can only move one tile in each direction, so if the difference between the x and y
        #coordinates is greater than 1 than we know the King can't possibly move there so we can
        #return False
        if diff_x > 1 or diff_y > 1:
            return False
        else:
            #Otherwise we return True
            return True

class Pawn(Piece):
    __type__ = "Pawn"

    @staticmethod
    def __str__():
        return "♙"

    def find_legal_moves(self):
        """This function will find and return all the legal moves that the queen can do at any given
        time on the board"""

        #creating and empty list were all the moves will be stored
        moves = []

        #If the pawn is white it must move up the board but if its black it will move
        #down the board
        movement = 1 if self.colour == "white" else -1

        #The pawn's movement are the most diffcult to program not only do pawns move
        #in different directions depending on their colours but they also are very wierd in that their
        #attack is not the same as their normal movement
        for i in range(3):
            #The maxium amount of possible moves a pawn can make during a game is three
            #forwards once, and on the two diagonals to kill another piece
            #The pawns can move twice foreward on their first move but that's more of a special case
            if i == 0:
                #Moving foreward
                x, y = self.x, self.y + movement
            elif i == 1:
                #Moving diagnally to the right
                x, y = self.x + 1, self.y + movement
            elif i == 2:
                #Moving diagnally to the left
                x, y = self.x - 1, self.y + movement

            coords = chr(x) + str(y)

            if self.is_out_of_bounds(coords) is True:
                #If the current position is out of bounds there we can't do anything with
                #that move so we will continue to the next move
                continue

            #Due to the Pawns weird movement we have to change the varification we do on each move
            #When the Pawn is moving forward there can't be any piece in front of it
            #But when the Pawn is moving diagonally it can only do so when there is an enemy
            #over there
            if i == 0:
                #Checking the Pawn's forward movement
                if self.is_empty(coords) is False:
                    #The pawns can only move foreward when there is nothing in front of it
                    continue

                #If the pawn is white and has a 2 value for its y coordinate or if the pawn is black
                #and has a value of 7 for its y coordinate then we know that pawn hasn't moved yet so
                #we need to check weather it can move twice or not
                if (self.y == 2 and self.colour == "white") or (self.y == 7 and self.colour == "black"):
                    #Creating the new coordinates for the second move forward
                    newCoords = chr(x) + str(y + movement)

                    if self.is_empty(newCoords) is True:
                        #If we know that the tile is empty than we now know that the pawn can move
                        #there so we will add that to the list of moves

                        if self.MustGo == [] or newCoords in self.MustGo:
                            #But before we do that we have to check that the King isn't in danger
                            #and needs protecting
                            moves.append(newCoords)
            else:
                #Checking the Pawn's diagonal attack movement
                if self.is_empty(coords) is True:
                    #The pawn can only move diagnally to attack another piece so we have to check
                    #weather the tile we want to move to is empty if it is than we know that
                    #there is nothing to attack on that tile so the pawn can't move there
                    #so we will continue and check the next possible move
                    continue
                if self.has_friend_on_tile(coords) is True:
                    #When we know the tile isn't empty and there's a piece on it we than have to
                    #check weather that piece is the same colour as the pawn if it is than we can't
                    #attack it as pieces can't attack their own team
                    continue

            if self.MustGo != [] and coords not in self.MustGo:
                #If the MustGo list is not empty than we know that pieces must move to
                #at least one of the positions that the list says, so we check that the move
                #is in the list and if it's not than we continue the loop but don't add this to
                #our list of moves
                continue

            #Adding the position to the list of moves
            moves.append(coords)

        #returning all the possible moves that this piece can make
        #under the current board state
        return moves
    def can_go_to(self, coords) -> bool:
        """This function calculates if it is possible for the Pawn to move to the given position
        given its current position on the board. This function ignores if there are any pieces
        between the given position and the Pawn and just checks if it's possible not weather
        the Pawn can actually go there"""

        #If the Pawn is white it must move up the board but if its black it will move
        #down the board
        movement = 1 if self.colour == "white" else -1

        #This function only checks weather the Pawn can go diagnally it doesn't check if it
        #in front of the Pawn becuase the Pawn can only attack diagnally
        for i in range(2):
            if i == 0:
                x, y = self.x - 1, self.y + movement
            elif i == 1:
                x, y = self.x + 1, self.y + movement

            #This variable wil be the position the Pawn can go to
            possible_coords = chr(x) + str(y)

            #If the coords is equal to the possible_coords than we return True
            if coords == possible_coords:
                return True

        #If we get here than we know that the Pawn can't go to the given position so we return False
        return False

#This PIECES variable will be a tuple of all the pieces and thier positions in the
#tuple will dictate their position on the board
#it's diffcult to explain but hopefully it will make sense as you go through the code
PIECES = (
    Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook
)

class Application:
    def __init__(self, master = None):
        """This is the class where the main program will run"""
        self.master = tk.Tk() if master == None else master
        self.master.title("Chess")
        self.master.wm_state("zoomed")

        #creating the area were the board will be
        self.canvas = tk.Canvas(self.master, bg = "grey", highlightthickness = 0)
        self.canvas.pack(fill = "both", expand = True) #we want it to fill the screen

        #The pieces will be a dictionary of coordinates and the corresponding pieces
        self.pieces = {}

        #The board will be a dictionary of every tile and its corresponding text object
        self.board = {}

        #This will be a list of all the legal moves a piece can make when
        #the user clicks on that piece
        self.LegalMoves = []

        #This will be a list of tiles that pieces must go to when the game is in check
        self.MustGo = []

        self.CanGo = []

        #This will be a list of pieces that cannot move when the game is in check because those
        #pieces are protecting the King
        self.MustStay = []

        #This will be a list of all the legal moves avaiable to the King
        #At the start of every game the King will never have any legal moves
        self.LegalMovesForKing = []

        #This will be a list of all the moves that the players have made during the game
        self.move_history = []

        #When the size of the main window changes so should the board
        self.canvas.bind("<Configure>", self.ReDrawBoard)

        #When the user presses the f key the board should flip, swapping the position of all the pieces
        #This variable will just tell the program what state the board is currently in
        self.WhiteFirst = True
        self.master.bind("<f>", lambda event: self.FlipBoard())

        #When the user presses the cmd or ctrl z than the current move should be undone, when the
        #user presses shift cmd or ctrl z the move should than be redone
        self.master.bind("<Command-z>", lambda event: self.UndoMove())
        self.master.bind("<Shift-Command-z>", lambda event: self.RedoMove())
    def main(self):
        """This function resets all the main variables of the program, this will be done to reset
        the game when a player wins"""

        #Clearing all the dictionaries and lists so they don't interfer with the new game
        self.pieces.clear()
        self.board.clear()
        self.LegalMoves.clear()
        self.LegalMovesForKing.clear()
        self.MustGo.clear()
        self.CanGo.clear()
        self.MustStay.clear()

        #Resetting the player variable
        #This variable will be used by the program to know which player's turn it is
        self.player = 1

        #During the program there will be times when a pop-up is needed to tell the user
        #something such as a pawn promotion, so the program must know when a pop-up
        #occurs so it knows when to resize the pop-up and to ignore clicks the user preforms
        #that are not on the pop-up
        #This variable will be None when there isn't a pop-up but when there is a pop-up
        #this variable will be the function to call to resize the pop-up
        self.PopUpFunction = None

        #This variable will be used to record the position of a piece that is currently attacking
        #the King
        self.AttackingPiece = None

        #Clearing and reseting the move history list and the number_of_undos variable
        #this variable will be used to tell the program the current position we are in, in the
        #move_history list
        self.move_history.clear()
        self.number_of_undos = 0

        #Making an iterable of all the x coordinates
        #this way in order to get the next coordinate we just
        #have to use the built-in next function
        x_coords = iter("abcdefgh")

        for piece in PIECES:
            x = next(x_coords) #getting the next X coordinate

            #creating the black and white pieces
            white_piece = piece("white", x + "1", self.pieces, self.MustGo)
            black_piece = piece("black", x + "8", self.pieces, self.MustGo)

            #creating the black and white pawns
            white_pawns = Pawn("white", x + "2", self.pieces, self.MustGo)
            black_pawns = Pawn("black", x + "7", self.pieces, self.MustGo)

            #and now we just update the pieces dictionary to add these new
            #pieces into it
            self.pieces.update({
                x + "1": white_piece, x + "8": black_piece,
                x + "2": white_pawns, x + "7": black_pawns
            })

            if piece.__type__ == "King":
                #If the piece is a King we want to save the position of both kings
                self.KingPosition = {1: x + "1", 2: x + "8"}

        #The main difference between the pieces and board dictionaries
        #is that the pieces dictionary only stores the positions of pieces and the piece object itself
        #where as the board dictionary stores all the positions of every tile and its corresponding
        #text object

        #When the user clicks on a piece the program should show the user all the legal moves
        #that piece can make. So the program must know when a single click occurs
        #Orginally there was meant to be a tag_bind "<Button-1>" to each tile and text object
        #but I ran into a few problems so instead I decided to use a click bind to the entire
        #canvas object I could have solved the problem with the tag bind approuch but the code
        #would have ended up very messy and tangled so I used this method to make the code cleaner
        self.canvas.bind("<Button-1>", self.onClick)
    def ReDrawBoard(self, event = None):
        """This function gets called everytime the main window changes size. It will dynamically change
        the size of the board to fill the window"""

        #deleting the previous board
        self.canvas.delete("all")

        #determining the height and width of each tile on the board
        if event == None:
            #If the event is None than we will simply just use the current canvas width and height
            #which we can get through the winfo_width and winfo_height functions of the canvas
            #widget
            width = self.canvas.winfo_width() / 8
            height = self.canvas.winfo_height() / 8
        else:
            #Otherwise we use the width and height atrribute of the event
            width, height = event.width / 8, event.height / 8

        half_width, half_height = int(width) // 2, int(height) // 2

        #The font size of each test objects is always half the width of the tile
        #plus half the height of the tile
        #This way each piece will fill the tile without being too big or too small
        font_size = (half_width // 2) + (half_height // 2)

        #When the user clicks on a piece, green circles will show up
        #on all the tiles that piece can move to
        #by dividing the font size by 4 the circle will always be the same
        #size relative to the size of the tile
        self.radius = font_size // 4

        X,Y = 0,0 #Starting x and y coordinates

        range_y = range(8, 0, -1) if self.WhiteFirst is True else range(1, 9)

        for x in "abcdefgh":
            for y in range_y:
                #The chess board needs an alternating brown and white pattern
                colour = "brown" if ((ord(x) + y) % 2 == 0) else "light grey"

                coords = x + str(y) #the coordinates of the current tile

                #Creating the tile
                #The tag of each tile is its coordinates
                tile = self.canvas.create_rectangle(X, Y, X + width, Y + height, fill = colour, width = 0, tag = coords)

                #Getting the middle x and y coordinates of the current tile
                #To do this we must do "(x1 + x2) / 2" same with the y coordinates
                #But since x2 is always "x + width" we are doing (x1 + x1 + width) / 2
                #simplified it will end up being "x1 + (width / 2)"
                mid_x = X + half_width
                mid_y = Y + half_height

                #Every time time the board is resized a new text object is created for each tile
                #The text object object will display the chess peice
                #the text object is always at the mid point coordinates of the tile
                text_object = self.canvas.create_text(mid_x, mid_y, font = ("courier new", font_size))

                #And now just saving the text object to the board dictionary
                self.board[coords] = text_object

                #We now want to see if there is a piece on the current tile we are making
                #to do this we will use the get attribute of the dictionary
                #We will lookup our current tile coordsinates and if we get something
                #we will display that piece on the board otherwise we will just ignore it
                piece = self.pieces.get(coords) #if there is nothing a None will be retured
                if piece != None: #if a piece was found on this tile
                    #displaying the piece
                    self.canvas.itemconfigure(text_object, text = piece, fill = piece.colour)

                #We also now want to check if there were any green circles on the
                #board when it was resized if there was then we want to redraw those
                #circles. To do this we will check weather the coordinates of the
                #current tile we are making are in the legal moves list if they are then
                #we will draw the circle
                if coords in self.LegalMoves:
                    #using the self.radius variable to make sure that
                    #the size of each circle is correctly proportional to the size of the tiles
                    #this way no matter the size of the board the green circles will never
                    #appear be too big or too small
                    x1, x2 = (mid_x - self.radius), (mid_x + self.radius)
                    y1, y2 = (mid_y - self.radius), (mid_y + self.radius)

                    #creating the circle
                    #with a tag of "move" so it will be easy to delete all of them
                    #later on in the program
                    self.canvas.create_oval(x1, y1, x2, y2, fill = "#24E605", width = 0, tag = "move")

                Y += height #incrementing the Y varaiable by the height
            X += width #incrementing the X varaiable by the width
            Y = 0 #reseting the Y variable
        self.canvas.unbind("<ButtonRelease-1>")

        if self.PopUpFunction != None:
            #If this variable doesn't equal None than we know that there is currentluy a pop-up
            #on screen so we want to call the PopUpFunction to resize the pop-up
            self.PopUpFunction()
    def onClick(self, event):
        """This function is called whenever the user clicks on the canvas. It takes the event as an
        argument and from that will use the mouses x and y position to calculate which tile it
        is currently on top of using the find_overlapping function in the canvas class"""

        if self.PopUpFunction != None:
            #If this variable doesn't equal None than we know that there is a pop-up
            #on the screen so we don't want to take action on any clicks the user preforms
            return

        #The find_overlapping function will return a tuple of all the objects
        overlapping = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        if overlapping == ():
            #If the user presses somewhere without a tile there isn't anything we can do
            #so we exit the function with the return keyword
            return

        #Getting the tag of the tile
        #remember that each tile has its coordinates as its tag
        coords = self.canvas.itemcget(overlapping[0], "tag")

        #The reason for using the split function and turning it into a list and getting
        #the first element from that list is because sometimes we would have the coords variable
        #equal "{position} current" (don't know why?) so this way we can get the position of the
        #piece without having to worry about the "current" part at the end breaking the code
        coords = coords.split(" ")[0]

        if coords in self.LegalMoves:
            #If the user pressed a tile that was in the legal moves list then
            #we know that the user wants to move a piece
            self.MovePiece(self.SelectedPiece, coords)

            #once we've moved a piece there's no need to continue with this
            #function so we will exit the function with the return keyword
            return

        #When a Pawn reaches the end of the board for a promotion a pop-up will appear asking
        #the user which piece they want to promote the Pawn to, during this pop-up we don't
        #want the user to click on other pieces and move them, so we will create an invisbale
        #rectangle

        #If the legal move list is not empty and did not have a green circle on it
        #than we know that the user has clicked on a piece and has now clicked
        #on a different tile so we need to unselect that piece and remove the green circles
        #from the board
        if self.LegalMoves != []:
            #deleting all the green circles
            self.canvas.delete("move")
            #clearing the list
            self.LegalMoves.clear()

        piece = self.pieces.get(coords)

        if piece == None:
            #if piece equals none then there is no piece on that
            #tile that was clicked so there is nothing that we can do
            #so we just exit the function by returning nothing
            return
        if (self.player == 1 and piece.colour != "white") or (self.player == 2 and piece.colour != "black"):
            #If its currently player ones turn and the user clicks on a black piece or visa-vera than
            #there is nothing we can do, because we want it so that black pieces can only be moved
            #during player twos turn and white pieces only during player ones turn
            #So will exit the function with the return keyword
            return

        #If there was a piece on the clicked tile than now we must
        #find all of the legal moves that the clicked piece can make
        #using the find_legal_moves attribute that all piece objects have
        #except if the clicked piece was one of the Kings because instead we will use
        #the LegalMovesForKing list
        if piece.__type__ == "King":
            #Making moves equal to a copy of the LegalMovesForKing list
            moves = self.LegalMovesForKing.copy()
        else:
            #Getting the legal moves for that piece
            moves = piece.find_legal_moves()

        if self.MustStay != [] and coords in self.MustStay:
            #We have to check weather the clicked piece is in the MustStay list because if it is
            #than we know that we can't allow that piece to move as it is currently defending the King
            #so we can't do anything and just exit this function

            #But before that we also have to check if that piece can do something like attack the
            #attacking piece

            #Otherwise we make it so that the only move that piece can make is attacking that
            #piece
            legalMoves = moves.copy()
            moves = []
            for move in legalMoves:
                if self.AttackingPiece == move or move in self.CanGo:
                    moves.append(move)

        #clearing the list, this probally doen't need to be here the legal moves
        #list should be already cleared when it gets to this point in the code
        #but I kept it in just to make sure that the list was cleared before
        #the new legal moves where added
        self.LegalMoves.clear()

        #adding the moves to the list
        self.LegalMoves.extend(moves)

        self.SelectedPiece = coords

        #For every tile that a piece can move to, a green circle will appear on those tiles
        for tile in moves:
            #getting the x and y coordinates of the text object
            #this will always be the mid coordinates of the given tile
            x, y = self.canvas.coords(self.board[tile])

            #using the self.radius variable to make sure that
            #the size of each circle is correctly proportional to the size of the tiles
            #this way no matter the size of the board the green circles will never
            #appear be too big or too small
            x1, x2 = (x - self.radius), (x + self.radius)
            y1, y2 = (y - self.radius), (y + self.radius)

            #creating the circle
            #with a tag of "move" so it will be easy to delete all of them
            #later on in the program
            self.canvas.create_oval(x1, y1, x2, y2, fill = "#24E605", width = 0, tag = "move")

        #When the user clicks on a piece they should be able to drag and drop
        #the piece to the tile they want it to go to
        #In order to do this a release will be binded to the canvas to know when the user
        #has released the mouse as well as a B1-Motion will be binded to the canvas
        #to know when the user is pressing down the mouse and dragging the piece

        #Getting the mouse coordinates
        #This is important becuase when the user drags the mouse we will calculate
        #the differance between the mouses's current position and its new position
        #and then move the piece by that amount
        #The reason these are class attributes is becuase the mouse coordinates
        #need to change very often and the DragPiece function also needs to know the
        #mouses prvious coordinates by using these variables
        self.mouse_x = event.x
        self.mouse_y = event.y

        #A new text object must be made now for the user to drag
        #The user can't simply drag the text object as each tile must have its own
        #text object so moving that text object would mean we would have a tile without
        #a text object which means we can't put a piece in that tile in the future and
        #will break the game
        text_object = self.board[coords] #getting the text object

        #Now we are getting some values of the piece pressed such as the x and y coordinates
        #and font
        x, y = self.canvas.coords(text_object)
        font = self.canvas.itemcget(text_object, "font")

        font = font.split(" ")
        font[2] = str(int(font[2]) + 35)
        font = " ".join(font)

        #Creating the movable piece
        #the movable piece will have the tag "movable" so it will be easy for
        #other functions in the program to manipulate it
        self.canvas.create_text(x, y, text = piece, font = font, fill = piece.colour, tag = "movable")

        #Removing the current piece on this tile
        self.canvas.itemconfigure(text_object, text = "")

        #Binding the dragging action to the canvas so the user can drag the piece
        self.canvas.bind("<B1-Motion>", self.DragPiece)

        #Binding the mouse release to the canvas to the onRelease function
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.onRelease(event, coords))
    def onRelease(self, event, piece):
        """This function is called whenever the user presses and releases the mouse. It works
        by taking in the current coordinates of the mouse and uses those coordinates to
        calculate the tile underneath the mouse by using the find_overlapping function in the
        canvas class. It also takes in the current piece that the user dragged"""

        #Finding the tile underneath the mouse
        overlapping = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        if overlapping == ():
            #If the overlapping is empty than there is nothing we can do
            #so we exit the function
            return
        
        #Getting the tag of the tile
        #remember that each tile has its coordinates as its tag
        coords = self.canvas.itemcget(overlapping[0], "tag")
        coords = coords.split(" ")[0]

        #unbinding some events to the canvas object because the program doesn't need to deal
        #with those events for the time being
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        #Deleting the "movable" piece that the user was dragging as it has surved its purpose and
        #should now be deleted
        self.canvas.delete("movable")

        #Placing the dragged piece back on its orginal tile
        self.canvas.itemconfigure(self.board[piece], text = self.pieces[piece], fill = self.pieces[piece].colour)

        #We can only move the dragged piece if it was dragged to a tile that it can leaglly
        #move to so a check is preformed to make sure that the piece was dragged to a tile
        #that was in the LegalMoves list
        if coords in self.LegalMoves:
            self.MovePiece(piece, coords)
    def DragPiece(self, event):
        """This function is called whenever the mouse is dragged while pressed, this function
        simply just moves the piece across the board"""

        #Getting the current x and y positions of the mouse
        newMouseX = event.x
        newMouseY = event.y

        #Finding the difference between the new x and y coordinates and the old ones
        #this will tell us how much the mouse has moved by
        diff_x = newMouseX - self.mouse_x
        diff_y = newMouseY - self.mouse_y

        #Moving the piece now by how much the mouse has moved
        self.canvas.move("movable", diff_x, diff_y)

        #Updating the self.mouse x and y coordindates
        self.mouse_x = newMouseX
        self.mouse_y = newMouseY
    def MovePiece(self, old_coords, new_coords, undoing_move = False):
        """This function is used whenever a piece has to be moved on board. This function takes
        in the current position of the piece that we want to move as old_coords and the new position
        that we want to move to as new_coords"""

        if undoing_move is True:
            self.player = 3 - self.player

        if undoing_move is False and self.number_of_undos != 0:
            self.move_history = self.move_history[0:self.number_of_undos]
            self.number_of_undos = 0

        #getting the piece that we want to move
        piece = self.pieces[old_coords]

        #When a Pawn gets to the end of the board that pawn gets a promotion and can turn into
        #any other piece except the King and another Pawn
        if piece.__type__ == "Pawn" and new_coords[1:] in ("1","8"):
            #To let the user decide what piece they want to promote the Pawn to an
            #option menu will appear

            #A variable will be defined that will allow the program to remember
            #the position that the piece has to go to
            self.NewPosition = new_coords

            #Telling the program what function to call when the pop-up has to be resized
            self.PopUpFunction = self.PawnOptionMenu

            #Creating the pop-up
            self.PawnOptionMenu()

            #After creating the option menu we will exit this function
            #because there is nothing we can do until we know what the user wants to promote
            #the pawn into
            return
        elif piece.__type__ == "King":
            #If the piece moved is one of the kings than we need to update that kings position
            #Because the KingPosition is just a dictionary we can easily change its value
            self.KingPosition[self.player] = new_coords

        if self.number_of_undos == 0:
            self.move_history.append((old_coords, new_coords, self.pieces.get(new_coords, None)))

        #Deleting the current piece
        del self.pieces[old_coords]

        #Adding the piece back into the pieces dictionary with its new coordinates
        self.pieces[new_coords] = piece
   
        #Updating the position of the piece
        piece.UpdatePosition(new_coords)

        #Nothing should now be displayed on the tile that the piece came form
        self.canvas.itemconfigure(self.board[old_coords], text = "")

        #Displaying the piece on the new tile
        self.canvas.itemconfigure(self.board[new_coords], text = piece, fill = piece.colour)

        #Deleting all the grenn circles
        self.canvas.delete("move")

        #Clearing the legal moves list and the LegalMovesForKing list
        self.LegalMoves.clear()
        self.LegalMovesForKing.clear()

        if undoing_move is False:
            #Changing the player variable to the next player
            self.player = 3 - self.player

        #Now we just call this function to calculate the legal moves of the King and weather the
        #game is check, checkmate or stalemate
        self.master.after(1, self.EvaluateCurrentBoardState)
    def PawnOptionMenu(self):
        """This function will be called when the pop-up for the Pawn needs to be made or resized"""

        #Getting the coordinates needed to create the pop-up
        x1,y1 = self.canvas.coords(self.board["b6"])
        x2,y2 = self.canvas.coords(self.board["g3"])

        #The canvas object can't deal with floating point numbers for coordinates
        #So we must type cast all the coordinates we obtained into the int type
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        #Creating the pop-up with a rectangle on the board
        #But the rectangle is going to have rounded corners because it looks better that way
        #So we need to create a polygon with the below coordinates

        #Setting the radius variable for the corners of the rectangle
        radius = 50

        #This is the list of all the points we need to create the rounded rectangle
        #I just got this off the internet on StackOverflow
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

        #We give the rectangle the tag "popUp" so it will be easy to delete later in the program
        self.canvas.create_polygon(points, fill = "#0967F9", tag = "popUp", width = 1, smooth = True)

        #Calculating the width and height of the rectangle
        width = x2 - x1
        height = y2 - y1

        #When the pop-up is made there will be four options the user has to promote the Pawn to
        #A font_size will be calculated so the pieces on the pop-up will be the correct size
        #for the pop-up
        font_size = (width // 6) + (height // 6)

        #This will be the space between the pieces on the pop-up
        size = width // 4

        #Getting the mid y coordinates for the pieces to be placed on
        mid_y = (y1 + y2) // 2

        #Getting the colour of the piece
        colour = self.pieces[self.SelectedPiece].colour

        #Creating and placing the pieces on the pop-up
        for i in range(4):
            #For each iteration of the loop we create a unique piece
            if i == 0: piece = Queen
            elif i == 1: piece = Rook
            elif i == 2: piece = Bishop
            elif i == 3: piece = Knight

            #Getting the mid x coordinates for pieces to be placed on
            mid_x = (2 * x1 + size) // 2

            #Creating the piece on the pop-up
            text_object = self.canvas.create_text(mid_x, mid_y,
                text = piece.__str__(), font = ("courier new", font_size),
                activefill = "#F39A06", fill = colour, tag = "popUp"
            )

            #The purpose of this lambda function is diffcult to explain but know that
            #it is important and without it the program won't behave as expected
            #Basically because we are in a loop and the piece variable is constantly
            #changing this lambda function allows us to make a copy of the piece variable
            #otherwise everytime we called the PromotePawn function it would only use
            #the last known version of the piece variable which would be the Knight
            #but that isn't always what we want
            function = (lambda piece: lambda event: self.PromotePawn(piece))(piece)

            #Using this tag_bind to know when ever the user clicks on one of the pieces
            #so we know what piece to promote the Pawn into
            self.canvas.tag_bind(text_object, "<Button-1>", function)

            x1 += size
    def PromotePawn(self, promotion):
        """This function will be called when ever the Pawn needs to be promoted. All it does
        is transform the Pawn to the new piece and then call the MovePiece function to move
        the piece to the new position"""

        #Getting the colour of the Pawn that is going to be promoted
        colour = self.pieces[self.SelectedPiece].colour

        #Replacing the Pawn with the new piece we want to promote it too
        self.pieces[self.SelectedPiece] = promotion(colour, self.SelectedPiece, self.pieces, self.MustGo)

        #Resetting the PopUpFunction variable so the rest of the program knows the pop-up
        #is no longer up
        self.PopUpFunction = None

        #Deleting the pop-up
        self.canvas.delete("popUp")

        #Moving the new promoted Pawn to the piece the user was orginally moving it to
        self.MovePiece(self.SelectedPiece, self.NewPosition)

        old_coords, new_coords, piece = self.move_history.pop(-1)
        self.move_history.append(("Promotion", old_coords, new_coords, piece, promotion))
    def EvaluateCurrentBoardState(self):
        """At the end of every turn this function will be called to look at the board and
        evaluate the current board state and calculate weather the game must end either
        because it is at checkmate or stalemate. As well as that this function will also
        calculate the legal moves for the King of the player whooses turn it is next. It will
        also calculate if the King is in danger and must be protected"""

        #Resetting the AttackingPiece variables
        self.AttackingPiece = None

        #Clearing the MustGo and MustStay and CanGo lists
        self.MustGo.clear()
        self.CanGo.clear()
        self.MustStay.clear()

        #Getting the position of the King
        KingsPosition = self.KingPosition[self.player]

        #Getting all the possible moves for the King
        PossibleMovesForKing = self.pieces[KingsPosition].find_all_possible_moves()

        #Getting the colour of the King
        KingsColour = self.pieces[KingsPosition].colour

        #This variable will be incremented every time a piece is found attcking the King
        KingsAttackers = 0

        #Creating a loop and checking all the oppiste coloured pieces on the board
        for position, piece in self.pieces.items():
            if piece.colour == KingsColour:
                #If the colour of the piece is the same as the colour of the King than we know they
                #are on the same team so we will skip it and move on to the next piece
                continue

            if piece.can_go_to(KingsPosition) is True:
                #If a piece can go to the Kings position then we have to calculate if it is
                #check, checkmate or stalemate and weather we need to protect the King or end
                #the game

                #But before we do any of that we have to first calclaute if it is actaully possible
                #for the piece to attack the King because the can_go_to function of all the pieces
                #doesn't take into account weather there are any pieces inbetween the King and the
                #attacking piece so we have to do that here

                #To do this we will create a variable named protectors, than we will check all the
                #tiles between the King and the attacking piece and keep track of the number of pieces
                #we find, the last seen piece between the King and the attacking piece will be stored
                #in the lastSeenProtector variable as it may be important later on
                protectors = 0
                lastSeenProtector = None

                #A list of all the tiles inbetween the King and the attcking piece may be
                #needed later on in the program so we will create an empty list and store the
                #tiles in the list through out the loop
                inBetweenTiles = []

                if piece.__type__ == "Knight":
                    #If the piece is the Knight than there is no point checking the tiles between
                    #the King and the Knight as the Knigth can jump over pieces so we have to treat
                    #the Knight as a special case
                    KingsAttackers += 1
                else:
                    for tile in self.find_inbetween_tiles(KingsPosition, position):
                        PIECE = self.pieces.get(tile) #Getting the piece on the tile

                        if PIECE != None:
                            #If piece is not equal to None than there was a piece on that tile
                            protectors += 1 #So we add one to the protectors variable
                            lastSeenProtector = tile

                        #Adding the tile to the list
                        inBetweenTiles.append(tile)

                        if protectors == 2:
                            #If there are two or more pieces between the King and the attacking piece
                            #than there is no risk to the King so we can just break out of this loop
                            break

                    if protectors == 0:
                        #If there are no pieces inbetween the King and the attacking piece than
                        #the King is under attack so we just add one to the KingsAttackers variable
                        KingsAttackers += 1


                if protectors == 1 and self.pieces[lastSeenProtector].colour == KingsColour:
                    #If there is only one piece inbetween the King and the attacking piece and that
                    #piece is on the King's side than that piece can not move as it is defending the
                    #King
                    self.MustStay.append(lastSeenProtector)
                    self.CanGo.extend(inBetweenTiles)
                    self.AttackingPiece = position
                elif protectors == 0:
                    #If there are no pieces inbetween the King and attacking piece than some piece
                    #on the King's side must move inbetween them to protect the King or the King must
                    #move himself to safty
                    self.MustGo.extend(inBetweenTiles)
                    self.MustGo.append(position)

            for possible_move in PossibleMovesForKing[:]:
                #After checking the King's current position we have to do the same for all of his
                #possible moves, this is very similar to the above code but a little different

                if piece.can_go_to(possible_move) is True and possible_move != position:
                    #First we have to check if the current piece can attack the King, we also
                    #want to check that the piece isn't on a tile that the King can move to because
                    #if it is than the King can just eat the piece and there is no point doing
                    #any further calculations

                    #Just like before we create a protectors variable that will keep track
                    #of the number of pieces we find
                    protectors = 0

                    if piece.__type__ != "Knight":
                        #We only do this if the piece isn't a Knight because the Knight has the
                        #ability to jump over other pieces so what we're doing now would just be
                        #redunant and waste CPU time

                        for tile in self.find_inbetween_tiles(possible_move, position):
                            #Like before we find all the inbetween tiles and loop over them
                            #incrementing the protectors variable by 1 every time we find a
                            #piece

                            PIECE = self.pieces.get(tile) #Getting the piece on the tile

                            if PIECE != None:
                                #The PIECE variable will be equal to None if there is no piece on
                                #that tile so we just have to make sure that the PIECES variable
                                #does not equal None

                                if PIECE.__type__ == "King" and PIECE.colour == KingsColour:
                                    #When checking for a other pieces we don't want to count
                                    #the King so if we come across the King we don't do anything
                                    pass
                                else:
                                    #Otherwise if increment the protectors variable by one
                                    protectors += 1

                            if protectors >= 1:
                                #As long as there is one piece inbetween the King and the attacking
                                #piece than the King is safe and there is no need to continue with
                                #this loop so we just break out of it 
                                break

                    if protectors == 0:
                        #If there are no pieces inbetween the King and the attacking piece than
                        #the King can't move there so we just remove that move from the list of
                        #possible moves the King can do
                        PossibleMovesForKing.remove(possible_move)

        #Finally at the end of this we just add the contents of the PossiableMoves list to the
        #legal moves list
        self.LegalMovesForKing.extend(PossibleMovesForKing)

        if self.LegalMovesForKing == []:
            #If the King has no legal moves we than have to check that weather the game is
            #checkmate or stalemate or neither

            #To do this we will loop again through all the pieces on the board and check weather
            #any piece that is on the King's team has any legal moves, if they don't than we know
            #that the game is either checkmate or stalemate but if any piece still has any legal
            #move than the game will just continue as normal
            for position, piece in self.pieces.items():
                if piece.colour != KingsColour or piece.__type__ == "King":
                    #If the piece is not on the King's team or if the piece is a King
                    #than we will continue on with the loop to the next piece
                    continue

                #Getting a list of all the legal moves that the current piece can move to
                moves = piece.find_legal_moves()

                if position in self.MustStay:
                    #If the current piece is in the MustStay list it cannot move as it is
                    #defending the King and stopping him from being killed but we also have to
                    #check weather the piece can attack the attacking piece because than we know
                    #that if it can then that is a legal move the piece can make
                    if self.AttackingPiece in moves:
                        #If the position of the attacking piece is in the moves list for the
                        #current piece than that is the only move it can make
                        moves = [self.AttackingPiece]
                    else:
                        #Otherwise we make the moves list empty
                        moves = []

                if moves != []:
                    #When we find a piece which does have some legal moves than we will just break
                    #out of this loop as this means that the game is not in checkmate or stalemate
                    break
            else:
                #This else statement will only run if the for-loop hasn't been broken out of
                #meaning that no piece on the King's team had any legal moves

                if KingsAttackers == 0:
                    #If there are no pieces attacking the King and there are no legal
                    #moves for any piece on the King's team to make than the game is in
                    #Stalemate
                    messagebox.showinfo(title = "Chess", message = "Stalemate")
                else:
                    #Otherwise we know that the game is in checkmate so we will display a message for
                    #the user saying that it is checkmate and who the winner is

                    #Getting the colour of the winner
                    winner = "Black" if self.player == 1 else "White"

                    messagebox.showinfo(title = "Chess", message = "Checkmate", detail = winner + " Won")

                #Resetting all the game variables through the main function
                self.main()
                self.ReDrawBoard() #Redrawing the board
    @staticmethod
    def find_inbetween_tiles(first_position, second_position):
        """This function will be a generator function and calculate the inbetween tiles between two
        points and than return the coordinates of those tiles. This function uses the yield keyword
        to return the coordinates of the tile straight after it has calculates as this means the
        program doesn't have to wait until this function has found every tile and returned an
        entire list but instead as soon as this function as found a tile it will tell the program and
        it can act on it straight away without having to wait for this function"""

        #Getting the x and y coordinates of all the positions
        x1 = ord(first_position[0])
        y1 = int(first_position[1:])

        x2 = ord(second_position[0])
        y2 = int(second_position[1:])

        try:
            #Calculating the gradient of line between the two given points
            gradient = (y1 - y2) / (x1 - x2)
        except ZeroDivisionError:
            #However if the both x coordinates are the same than when we subtract them
            #we will get zero and then we will have to divide by zero which we can't do
            #so instead we will just make the gradient 0
            gradient = 0

        if x1 == x2:
            #If both x coordinates are the same than we know that the movement is vertical and
            #can calculate the tiles inbetween just by starting from the lowest y coordinate and
            #going up until we hit the highest y coordinate(It will hopfully make more sence as you
            #read the code)

            #Finding the lowest and highest y coordinates
            min_y = y1 if y1 < y2 else y2
            max_y = y2 if y1 == min_y else y1

            for y in range(min_y + 1, max_y):
                yield f"{chr(x1)}{y}"
        elif y1 == y2:
            #This is the same as the one above if both y coordinates are the same than we know that
            #the movement is horizontal and can calculate the tiles inbetween tile the same way the 
            #only difference is we are going to have to increment the x coordinate

            #Finding the higher and lower x coordinates
            min_x = x1 if x1 < x2 else x2
            max_x = x2 if x1 == min_x else x1

            for x in range(min_x + 1, max_x):
                yield f"{chr(x)}{y1}"
        elif abs(gradient) == 1:
            #If the absolute value of the gradient is 1 than we know the movement was daiognal and
            #can use that to calculate the inbetween tiles

            #These variables will tell us weather we have to add or subtract 1 from the x1 and y1
            #variables to get x2 and y2
            x_movement = -1 if x1 - x2 >= 0 else 1
            y_movement = -1 if y1 - y2 >= 0 else 1

            #Creating two variables x and y than will be equal to x1 and y1 and that will
            #be added to during the program until they equal x2 and y2
            x = x1
            y = y1

            #By finding the absolute difference between x1 and x2 and than taking away 1 we will
            #than know the number of tiles we have to iterate through
            for i in range(abs(x1 - x2) - 1):
                #Adding to the x and y coordinates
                x += x_movement
                y += y_movement

                yield f"{chr(x)}{y}"
    def FlipBoard(self):
        """This function is pretty self explanatory, it just flips the board around"""
        self.WhiteFirst = not self.WhiteFirst
        self.ReDrawBoard()
    def UndoMove(self):
        if self.PopUpFunction != None:
            return

        try:
            self.number_of_undos -= 1
            previous_move = self.move_history[self.number_of_undos]
            #previous_move = self.move_history.pop(-1)
        except IndexError:
            return
        
        if previous_move[0] == "Promotion":
            old_coords = previous_move[1]
            new_coords = previous_move[2]
            piece = previous_move[3]
            promotion = previous_move[4]

            colour = self.pieces[new_coords].colour
            self.pieces[new_coords] = Pawn(colour, new_coords, self.pieces, self.MustGo)
        else:
            old_coords = previous_move[0]
            new_coords = previous_move[1]
            piece = previous_move[2]

        self.MovePiece(new_coords, old_coords, True)

        if piece != None:
            self.pieces[new_coords] = piece
            self.canvas.itemconfigure(self.board[new_coords], text = piece, fill = piece.colour)
    def RedoMove(self):
        if self.PopUpFunction != None:
            return

        try:
            previous_move = self.move_history[self.number_of_undos]
        except IndexError:
            return

        if previous_move[0] == "Promotion":
            old_coords = previous_move[1]
            new_coords = previous_move[2]
            piece = previous_move[3]
            promotion = previous_move[4]

            colour = self.pieces[old_coords].colour
            self.pieces[old_coords] = promotion(colour, old_coords, self.pieces, self.MustGo)
        else:
            old_coords = previous_move[0]
            new_coords = previous_move[1]

        try:
            self.MovePiece(old_coords, new_coords, True)
        except KeyError:
            self.player = 3 - self.player
            return
        else:
            self.number_of_undos += 1
def main():
    root = tk.Tk() #creating the main window
    app = Application(root)
    app.main()
    root.mainloop()

if __name__ == "__main__":
    main()
