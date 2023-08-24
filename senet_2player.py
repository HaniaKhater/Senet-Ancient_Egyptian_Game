"""""
File: senet.py
-----------------
Ancient Egyptian Board game of Senet.
"""

import tkinter
import time
from random import choices
from PIL import ImageTk
from PIL import Image


CANVAS_HEIGHT = 720
CANVAS_WIDTH = 1200

N_ROWS = 3
N_COLS = 10
SIZE = CANVAS_WIDTH / N_COLS - 1
BOARD_TOP_Y = 165
BOARD_MAX_Y = BOARD_TOP_Y + (3 * SIZE)

PIONS = 5
PIONS_SIZE = 50
PIONS_TOP_MARGIN = 40
PIONS_SIDE_MARGIN = (SIZE / 2) - (PIONS_SIZE / 2)
PIONS_OUTLINE = 3
PAWN_OUT_SEPERATOR = PIONS_SIZE + 10

STICK_WIDTH = 200
STICK_HEIGHT = 25
STICK_TOP_Y = 550
STICK_SEPARATION = 17
STICK_TOP_X = (CANVAS_WIDTH / 2) - (STICK_WIDTH / 2)
STICK_END_X = STICK_TOP_X + STICK_WIDTH
STICK_END_Y = STICK_TOP_Y + STICK_HEIGHT + (STICK_SEPARATION * 4)

PAWN_ID_MIN = 62
PAWN_ID_MAX = 71
CIRCLE_ID_MIN = 62
CIRCLE_ID_MAX = 66
RECT_ID_MIN = 67
RECT_ID_MAX = 71

# ======================== GLOBAL VARIABLES ========================
kanvas = None  # stores the canvas so it can be used by event handlers (wanted to avoid confusion so I added the k)

moves = None  # the number of squares a pawn is allowed to move by as a result of the sticks being rolled

board_x = None  # list of x coordinates of each board square
board_y = None  # list of x coordinates of each board square

current_squ_clicked = None  # the recognized square of the board that was last clicked
current_pawn_clicked = None  # the recognized pawn that was last clicked
attacked_pawn = None  # the recognized pawn that is on current_squ_clicked + moves

a = 0  # alternates player by adding 1 at each turn and determining players depending on (a % 2 == 0 or 1)
# it's global because the event handling function that uses it restarts at every click
# ===================================================================


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Senet')
    global kanvas
    kanvas = canvas
    # SET UP

    # Store and adjust the x & y coordinates of each board square in lists
    # Store them in global variable so the can be accessed by event handling functions
    global board_x
    global board_y
    square_x = []
    square_y = []
    draw_board_squares(canvas, square_x, square_y)
    adjusted_x = []
    adjusted_y = []
    adjust_list(square_x, adjusted_x)
    adjust_list(square_y, adjusted_y)
    board_x = adjusted_x
    board_y = adjusted_y

    # FILL BOARD - INITIAL STATE
    # Add symbols to board
    # Add house of rebirth at square 15
    rebirth = ImageTk.PhotoImage(Image.open("images/rebirth.jpg"))
    canvas.create_image(adjusted_x[14] + 30, adjusted_y[14] + 10, anchor="nw", image=rebirth)
    # Add house of beauty at square 26
    beauty = ImageTk.PhotoImage(Image.open("images/beauty.jpg"))
    canvas.create_image(adjusted_x[25] + 11, adjusted_y[25] + 12, anchor="nw", image=beauty)
    # Add house of Water at square 27
    water = ImageTk.PhotoImage(Image.open("images/water.jpg"))
    canvas.create_image(adjusted_x[26] + 10, adjusted_y[26] + 6, anchor="nw", image=water)
    # Add House of Three Truths at square 28
    three_birds = ImageTk.PhotoImage(Image.open("images/3birds.jpg"))
    canvas.create_image(adjusted_x[27] + 6, adjusted_y[27] + 6, anchor="nw", image=three_birds)
    # Add house of Ra Atum at square 29
    ra_atum = ImageTk.PhotoImage(Image.open("images/2_ra.jpg"))
    canvas.create_image(adjusted_x[28] + 10, adjusted_y[28] + 22, anchor="nw", image=ra_atum)
    # Add house of Horus at square 30
    eye = ImageTk.PhotoImage(Image.open("images/eye.jpg"))
    canvas.create_image(adjusted_x[29] + 9, adjusted_y[29] + 20, anchor="nw", image=eye)
    # Decorate with the wings on top of the board
    wings = ImageTk.PhotoImage(Image.open("images/L_wings.jpg"))
    width = wings.width()
    canvas.create_image((CANVAS_WIDTH / 2) - (width / 2), 10, anchor="nw", image=wings)

    # ENUMERATE_SQUARES
    number_board(canvas, adjusted_x, adjusted_y)
    # ADD PAWNS
    add_circles(canvas, adjusted_x, adjusted_y)
    add_rect_pions(canvas, adjusted_x, adjusted_y)
    # ADD BLANK STICKS
    display_sticks(canvas, 5)

    canvas.mainloop()


