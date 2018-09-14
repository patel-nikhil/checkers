from graphics import *
from Utilities import *
from ResetGame import *

# Solves for center of piece for drawing circle
def center(a,b):
    x = a * 60 + 30
    y = b * 60 + 30

    return Point(x,y)

# Draws the piece on the board
def drawPiece(window, x, y, color):
    piece = Circle (center(x,y), 25)
    piece.setFill(color)
    piece.draw(window)

# Fills a square - use for when piece moves
def drawBox(window, x, y):
    end1 = Point(x * 60, y * 60)
    end2 = Point(x * 60 + 60, y * 60 + 60)
    box = Rectangle(end2, end1)
    box.setFill("dark green")
    box.draw(window)



# Checks for forced captures
def checkCapture(red_piece, black_piece, color):

    count = 0    
    for x in range (1,9):
        for y in range (1,9):
            if isSquare (x,y):
                
                if checkPiece(red_piece, black_piece, x, y, color):
                    
                    if validCapture(color, red_piece, black_piece,x,y,x+2,y+2):
                        #print "A"
                        count += 1

                    elif validCapture(color, red_piece, black_piece,x,y,x+2,y-2):
                        #print "B"
                        count += 1

                    elif validCapture(color, red_piece, black_piece,x,y,x-2,y+2):
                        #print "C"
                        count += 1

                    elif validCapture(color, red_piece, black_piece,x,y,x-2,y-2):
                        #print "D"
                        count += 1
    return count


# Check for an additional capture
def secondCapture (color, red_piece, black_piece, x1, y1):

    end_x = []
    end_y = []
    
    for i in range (-2, 3, 4):
        for j in range (-2, 3, 4):

            if validCapture(color, red_piece, black_piece, x1, y1, x1 + i, y1 + j):
                end_x.append(x1 + i)
                end_y.append(y1 + j)

    return [end_x, end_y]


# Checks if move is valid (if piece is king, moving right way on the board)
def validMove(red_piece, black_piece, x1, y1, x2, y2, color):

    if onBoard(x2,y2) == False:        
        return False

    if checkEmpty(red_piece, black_piece,x2,y2) == False:
        return False

    index = findPiece(red_piece, black_piece, x1, y1, color)
    if color == "red":
        king = red_piece[index].isKing()
    else:
        king = black_piece[index].isKing()
    
    # Checks piece is moving right way
    if king == False:
        if abs (x1 - x2) == 1 and abs(y1 - y2) == 1:
            if color == "red":
                if y2 > y1:
                    return True
            else:
                if y1 > y2:
                    return True
    else:
        if abs (x1 - x2) == 1 and abs(y1 - y2) == 1:
            return True
            
    return False


# Checks if valid capture can be made given start and end points
def validCapture(color, red_piece, black_piece, x1, y1, x2, y2):

    if onBoard(x2,y2) == False:
        return False

    if checkEmpty(red_piece, black_piece,x2,y2) == False:
        return False

    # Location of 'captured' piece
    midx = x1 + (x2 - x1)/2
    midy = y1 + (y2 - y1)/2

    index = findPiece(red_piece, black_piece, x1, y1, color)
    if color == "red":
        king = red_piece[index].isKing()
    else:
        king = black_piece[index].isKing()


    # Check if capture is possible (piece to be jumped, end (x,y) right
    if king == False:
        if color == "red" and checkPiece(red_piece, black_piece, midx, midy, "black"):
            if abs(x2 - x1) == 2 and y2 - y1 == 2:                
                return True
        elif color == "black" and checkPiece(red_piece, black_piece, midx, midy, "red"):
            if abs(x2 - x1) == 2 and y1 - y2 == 2:
                return True
    else:
        if color == "red" and checkPiece(red_piece, black_piece, midx, midy, "black"):
            if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:                
                return True
        elif color == "black" and checkPiece(red_piece, black_piece, midx, midy, "red"):
            if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                return True

    return False


# Returns overall threat level based on location of pieces on board
def isThreatened(red_piece, black_piece, color, iteration):

    threat = 0.0
    safety = 0.0
    attack = 0.0
    power = 0.0
    if color == "black":

        for piece in black_piece:
            
            x = piece.getNew_X()
            y = piece.getNew_Y()
            if piece.isKing():
                power += 1
            for i in range(-1,3,2):
                for j in range(-1,3,2):
                    if onBoard(x + i, y + j) and isSquare(x + i, y + j):

                        if checkPiece(red_piece, black_piece, x + i, y + j, "red"):
                            place = findPiece(red_piece, black_piece, x + i, y + j, "red")
                            if red_piece[place].isKing():
                                threat += 0.2
                            else:
                                threat += 0.1
                    elif isSquare(x + i, y + j):
                        #Edge of board
                        safety -= 1

        for piece in black_piece:
            
            x1 = piece.getX()
            y1 = piece.getY()
            for i in range(-2,3,4):
                for j in range(-2,3,4):

                    valid = validCapture(color, red_piece, black_piece, x1, y1, x1 + i, y1 + j)
                    if valid:
                        threat -= 2

                        x2 = x1 + i
                        y2 = y1 + j
                        midx = x1 + (x2 - x1)/2
                        midy = y1 + (y2 - y1)/2
                        index = findPiece(red_piece, black_piece, midx, midy, "red")
                        if red_piece[index].isKing():
                            attack -= 1
    try:
        score = (float(power)/attack)**2 + (float(safety)/threat)**2
    except ZeroDivisionError:
        score = power**2 + attack**2 + safety*2 - threat**2
        #score = power + attack + safety - threat
    
    return [score, iteration]
  

