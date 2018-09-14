# This module contains the behind-the-scenes functions that 
# are called on by the central functions

## Contained Functions ##

# Boolean Check Functions
# numPieces
# onBoard
# isSquare
# checkEmpty

# Piece Selection Functions
# findPiece
# checkPiece
# takePiece

# Mouse Click Functions
# getClick
# endClick




##########################  Boolean Check Functions  ##########################

# Counts the number of pieces left on the board, returns tuple (red,black)
def numPieces(red_piece, black_piece):
    return (len(red_piece), len(black_piece))


# Checks if coordinates are on playing board
def onBoard(x, y):
    if x < 9 and y < 9 and x > 0 and y > 0:
        return True

    return False

# Checks if it is a valid checkers square(pieces can move there)
def isSquare(x,y):

    if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
        return True
    else:
        return False

# Check if square is empty
def checkEmpty(red_piece, black_piece,x ,y):

    for piece in red_piece:
        if piece.getX() == x and piece.getY() == y:
            return False

    for piece in black_piece:
        if piece.getX() == x and piece.getY() == y:
            return False

    return True


#########################  Piece Selection Functions  #########################

# Returns index of piece on a given square
def findPiece(red_piece, black_piece, x, y, color):
    if color == "red":
        for piece in red_piece:
            if piece.getX() == x and piece.getY() == y:
                return red_piece.index(piece)
                
    else:
        for piece in black_piece:
            if piece.getX() == x and piece.getY() == y:
                return black_piece.index(piece)

    return "No matching piece"

# Checks if a piece (of either) colour is on a given square
def checkPiece(red_piece, black_piece, x, y, color):
    if color == "red":
        for piece in red_piece:
            if piece.getX() == x and piece.getY() == y:
                return True
                
    else:
        for piece in black_piece:
            if piece.getX() == x and piece.getY() == y:
                return True

    return False

# Performs the capturing action - moves piece, deletes taken piece
def takePiece(red_piece, black_piece, x1, y1, x2, y2, color):

    midx = x1 + (x2 - x1)/2
    midy = y1 + (y2 - y1)/2

    #print color
    if color == "black":

        index = findPiece(red_piece, black_piece, midx, midy, "red")
        del red_piece[index]

        index = findPiece(red_piece, black_piece, x1, y1, color)
        black_piece[index].move(x2, y2)

    else:

        index = findPiece(red_piece, black_piece, midx, midy, "black")
        del black_piece[index]

        index = findPiece(red_piece, black_piece, x1, y1, color)
        red_piece[index].move(x2, y2)



###########################  Mouse Click Functions  ###########################

# Gets mouse click, returns true if clicked on player's own piece
def getClick(window, color, red_piece, black_piece):
        
    while True:        
        point = window.getMouse()
        x = int(point.getX()) / 60
        y = int(point.getY()) / 60
        
        if onBoard(x,y) and isSquare(x,y):
            #used to be selectPiece
            click = checkPiece(red_piece, black_piece,x,y,color)

            if click == True:
                break
    return (x,y)

# Gets second (end) mouse click, makes sure the square is empty
def endClick(window, color, red_piece, black_piece):
    
    while True:        
        point = window.getMouse()
        x = int(point.getX()) / 60
        y = int(point.getY()) / 60

    
        if onBoard(x,y) and isSquare(x,y) and checkEmpty(red_piece, black_piece, x,y):
            return (x,y)        