def adjust_list(list_name, adjusted_list):
    # Adapt the coordinates lists to the snake shape of the board
    for i in range(len(list_name)):
        # 1st row stays as is
        if i < 10:
            adjusted_list.append(list_name[i])
        # 2nd row: the squares are reversed (10 saved as 19, 11 as 18, 12 as 17, 13 as 16, etc.)
        elif i < 20:
            reverse = (9 - (i - 10)) + 10
            adjusted_list.append(list_name[reverse])
        # 3rd row stays as is
        else:
            adjusted_list.append(list_name[i])


def roll_sticks(canvas):
    # Set up the probability of each sticks combination and getting one at random
    global moves
    population = [1, 2, 3, 4, 5]
    weights = [0.25, 0.375, 0.25, 0.1675, 0.1675]
    rand_moves = choices(population, weights)  # gives me a list with the random number of moves
    moves = rand_moves[0]  # get the number out of the list and into global variable moves
    display_sticks(canvas, moves)  # draw the sticks combination corresponding to the random number of moves generated
    write_moves(canvas, moves)  # write the random number of moves generated


def write_moves(canvas, moves):
    x = (CANVAS_WIDTH / 2) - 10
    y = 680
    number = str(moves)
    canvas.create_rectangle(x - 20, y - 40, x + 45, y + 25, fill="white", width=3)
    canvas.create_text(x, y, anchor="w", font=('Papyrus', 56), text=number)


def draw_board_squares(canvas, square_x, square_y):
    for row in range(N_ROWS):
        for col in range(N_COLS):
            draw_square(canvas, row, col, square_x, square_y)


def draw_square(canvas, row, col, squares_x, squares_y):
    x = col * SIZE
    y = (row * SIZE) + BOARD_TOP_Y
    canvas.create_rectangle(x, y, x + SIZE, y + SIZE, width=5)
    squares_x.append(x)
    squares_y.append(y)


def number_board(canvas, adjusted_x, adjusted_y):
    for i in range(25):
        if i != 14:
            number_a_square(canvas, i, adjusted_x, adjusted_y)


def number_a_square(canvas, index, adjusted_x, adjusted_y):
    # writes the number of a board square on the top left corner
    x = adjusted_x[index] + 13
    y = adjusted_y[index] + 8
    text = str(index + 1)
    canvas.create_text(x, y, anchor='nw', font=('Papyrus', 25), text=text)


def add_circles(canvas, adjusted_x, adjusted_y):
    # adds the five circle pawns at squares 1, 3, 5, 7, & 9
    for i in range(5):
        draw_circle(canvas, (i * 2), adjusted_x, adjusted_y)


def draw_circle(canvas, index, adjusted_x, adjusted_y):
    x = adjusted_x[index] + PIONS_SIDE_MARGIN
    y = adjusted_y[index] + PIONS_TOP_MARGIN
    canvas.create_oval(x, y, x + PIONS_SIZE, y + PIONS_SIZE, fill="red", width=PIONS_OUTLINE, tags="circles")


