from graphics import *

class Piece:

    def __init__(self, color, x, y, index):
        self.color = color
        self.x = x
        self.y = y
        self.king = False
        self.new_x = self.x
        self.new_y = self.y
        self.index = index
        self.test()


    def move(self, x, y):
        self.x = x
        self.y = y
        self.test()

        if self.color == "red" and self.y == 8:
            self.makeKing()
        elif self.color == "black" and self.y == 1:
            self.makeKing()

    def test(self):
        self.new_x = self.x * 1
        self.new_y = self.y * 1

    def setNew_xy(self, x,y):
        self.new_x = x
        self.new_y = y

    def taken(self):
        self.x = 0
        self.y = 0
        self.king = False

    def makeKing(self):
        self.king = True

    def setIndex(self, index):
        self.index = index

    def getColor(self):
        return self.color

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNew_X(self):
        return self.new_x

    def getNew_Y(self):
        return self.new_y

    def getIndex(self):
        return self.index

    def isKing(self):
        return self.king


def resetGame(window, red_piece, black_piece):
    drawBoard(window)
    #test_init(window, red_piece, black_piece)
    initPieces(window, red_piece, black_piece)

# Draws the checkerboard to window object
def drawBoard(window):    
    
    for i in range(1,9):
        for j in range (1,9):
            
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                colour = "dark green"
            else:
                colour = "white"

            end1 = Point(i * 60,j * 60)
            end2 = Point(i * 60 + 60, j * 60 + 60)
            box = Rectangle(end2, end1)
            box.setFill(colour)
            box.draw(window)    

# Draws pieces and stores Piece objects in their respective lists
def initPieces(window, red_piece, black_piece):

    index = 0
    for y in range (1,4):
        for x in range (1,9):

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                piece = Circle (center(x,y), 25)
                piece.setFill("red")
                piece.draw(window)
                red_piece.append (Piece("red", x,y,index))
                index += 1
                
    index = 0
    for y in range (6,9):
        for x in range (1,9):

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                piece = Circle (center(x,y), 25)
                piece.setFill("black")
                piece.draw(window)
                black_piece.append(Piece("black",x,y, index))
                index += 1

# Returns point where center of piece will be drawn
def center(a,b):

    x = a * 60 + 30
    y = b * 60 + 30

    return Point(x,y)

# Updates the index of pieces based on location in list
# For when captures are made and pieces deleted from list
def update_pieces(red_piece, black_piece):

    for i in range(len(red_piece)):
        red_piece[i].setIndex(i)

    for j in range(len(black_piece)):
        black_piece[j].setIndex(j)

# Draws pieces and stores Piece objects in their respective lists
def test_init(window, red_piece, black_piece):

    index = 0
    for y in range (1,2):
        for x in range (3,5):

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                piece = Circle (center(x,y), 25)
                piece.setFill("red")
                piece.draw(window)
                red_piece.append (Piece("red", x,y,index))
                index += 1
                
    index = 0
    for y in range (8,9):
        for x in range (5,7):

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                piece = Circle (center(x,y), 25)
                piece.setFill("black")
                piece.draw(window)
                black_piece.append(Piece("black",x,y, index))
                index += 1
