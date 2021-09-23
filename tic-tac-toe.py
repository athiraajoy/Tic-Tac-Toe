import pygame as pg
import sys
import time
from pygame.locals import *

# sets values to use to start window
width = 400
height = 400

# X starts the game (first turn) so XO is x
XO = 'x'
player = 'o'
opponent = 'x'

white = (255, 255, 255)
line_color = (0, 0, 0)

pg.init()

# starts with empty board
board = [[None]*3, [None]*3, [None]*3]

screen = pg.display.set_mode((width, height + 100))

# added window title
pg.display.set_caption("Tic-Tac-Toe Using Minimax")

# takes images from folder to show at loading screen and to print inside squares
initiating_window = pg.image.load("1.png")
x_img = pg.image.load("2.png")
y_img = pg.image.load("3.png")

#image resizing
initiating_window = pg.transform.scale(
    initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


winner = None

draw = None

# prints the current status of the game i.e, who won, or whose turn it is
def draw_status():

    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won !"
    if draw:
        message = "Game Draw !"

    font = pg.font.Font(None, 30)

    text = font.render(message, 1, (255, 255, 255))

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()


# prints X or O at position given by the user_click() function
def drawXO(row, col):
    global board, XO

    if row == 1:
        posx = 30

    if row == 2:
        posx = width / 3 + 30

    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30

    if col == 2:
        posy = height / 3 + 30

    if col == 3:
        posy = height / 3 * 2 + 30
    board[row-1][col-1] = XO

    if(XO == 'x'):
        screen.blit(x_img, (posy, posx))
        XO = 'o'
        f, k = findBestMove(board)  # function called so the game can continue onto the next turn
        win, draw = evaluate(board, 0)  # decides what to do according to the status of the game
        time.sleep(1)
        if(win == None and (draw == False or draw == None)):
            drawXO(f+1, k+1)

    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()

# checks if there are any empty spaces left on the board and returns bool value
def isMovesLeft(b):
    for i in range(3):
        for j in range(3):
            if (b[i][j] == None):
                return True
    return False

# check for winning conditions
# if val=0, draws line over the winning player
# if val=1, returns the score depending on who won the game
def evaluate(b, val):
    global board, winner, draw
    for row in range(3):
        if ((b[row][0] == b[row][1] and b[row][1] == b[row][2]) and (board[row][0] is not None)):
            if (val == 1):
                if (b[row][0] == player):
                    return +10
                elif (b[row][0] == opponent):
                    return -10
            else:
                winner = board[row][0]
                pg.draw.line(screen, (250, 0, 0), (0, (row + 1)*height / 3 -
                                                   height / 6), (width, (row + 1)*height / 3 - height / 6), 4)
                break

    for col in range(3):
        if ((b[0][col] == b[1][col] and b[1][col] == b[2][col]) and (board[0][col] is not None)):
            if (val == 1):
                if (b[0][col] == player):
                    return +10
                elif (b[0][col] == opponent):
                    return -10
            else:
                winner = board[0][col]
                pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 -
                                                   width / 6, 0), ((col + 1) * width / 3 - width / 6, height), 4)
                break

    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) and (board[0][0] is not None):
        if (val == 1):
            if (b[0][0] == player):
                return +10
            elif (b[0][0] == opponent):
                return -10
        else:
            winner = board[0][0]
            pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) and (board[0][2] is not None):
        if(val == 1):
            if (b[0][2] == player):
                return +10
            elif (b[0][2] == opponent):
                return -10
        else:
            winner = board[0][2]
            pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if(val == 1):
        return 0
    else:
        if(all([all(row) for row in board]) and winner is None):
            draw = True
        draw_status()
        return(winner, draw)

# tries each possible move recursively and returns the best score available at that point
def minimax(b,  depth, isMax):
    score = evaluate(b, 1)

    if (score == 10):
        return score

    if (score == -10):
        return score

    if (isMovesLeft(b) == False):
        return 0

    if (isMax):
        best = -1000
        for i in range(3):
            for j in range(3):
                if (b[i][j] == None):
                    b[i][j] = player
                    best = max(best, minimax(b, depth+1, not isMax))
                    b[i][j] = None
        return best

    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if (b[i][j] == None):
                    b[i][j] = opponent
                    best = min(best, minimax(b, depth+1, not isMax))
                    b[i][j] = None
        return best

# depending on the score returned by the minimax algorithm
# this function finds the row and column of the best move and sends it to drawXO to print it
def findBestMove(b):
    bestVal = -1000
    bestMover = -1
    bestMovec = -1
    for i in range(3):
        for j in range(3):
            if (b[i][j] == None):
                b[i][j] = player
                moveVal = minimax(b, 0, False)
                b[i][j] = None
                if (moveVal > bestVal):
                    bestMover = i
                    bestMovec = j
                    bestVal = moveVal
    return(bestMover, bestMovec)


# controls the basic UI of the game
# defines each element of the UI and draws them inside the window 
def game_initiating_window():

    screen.blit(initiating_window, (0, 0))

    pg.display.update()
    time.sleep(2)
    screen.fill(white)

    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 3)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0),
                 (width / 3 * 2, height), 3)

    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 3)
    pg.draw.line(screen, line_color, (0, height / 3 * 2),
                 (width, height / 3 * 2), 3)
    draw_status()
    pg.display.update()


game_initiating_window()


# finds the coordinate of where the mouse was clicked and sends the row and col to drawXO function
def user_click():
    x, y = pg.mouse.get_pos()
    if(x < width / 3):
        col = 1

    elif (x < width / 3 * 2):
        col = 2

    elif(x < width):
        col = 3

    else:
        col = None

    if(y < height / 3):
        row = 1

    elif (y < height / 3 * 2):
        row = 2

    elif(y < height):
        row = 3

    else:
        row = None

    print(row, col, board[row-1][col-1])
    if(row and col and board[row-1][col-1] is None):
        global XO
        drawXO(row, col)
        evaluate(board, 0) #checks if any player has won after the move was made
        

# resets board to empty and first turn to X
def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    winner = None
    game_initiating_window()
    board = [[None]*3, [None]*3, [None]*3]

# infinte loop controls game depending on what the user is doing
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            user_click()
            if(winner or draw):
                reset_game()
    pg.display.update()