def add_rect_pions(canvas, adjusted_x, adjusted_y):
    # adds the five square pawns at squares 2, 4, 6, 8, & 10
    for i in range(5):
        draw_rect_pion(canvas, ((i * 2) + 1), adjusted_x, adjusted_y)


def draw_rect_pion(canvas, index, adjusted_x, adjusted_y):
    x = adjusted_x[index] + PIONS_SIDE_MARGIN
    y = adjusted_y[index] + PIONS_TOP_MARGIN
    canvas.create_rectangle(x, y, x + PIONS_SIZE, y + PIONS_SIZE, fill="brown", width=PIONS_OUTLINE, tags="squares")


def display_sticks(canvas, moves):
    # depending on the random number of moves generated it will display colored and uncolored sticks
    if moves == 5:
        # the sticks system's exception is 5 where all four sticks are uncolored
        moves = 0
    for i in range(moves):
        draw_stick(canvas, i, "gray")
    for i in range(4 - moves):
        draw_stick(canvas, (i + moves), "white")


def draw_stick(canvas, stick_number, color):
    y = STICK_TOP_Y + (stick_number * STICK_SEPARATION)
    y_end = y + STICK_HEIGHT
    canvas.create_oval(STICK_TOP_X, y, STICK_END_X, y_end, fill=color, width=3)


##################################################
##################################################
# =============== EVENT HANDLING =============== #
##################################################
##################################################
# ====== This is where the action happens ====== #
##################################################
def get_click(event):
    # Triggered when something on the canvas is clicked
    global a
    mouse_x = event.x
    mouse_y = event.y
    # compares the coord of the click to the location of the sticks and the board
    sticks_clicked = (STICK_TOP_X < mouse_x < STICK_END_X) and (STICK_TOP_Y < mouse_y < STICK_END_Y)
    board_clicked = (BOARD_TOP_Y < mouse_y < BOARD_MAX_Y)
    if sticks_clicked:
        # Gives a new random combination of sticks and moves
        roll_sticks(kanvas)
        # Display Player
        if a % 2 == 0:
            display("Circle")
        else:
            display("Square")
        a += 1
    if board_clicked:
        recognize_square_and_pawn_clicked(mouse_x, mouse_y)
        if pawn_present(current_squ_clicked):
            attempt_move_pawn(current_squ_clicked, current_pawn_clicked)
    # Will only do something if the game is over, but needed to check after every click
    game_is_over(kanvas)


def recognize_square_and_pawn_clicked(mouse_x, mouse_y):
    global current_squ_clicked
    global current_pawn_clicked
    # loop through all squares to check if the click was on it
    for i in range(30):
        if (board_x[i] < mouse_x < board_x[i] + SIZE) and (board_y[i] < mouse_y < (board_y[i] + SIZE)):
            current_squ_clicked = i
    current_pawn_clicked = index_to_pawn(current_squ_clicked)


"""
PREPARATIONS FOR PAWN MOVEMENT BY MOVES
"""


def attempt_move_pawn(current_squ_clicked, current_pawn_clicked):
    target_squ = current_squ_clicked + moves
    # Make sure not skipping the house that all pawns need to pass by
    if not trying_to_skip(current_squ_clicked):
        # in case the pawn is on the house of passing and doesn't immediately exit the board with a 5
        if (current_squ_clicked == 25) and (moves < 5):
            if not pawn_present(target_squ):
                move_to_empty(target_squ, current_pawn_clicked)
            elif pawn_present(target_squ) and not in_safe_zone(target_squ):
                swap_pawns(target_squ)
        #  in case the pawn clicked could exit with the right number of moves
        elif current_squ_clicked >= 25:
            exit_house(current_squ_clicked)
        elif target_squ_empty(target_squ):
            move_to_empty(target_squ, current_pawn_clicked)
        elif pawn_present(target_squ) and (not pawn_is_safe(target_squ)):
            swap_pawns(target_squ)


