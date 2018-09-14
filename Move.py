from RegularMove import *

# User Move
def UserMove(window, color, red_piece, black_piece):

    user_capture = checkCapture(red_piece, black_piece, color)
    #print "User Capture", user_capture
    if user_capture:
        captureMove(window, color, red_piece, black_piece)

    else:
        regularMove(window, color, red_piece, black_piece)


# AI Move
def AI_Move(window, color, red_piece, black_piece):

    ai_capture = checkCapture(red_piece, black_piece, "black")
    #print "AI Capture", ai_capture
    
    if ai_capture == 1:        
        AI_capture(window, color, red_piece, black_piece, False,5)        
    elif ai_capture > 1:        
        AI_capture(window, color, red_piece, black_piece, True,5)
    else:        
        reg_AI_Move(window, color, red_piece, black_piece,0)
