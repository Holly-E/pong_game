# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 12
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT // 2
paddle2_pos = HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
ball_vel = [0, 0]
table = 'DarkGreen'
left_color = 'Tomato'
right_color = 'SkyBlue'


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball():
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]

    HORIZONTAL = random.randrange(120, 240) // 60
    VERTICAL = random.randrange(60, 180) // 60
    if score1 == 5 or score2 == 5:
        ball_vel = [0, 0]
        end_game()
    elif RIGHT:
        ball_vel = [HORIZONTAL, -VERTICAL]
    else:
        ball_vel = [-HORIZONTAL, -VERTICAL]

# end game is score reaches 5
def end_game():
    global winner

    if RIGHT:
        winner = "Right player won!"
    else:
        winner = "Left player won!"

# change ball direction & increase velocity up to maximum
def faster():
    ball_vel[0] = - ball_vel[0]
    if -13 < ball_vel[0] < 13:
        ball_vel[0] = ball_vel[0] * 1.3

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos # these are numbers
    global score1, score2, winner

    score1 = 0
    score2 = 0
    winner = ''

    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2

    spawn_ball()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, LEFT, RIGHT

    # draw mid line and gutters
    canvas.draw_line([WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1, 'white')
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, left_color)
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, right_color)

    # update ball
    ball_pos = [ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1]]

    # keep ball inside horizontal lines
    if ball_pos[1] == 0 + BALL_RADIUS or ball_pos[1] == HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'white', 'white')

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel > HALF_PAD_HEIGHT) and (paddle1_pos + paddle1_vel < (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos += paddle1_vel

    if (paddle2_pos + paddle2_vel > HALF_PAD_HEIGHT) and (paddle2_pos + paddle2_vel < (HEIGHT - HALF_PAD_HEIGHT)):
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), PAD_WIDTH, left_color)
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), PAD_WIDTH, right_color)

    # determine whether paddle and ball collide
    # increase velocity by 10%
    # spawn ball moving in opposite direction if gutter is hit
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            faster()
        else:
            score2 += 1
            RIGHT = True
            LEFT = False
            spawn_ball()

    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            faster()
        else:
            score1 += 1
            RIGHT = False
            LEFT = True
            spawn_ball()

    # draw scores
    canvas.draw_text(str(score1), [255, 50], 30, left_color)
    canvas.draw_text(str(score2), [330, 50], 30, right_color)
    canvas.draw_text(winner, [150, 125], 50, 'Gold')

def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 5

    # control left paddle
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel

    # control right paddle
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel

def keyup(key):
    global paddle1_vel, paddle2_vel

    if (key == simplegui.KEY_MAP["w"]) or (key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 0

    if (key == simplegui.KEY_MAP["up"]) or (key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('New Game', new_game)
frame.set_canvas_background(table)

# start frame
new_game()
frame.start()