def move_to_empty(target_squ, current_pawn_clicked):
    target_x = board_x[target_squ] + PIONS_SIDE_MARGIN
    target_y = board_y[target_squ] + PIONS_TOP_MARGIN
    kanvas.moveto(current_pawn_clicked, target_x, target_y)
    # If it lands on water it needs to go back to the rebirth square at index 14
    if target_squ == 26:
        kanvas.moveto(current_pawn_clicked, target_x, target_y)
        kanvas.update()
        time.sleep(0.6)
        kanvas.moveto(current_pawn_clicked, board_x[14] + PIONS_SIDE_MARGIN, board_y[14] + PIONS_TOP_MARGIN)
        display("      Pawn returns to \n the House of Rebirth")


def target_squ_empty(target_index):
    # to make the code more readable
    if pawn_present(target_index):
        return False
    else:
        return True


def swap_pawns(target_squ):
    # swap positions when successfully attacking a pawn
    attacked_pawn = index_to_pawn(target_squ)
    target_x = board_x[target_squ] + PIONS_SIDE_MARGIN
    target_y = board_y[target_squ] + PIONS_TOP_MARGIN
    target_v = board_x[current_squ_clicked] + PIONS_SIDE_MARGIN
    target_w = board_y[current_squ_clicked] + PIONS_TOP_MARGIN
    kanvas.moveto(current_pawn_clicked, target_x, target_y)
    kanvas.moveto(attacked_pawn, target_v, target_w)


def pawn_present(index):
    # gets the coordinates for the search area
    m = board_x[index]
    n = board_y[index]
    results_squ = kanvas.find_overlapping(m, n, m + SIZE, n + SIZE)
    # loop through the items on the square checking if one of them is a pawn
    for elem in results_squ:
        if PAWN_ID_MIN <= elem <= PAWN_ID_MAX:
            return True


def pawn_is_safe(index):
    if in_safe_zone(index):
        display("Respect the Safe Haven!")
        return True
    if not pawn_is_alone(index):
        if pawn_coupled(index):
            display("The pawn you attempted \n        to attack is safe")
            return True
    else:
        return False


def pawn_is_alone(index):
    # Check if the pawn has a neighbor
    if (not pawn_present(index - 1)) and (not pawn_present(index + 1)):
        return True
    else:
        return False


def pawn_coupled(index):
    # Check if the pawn's neighbor is the same shape, and therefore protecting him from attack
    shape_attacked = find_shape_attacked(index)
    # Avoid errors involving checking for an index that doesn't exist
    if index != 0:
        before_neighbor_same = neighbor_is_same_shape(index, index - 1, shape_attacked)
    if index != 29:
        after_neighbor_same = neighbor_is_same_shape(index, index + 1, shape_attacked)
    return before_neighbor_same or after_neighbor_same


def neighbor_is_same_shape(index, index_neighbor, shape_attacked):
    if index != 0:
        if (shape_attacked == "circle") and pawn_is_circle(index_neighbor):
            return True
    if index != 29:
        if (shape_attacked == "rect") and pawn_is_rect(index_neighbor):
            return True


def find_shape_attacked(index):
    shape_attacked = "idk"
    if pawn_is_circle(index):
        shape_attacked = "circle"
    elif pawn_is_rect(index):
        shape_attacked = "rect"
    return shape_attacked


def pawn_is_circle(index):
    if pawn_present(index):
        pawn_id = index_to_pawn(index)
        if CIRCLE_ID_MIN <= pawn_id <= CIRCLE_ID_MAX:
            return True


def pawn_is_rect(index):
    if pawn_present(index):
        pawn_id = index_to_pawn(index)
        if RECT_ID_MIN <= pawn_id <= RECT_ID_MAX:
            return True


def in_safe_zone(index):
    # GAME RULE: pawns on these Safe Havens squares cannot be attacked
    if index == 14 or index == 25 or index == 29:
        return True
    else:
        return False


