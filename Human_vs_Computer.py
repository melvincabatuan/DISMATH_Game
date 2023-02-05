import pygame as pg
import numpy as np
from pygame.locals import *

# Import local modules
import Basic_Operation
import Pygame_Plotting
import Mini_Max_and_Alpha_Beta

# Initialize constant values
Nx = 8               # Board size, 8 x 8
grid_size = 64
Lx = 600             # Window size, Lx x Ly
Ly = 600
margin_x = (Lx-Nx*grid_size)//2  # margin is 44
margin_y = (Ly-Nx*grid_size)//2

side = 1
red_win = False
white_win = False

max_eva = 100
alpha = -200.    # - infinity
beta = -alpha    # + infinity

global king_value
king_value = 2   # king is valued twice as the normal piece

global man_value
man_value = 1

score = 0

step_fr_w = 9  # forward_right
step_fl_w = 7  # forward_left
step_br_w = -7  # backward_rigt
step_bl_w = -9  # backward_left

step_fr_r = -7  # forward_right
step_fl_r = -9  # forward_left
step_br_r = 9  # backward_right
step_bl_r = 7  # backward_left

# White pieces location 
man_w = [1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23]
king_w = []

# Black pieces location 
man_r = [40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]
king_r = []

pg.init()

FLIP = False
FPS = 30  # frame per second
#clock = pg.time.Clock()

WINDOWS = pg.display.set_mode((Lx, Ly))
pg.display.set_caption('DISMATH Checkers Game')
icon = pg.image.load('images/CHECKER_RED.png')
pg.display.set_icon(icon)

# DAMATH Style Board
operations = [' ', '∧', ' ', '⇔', ' ', '⇒', ' ', '∨',
              '⇔', ' ', '∧', ' ', '∨', ' ', '⇒', ' ',
              ' ', '⇒', ' ', '∨', ' ', '∧', ' ', '⇔',
              '∨', ' ', '⇒', ' ', '⇔', ' ', '∧', ' ',
              ' ', '∧', ' ', '⇔', ' ', '⇒', ' ', '∨',
              '⇔', ' ', '∧', ' ', '∨', ' ', '⇒', ' ',
              ' ', '⇒', ' ', '∨', ' ', '∧', ' ', '⇔',
              '∨', ' ', '⇒', ' ', '⇔', ' ', '∧', ' ']

# Initialize / Plot board
BOARD = Pygame_Plotting.Plotting(
    Nx, grid_size, margin_x, margin_y, Lx, Ly, man_value, king_value, FLIP, WINDOWS, operations)

# Initialize Checkers_Basic object
CHECKERS = Basic_Operation.Checkers_Basic(Nx, man_value, king_value, step_fr_r, step_fl_r, step_br_r, step_bl_r, step_fr_w, step_fl_w, step_br_w, step_bl_w, man_r, man_w, king_r, king_w, operations)

# Initialize pruning  object
COMPUTER_MOVE = Mini_Max_and_Alpha_Beta.pruning(
    Nx, max_eva, man_value, king_value, CHECKERS)

# First Criteria for score: Chips left
checkers = [0]*(Nx*Nx)
# checkers is originally an empty list. The function CHECKER_LIST fills
checkers = CHECKERS.CHECKER_LIST(checkers)
# the list with the position of red and white pieces delcared (by declaring man_r, man_w, king_r, king_w).

# Second criteria for score: Capture values
score_board = [0]*(Nx*Nx)

#################

# Draw the board
BOARD.WINDOWS_PLOT(WINDOWS, FLIP)

# Draw the pieces
BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)

# Change sides if flipped
# pg.display.flip()

click = []
save = []

side = -1  # White's turn / computer
total_move = 1
if side == 1:
    red_first = True
else:
    red_first = False

# Difficulty level of the tree
# depth = 12
depth = 6
point = 0.0
running = True
continue_to_jump = False


if side == 1:
    print('Black Turn')
    CHECKERS.saving(checkers, save)
else:
    print('White Turn')
print('==============================================')

