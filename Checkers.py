from graphics import *
from ResetGame import *
from Move import *


def main():

    window = GraphWin (title="Checkers", width=800, height=600)
    window.setCoords(0,0,600,600)

    red_piece = []
    black_piece = []

    
    resetGame(window, red_piece, black_piece)

    while len(red_piece) > 0 and len(black_piece) > 0:


        UserMove(window,"red",red_piece, black_piece)
        update_pieces(red_piece, black_piece)

        if len(red_piece) < 0 or len(black_piece) < 0:
            break
        else:
            AI_Move(window, "black", red_piece, black_piece)
            update_pieces(red_piece, black_piece)
    
    window.close()

main()

## For debugging only
#        for piece in black_piece:
#            print "Black Piece at", piece.getX(), piece.getY()

#        for piece in red_piece:
#            print "Red Piece at", piece.getX(), piece.getY()