def index_to_pawn(index):
    # returns the id of the pawn on the square with the index passed
    m = board_x[index]
    n = board_y[index]
    results_squ = kanvas.find_overlapping(m, n, m + SIZE, n + SIZE)
    for elem in results_squ:
        if PAWN_ID_MIN <= elem <= PAWN_ID_MAX:
            return elem


def display(message):
    # pops up a message for the player
    x = (CANVAS_WIDTH / 4) - 45
    y = 630
    words = kanvas.create_text(x, y, anchor="center", font=('Papyrus', 35), text=message)
    kanvas.update()
    time.sleep(1.2)
    kanvas.delete(words)


""""
Setting up the exits
"""""


def trying_to_skip(current_squ_clicked):
    # GAME RULE: all pawns must pass by 25 before moving on
    if current_squ_clicked < 25 and (current_squ_clicked + moves > 25):
        display("You must first \n   pass by 26")
        return True
    else:
        return False


def exit_house(current_squ_clicked):
    # GAME RULE: pawn on square indexed 27 needs a 3 to get out, 28 a 2, and 29 a one.
    if 30 - current_squ_clicked == moves:
        go_off_board(current_squ_clicked)
    else:
        s = "   You need a " + str(30 - current_squ_clicked) + " to \n remove this pawn"
        display(s)


def go_off_board(current_squ_clicked):
    # Move the pawns getting off the board to the bottom of the board
    pawn_leaving = index_to_pawn(current_squ_clicked)
    if find_shape_attacked(current_squ_clicked) == "circle":
        circle_number = pawn_leaving - CIRCLE_ID_MIN
        x = (CANVAS_WIDTH / 2) + 200 + (circle_number * PAWN_OUT_SEPERATOR)
        y = BOARD_MAX_Y + 30
        kanvas.moveto(pawn_leaving, x, y)
    elif find_shape_attacked(current_squ_clicked) == "rect":
        rect_number = pawn_leaving - RECT_ID_MIN
        x = (CANVAS_WIDTH / 2) + 200 + (rect_number * PAWN_OUT_SEPERATOR)
        y = BOARD_MAX_Y + 30 + PIONS_SIZE + 20
        kanvas.moveto(pawn_leaving, x, y)


"""""        
Set up the GAME OVER
"""""


def game_is_over(kanvas):
    # If someone has won, displays a Game Over screen and announces the winner
    if circles_won() or rect_won():
        time.sleep(0.5)     # Gives time for us to see the last pawn get off the board
        kanvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="white", width=20)
        kanvas.create_text((CANVAS_WIDTH / 2), 280, anchor='center', font=('Papyrus', 120), text="Game Over!")
    if circles_won():
        kanvas.create_text((CANVAS_WIDTH / 2), 450, anchor='center', font=('Papyrus', 80), text="Circles Won!")
    elif rect_won():
        kanvas.create_text((CANVAS_WIDTH / 2), 450, anchor='center', font=('Papyrus', 80), text="Squares Won!")


def circles_won():
    # loop through the circle pawns counting how many are bellow the board
    circles_bellow = 0
    for i in range(5):
        id_to_check = i + CIRCLE_ID_MIN
        circle_coord = kanvas.coords(id_to_check)
        y = circle_coord[1]
        if y > BOARD_MAX_Y:
            circles_bellow += 1
    if circles_bellow == 5:
        return True
    else:
        return False


def rect_won():
    # Loop through the square pawns counting how many are bellow the board
    rect_bellow = 0
    for i in range(5):
        id_to_check = i + RECT_ID_MIN
        circle_coord = kanvas.coords(id_to_check)
        y = circle_coord[1]
        if y > BOARD_MAX_Y:
            rect_bellow += 1
    if rect_bellow == 5:
        return True
    else:
        return False




######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########
# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    # ADDITION - CLICK
    # This generates a call to get_click whenever the left mouse button is pressed
    canvas.bind("<Button-1>", get_click)
    # END OF ADDITION
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

    return canvas


if __name__ == '__main__':
    main()