# A regular user move
def regularMove(window, color, red_piece, black_piece):    

    index = 12
    while True:
        start = getClick(window, color, red_piece, black_piece)
        end = endClick(window, color, red_piece, black_piece)
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        if validMove(red_piece, black_piece, x1, y1, x2, y2, color):
            index = findPiece(red_piece, black_piece, x1, y1, color)
            break

    red_piece[index].move(x2,y2)

    drawBox(window, x1,y1)
    drawPiece(window,x2,y2,color)


# A user capture move
def captureMove(window, color, red_piece, black_piece):

    while True:

        start = getClick (window, color, red_piece, black_piece)    
        end = endClick(window, color, red_piece, black_piece)
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        if validCapture(color, red_piece, black_piece, x1, y1, x2, y2):
            break

    midx = x1 + (x2 - x1)/2
    midy = y1 + (y2 - y1)/2

    takePiece (red_piece, black_piece, x1, y1, x2, y2, color)

    drawBox(window, x1,y1)
    drawBox(window, midx, midy)
    drawPiece(window, x2,y2, color)

    update_pieces(red_piece, black_piece)

    # Multijump code
    click = True
    move2 = secondCapture (color, red_piece, black_piece, x2, y2)

    # Wait for click on end square
    while move2[0]:
        while click:

            end = endClick(window, color, red_piece, black_piece)
            for option in range (len(move2[0])):
                if move2[0][option] == end[0] and move2[1][option] == end[1]:
                    click = False
                    

        midx = x2 + (end[0] - x2)/2
        midy = y2 + (end[1] - y2)/2
        
        takePiece (red_piece, black_piece, x2, y2, end[0], end[1], color)

        move2 = secondCapture (color, red_piece, black_piece, end[0], end[1])        

        drawBox(window, x2,y2)
        drawBox(window, midx, midy)
        drawPiece(window, end[0],end[1], color)


# A regular AI move
def reg_AI_Move (window, color, red_piece, black_piece, count):

    score = 9999
    move = []

    if color == "black":

        for piece in black_piece:

            x1 = piece.getX()
            y1 = piece.getY()

            for i in range(-1,2,2):
                for j in range(-1,2,2):

                    valid = validMove(red_piece, black_piece, x1, y1, x1 + i, y1 + j, color)
                    if valid:
                        piece.setNew_xy(x1 + i, y1 + j)
                        threat = isThreatened (red_piece, black_piece, color, count)
                        if score > threat[0]:
                            score = threat[0]
                            num = piece.getIndex()
                            best = [x1 + i, y1 + j]                            
                        elif score == threat[0]:                                
                            num = piece.getIndex()
                            best = [x1 + i, y1 + j]
                        else:
                            pass

                        piece.setNew_xy(x1, y1)

        if count == 15:                    
            startX, startY = black_piece[num].getX(), black_piece[num].getY()
            black_piece[num].move(best[0],best[1])

            drawPiece(window, best[0], best[1], color)
            drawBox(window,startX, startY)

        else:
            count += 1
            reg_AI_Move (window, color, red_piece, black_piece, count)
            

# AI Capture Move
def AI_capture(window, color, red_piece, black_piece, mult, count):

    score = 9999
    num = 20
    if mult:

        if color == "black":

            for piece in black_piece:
        
                x1 = piece.getX()
                y1 = piece.getY()

                for i in range(-2,3,4):
                    for j in range(-2,3,4):
                        
                        if validCapture(color, red_piece, black_piece, x1, y1, x1 + i, y1 + j):
                            
                            threat = isThreatened (red_piece, black_piece, color, count)
                            #print score
                            #print threat
                            if score > threat[0]:
                                score = threat[0]
                                num = piece.getIndex()
                                best = [x1 + i, y1 + j]
                                piece.setNew_xy(x1, y1)
                            elif score == threat[0]:
                                piece.setNew_xy(x1, y1)                                
                                num = piece.getIndex()
                                best = [x1 + i, y1 + j]
                            else:
                                piece.setNew_xy(x1, y1)                            
                            
                            piece.setNew_xy(x1 + i, y1 + j)

            #print "index", num

            startX, startY = black_piece[num].getX(), black_piece[num].getY()
            black_piece[num].move(best[0],best[1])
        
            midx = startX + (best[0] - startX)/2
            midy = startY + (best[1] - startY)/2

            #print startX, startY, best[0], best[1]
            #print "To be taken", midx, midy

            index = findPiece(red_piece, black_piece, midx, midy, "red")
            del red_piece[index]
            

            drawPiece(window, best[0], best[1], color)
            drawBox(window,startX, startY)
            drawBox(window,midx, midy)

    else:

        if color == "black":        
            for piece in black_piece:

                for i in range(-2, 3, 4):
                    for j in range(-2, 3, 4):

                        x1 = piece.getX()
                        y1 = piece.getY()

                        x2 = x1 + i
                        y2 = y1 + j

                        capture = validCapture(color, red_piece, black_piece, x1, y1, x2, y2)
                        if capture:
                            piece.move(x2,y2)                            
                            break

                    if capture:
                        break

                if capture:
                    break


            midx = x1 + (x2 - x1)/2
            midy = y1 + (y2 - y1)/2

            index = findPiece(red_piece, black_piece, midx, midy, "red")
            del red_piece[index]

            drawPiece(window, x2, y2, "black")
            drawBox(window, midx, midy)
            drawBox(window, x1, y1)
