import pygame
from game import *

pygame.init()

# window
window_len = 1280
window_width = 720
win = pygame.display.set_mode((window_len, window_width))
pygame.display.set_caption("Halloween Math")

# images
bg = pygame.image.load('res/graveyard(1280x720).png')
you_died_image = pygame.image.load('res/youdied.png')

# music
pygame.mixer.music.load('res/electro_zombies.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# welcome statement
print('My name is Greggroll and this is my first pygame.')

# TODO
# crop out whitespace on undertale
# create animated frames for movement

# input box rect
input_box = pygame.Rect(540, 250, 100, 32)
text = ''
'''
active = False
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
'''

# buttons
retry_button = Button((255, 255, 255), 540, 500, 200, 75, 'Retry?')
new_game_button = Button((255, 255, 255), 540, 500, 200, 75, 'Next level?')

# font
font = pygame.font.SysFont('comicsans', 30, True)

# user
user = User(83, 560, 10, 10, 'res/ghost-trick-or-treating-hi.png')

# game state
# TODO
# add 5 more headstones to work as progress markers
progress = 0
# TODO
# 5 for now
# if progress = 10 make it so game is over and halloween candy flies around or somthing
lives = 3

# TODO
# create graphics for lives
# can use for i in lives draw(life.png) x + 50

difficulty = 10
level = 1
correct_to_win = 5

## Drawers ##

def redraw_game_window():
    global new_game_button

    draw_background()
    draw_current_level()
    draw_health()
    draw_question()
    draw_sprite()
    update_input_box()

    if is_dead:
        draw_you_died()
    if progress == 5:
        # TODO
        # make screen or animation for winning
        new_game_button.draw(win)

    pygame.display.update()


def draw_background():
    global win

    win.blit(bg, (0, 0))


def draw_current_level():
    global win, font, level

    level_text = (font.render(f'level: {level}', 1, (0, 0, 0)))
    win.blit(level_text, (1150, 10))


def draw_health():
    global win, font, lives

    health = font.render(f'lives: {lives} ', 1, (255, 255, 255))  # 81x21
    pygame.draw.rect(win, (160, 160, 160), (589.5, 90, 105, 41))
    win.blit(health, (599.5, 100))


def draw_question():
    global win, font

    question_text = font.render(question, 1, (255, 255, 255))
    pygame.draw.rect(win, (160, 160, 160), (547, 190, 186, 41))
    win.blit(question_text, (557, 200))  # 166, 21


def draw_sprite():
    global win

    win.blit(user.image, (user.x, user.y, user.width, user.height))


def draw_you_died():
    global win, you_died_image, retry_button

    win.blit(you_died_image, (0, 0, 1280, 720))
    retry_button.draw(win)


def update_input_box():
    global win, font

    answer_text = font.render(text, True, (255, 255, 255))
    answer_width = max(200, answer_text.get_width() + 10)
    input_box.w = answer_width
    win.blit(answer_text, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(win, (255, 100, 0), input_box, 2)


def get_question():
    nums = generate_nums(difficulty)
    question = get_question_text(nums)
    answer = str(get_answer(nums))
    return question, answer


## Event handlers ##

def handle_keydown_event(event, text, done):
    global progress, correct_to_win

    if event.type == pygame.QUIT:
        pygame.quit()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            print(f'your answer: {text}')
            print(f'correct answer: {answer}')
            if text == answer:
                progress += 1
            print(f'you are at {progress}/{correct_to_win}')
            done = True
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode

    return text, done


def handle_mousebuttondown_event(event, check_state, done):
    button = Button((255, 255, 255), 540, 500, 200, 75, None)

    pos = pygame.mouse.get_pos()

    if event.type == pygame.QUIT:
        pygame.quit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button.is_over(pos):
            if check_state is 'level_up':
                done = False
                level_up()
            elif check_state is 'died':
                done = True
                died()

    return done


## Game states ##

def level_up():
    global progress, lives, user, difficulty, level

    progress = 0
    user.x = 83
    difficulty += 2
    level += 1
    lives += 1


def died():
    global lives, is_dead, user, difficulty, level

    lives = 3
    is_dead = False
    user.x = 83
    difficulty = 10
    level = 1


question, answer = get_question()
get_new_question = False

while 1:
    is_dead = True if lives <= 0 else False
    redraw_game_window()
    pygame.time.delay(100)

    while not is_dead:
        if get_new_question:
            question, answer = get_question()
            get_new_question = False
            text = ''
        done = False

        for event in pygame.event.get():
            text, done = handle_keydown_event(event, text, done)

        if done:
            if text == answer:
                get_new_question = True
                for i in range(20):
                    user.x += 10.25
                    redraw_game_window()

                while progress >= correct_to_win:
                    # make screen freeze so you cant input more
                    redraw_game_window()

                    for event in pygame.event.get():
                        done = handle_mousebuttondown_event(event, 'level_up', done)

            else:
                lives -= 1
                if lives == 0:
                    is_dead = True
                    get_new_question = True

        redraw_game_window()

    while is_dead:
        for event in pygame.event.get():
            done = handle_mousebuttondown_event(event, 'died', done)

    redraw_game_window()
