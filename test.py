import _curses as curses
from _curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

# Constants
KEY_ESC = 27

height = 10
width = 40
half_height = int(height / 2)
half_width = int(width / 2)
title = " snek "

curses.initscr()
win = curses.newwin(height, width, 0, 0)

# curses parameters
win.nodelay(True)  # makes getch non blocking
win.keypad(True)  # block keyboard signals (^C ...)
curses.noecho()  # do not print the keyboard inputs

# curses init
curses.curs_set(0)
win.border(0)
win.addstr(0, int(half_width - len(title) / 2), title)

# initializing values
score = -1
current_key = KEY_RIGHT
last_key = current_key

snake = [
    [half_height, half_width],
    [half_height, half_width - 1],
    [half_height, half_width - 2],
]
food = []


# methods
def opposite_key(key):
    if key == KEY_DOWN:
        return KEY_UP
    if key == KEY_UP:
        return KEY_DOWN
    if key == KEY_LEFT:
        return KEY_RIGHT
    if key == KEY_RIGHT:
        return KEY_LEFT


while current_key != KEY_ESC:
    # print the score at the top of the screen
    win.addstr(0, 1, f" Score: {score} ")

    event = win.getch()
    if event != -1:
        last_key = current_key
        current_key = event

    # ignore if wrong input
    if current_key == opposite_key(last_key):
        current_key = last_key
        continue

    # move the snake
    new_pos = [
        snake[0][0] + (current_key == KEY_DOWN and 1) + (current_key == KEY_UP and -1),
        snake[0][1]
        + (current_key == KEY_LEFT and -1)
        + (current_key == KEY_RIGHT and 1),
    ]
    snake.insert(0, new_pos)

    # move the snake to the other side of the screen
    if snake[0][0] == 0:
        snake[0][0] = height - 2
    if snake[0][1] == 0:
        snake[0][1] = width - 2
    if snake[0][0] == height - 1:
        snake[0][0] = 1
    if snake[0][1] == width - 1:
        snake[0][1] = 1

    if snake[0] == food or not food:  # not food for the init
        food = []
        score += 1
        # spawn the food
        while not food:
            if food in snake:
                food = []
            food.append(randint(1, height - 2))
            food.append(randint(1, width - 2))

        win.addch(food[0], food[1], "*")
        text = f" fruit: {food[0]};{food[1]} "
        win.addstr(0, width - len(text) - 1, text)

    else:
        # remove last value to move the snake
        last = snake.pop()
        win.addch(last[0], last[1], " ")

    # if snake runs over itself stop
    if snake[0] in snake[1:]:
        break

    # print the food
    win.addch(food[0], food[1], "*")

    # print the snake
    for i, elem in enumerate(snake):
        if i == 0:
            win.addch(elem[0], elem[1], "€")
        else:
            win.addch(elem[0], elem[1], "#")

    # wait before next turn
    win.timeout(150)

curses.endwin()
print("Score: " + str(score))