# MAIN GAME LOOP
while running:
    event = pg.event.wait()
    mods = pg.key.get_mods()

    # Handle mouse left click
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        (x, y) = pg.mouse.get_pos()
        column = (x-margin_x)//grid_size
        row = (y-margin_y)//grid_size
        index = column + row*Nx
        if FLIP:
            index = Nx**2-1-index
        click.append(index)

    # Take back: Ctrl+Z
    # See https://www.pygame.org/docs/ref/key.html
    elif not continue_to_jump and event.type == KEYDOWN and mods & pg.KMOD_CTRL:
        if event.key == pg.K_z:
            if len(save) > 1:
                # Use copy to clone the element of list. If use '=' directly, what is really cloned
                checkers = save[-2].copy()
                # is the address of the list! See http://www.runoob.com/python3/python3-att-list-copy.html
                del save[-1]  # remove the last element

                BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
                BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
                pg.display.flip()
                print(
                    '\tBlack takes back.\n==============================================\nBlack Turn')
                total_move -= 1
        elif event.key == pg.K_f:
            FLIP = not FLIP
            print('Board flipped.')
            BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
            BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
            pg.display.flip()

    # Close the window
    elif event.type == pg.QUIT:
        running = False

    if not continue_to_jump:
        (man_jump, king_jump, man_walk, king_walk, taken_by_man,
         taken_by_king) = CHECKERS.AVAILABLE_MOVE(side, checkers)
    available_move = man_jump+king_jump+man_walk+king_walk

    # Draw out the hints
    # find the avaiable start points and stop points, then drawing it out as hint
    (available_start, available_stop) = BOARD.MOVE_HINT(available_move)
    if side == 1:
        for i in available_start:
            hint_x = i % Nx
            hint_y = i//Nx
            if FLIP:
                hint_x = Nx-1-hint_x
                hint_y = Nx-1-hint_y
            pg.draw.circle(WINDOWS, (0, 0, 0),
                           (margin_x+hint_x*grid_size+grid_size//2, margin_y+hint_y*grid_size+grid_size//2), 4, 0)
        for i in available_stop:
            hint_x = i % Nx
            hint_y = i//Nx
            if FLIP:
                hint_x = Nx-1-hint_x
                hint_y = Nx-1-hint_y
            pg.draw.circle(WINDOWS, (0, 255, 0),
                           (margin_x+hint_x*grid_size+grid_size//2, margin_y+hint_y*grid_size+grid_size//2), 4, 0)
        pg.display.flip()

    # Have a winner
    if available_move == []:
        print('No move.')
        final_score = np.add(np.array(checkers), np.array(score_board))
        print(f'Chips left score = {np.array(checkers).sum()}')
        print(f'Moves score = {np.array(score_board).sum()}')
        print(f'Final score = {final_score.sum()}')
        if final_score.sum() > 0:
            white_win = True
            print('White win!')
        elif final_score.sum() < 0:
            red_win = True
            print('Black win!')
        else:
            print('Draw!')
        pg.time.delay(10000)
        break

    # Computer moves
    if side == -1:
        print('\tComputer is thinking...')
        if point == max_eva and depth > 2:
            depth -= 2
        # checkers, point = COMPUTER_MOVE.FIND_BEST_MOVE_MIN_MAX(-1, checkers, depth)  #mini-max
        checkers, point, score_board = COMPUTER_MOVE.FIND_BEST_MOVE_ALPHA_BETA(
            side, checkers, score_board, depth, alpha, beta)  # alpha-beta
        print('\tEvaluation = %.2f ; Depth = %d .' % (point, depth))
        print('\tComputer finishes thinking.')
        if red_first:
            print(f'Move {total_move} Ends')
            total_move += 1
        # accumulate?
        score = np.array(score_board).sum()
        print(f'\tChips left score = {np.array(checkers).sum()}')
        print('\tMoves Score = %d.' % (score))
        final_score = np.add(np.array(checkers), np.array(score_board))
        print(f'\tFinal score = {final_score.sum()}')
        print('Black Turn\n==============================================')

        side = -side
        BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
        BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
        BOARD.SHOW_SCORE(str(final_score.sum()), 15, 15)
        pg.display.flip()
        CHECKERS.saving(checkers, save)

    # Human moves
    # Read the last two clicked square and see whether it corresponding any available move
    # side = 1 Red's turn / human
    elif side == 1 and len(click) > 1:

        # Capture
        if man_jump+king_jump != []:

            # man jump
            if tuple(click[-2:]) in man_jump:
                start = click[-2]
                stop = click[-1]
                taken = (start+stop)//2
                checkers[start] = 0
                checkers[taken] = 0
                checkers[stop] = -man_value
                man_jump = []
                king_jump = []
                taken_by_man = []
                taken_by_king = []
                CHECKERS.MAN_JUMP_RED(stop, checkers, man_jump, taken_by_man)
                print('\tMan jumps from %d to %d.' % (start, stop))
                print(f'Chips left score = {np.array(checkers).sum()}')
                score_board[stop] += CHECKERS.COMPUTE(-man_value,
                                                      man_value, stop)
                print('\tMoves Score = %d.' % (np.array(score_board).sum()))
                final_score = np.add(np.array(checkers), np.array(score_board))
                print(f'\tFinal score = {final_score.sum()}')
                if man_jump != []:  # red man has a jump sequence
                    continue_to_jump = True
                    print('\tMan continues to jump.')
                else:  # zero or jump sequence ends
                    if stop//Nx == 0:
                        checkers[stop] = -king_value  # promote
                        print('\tMan promotes.')
                    continue_to_jump = False
                    side = -side
                    if not red_first:
                        print(f'Move {total_move} Ends')
                        total_move += 1
                    print('White Turn\n==============================================')
                    # can continue to jump without pressing the jumping piece again (but if the player does
                    click = []
                    # not clicked on the corrected square that can be jumped, need to repress the jumping piece)
                BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
                BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
                BOARD.SHOW_SCORE(str(final_score.sum()), 15, 15)
                pg.display.flip()

            # king jump
            elif tuple(click[-2:]) in king_jump:
                start = click[-2]
                stop = click[-1]
                taken = (start+stop)//2
                checkers[start] = 0
                checkers[taken] = 0
                checkers[stop] = -king_value
                man_jump = []
                king_jump = []
                taken_by_man = []
                taken_by_king = []
                CHECKERS.KING_JUMP_RED(
                    stop, checkers, king_jump, taken_by_king)
                print('\tKing jumps from %d to %d.' % (start, stop))
                print(f'Chips left score = {np.array(checkers).sum()}')
                # Update game score
                score_board[stop] += CHECKERS.COMPUTE(-man_value,
                                                      man_value, stop)
                print('\tMoves Score = %d.' % (np.array(score_board).sum()))
                final_score = np.add(np.array(checkers), np.array(score_board))
                print(f'\tFinal score = {final_score.sum()}')
                if king_jump != []:
                    continue_to_jump = True
                    print('\tKing continues to jump.')
                else:
                    continue_to_jump = False
                    side = -side
                    if not red_first:
                        print(f'Move {total_move} Ends')
                        total_move += 1
                    print('White Turn\n==============================================')
                    # can continue to jump without pressing the jumping piece again (but if the player does
                    click = []
                    # not clicked on the corrected square that can be jumped, need to repress the jumping piece)

                BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
                BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
                BOARD.SHOW_SCORE(str(final_score.sum()), 15, 15)
                pg.display.flip()

        # Walk
        elif man_walk+king_walk != []:
            # Man walk
            if tuple(click[-2:]) in man_walk:
                start = click[-2]
                stop = click[-1]
                checkers[start] = 0
                if stop//Nx == 0:
                    checkers[stop] = -king_value  # promote
                    print('\tMan walks from %d to %d .' % (start, stop))
                    print('\tMan promotes')
                else:
                    checkers[stop] = -man_value
                    print('\tMan walks from %d to %d.' % (start, stop))
                side = -side
                if not red_first:
                    print(f'Move {total_move} Ends')
                    total_move += 1
                print('White Turn\n==============================================')
                click = []
                BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
                BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
                pg.display.flip()
            # King walk
            elif tuple(click[-2:]) in king_walk:
                start = click[-2]
                stop = click[-1]
                checkers[start] = 0
                checkers[stop] = -king_value
                print('\tKing walks from %d to %d.' % (start, stop))
                side = -side
                if not red_first:
                    print(f'Move {total_move} Ends')
                    total_move += 1
                print('White Turn\n==============================================')
                click = []
                BOARD.WINDOWS_PLOT(WINDOWS, FLIP)
                BOARD.CHECKER_PLOT(checkers, WINDOWS, FLIP)
                pg.display.flip()
pg.quit()