import pygame
from game import *

pygame.init()

window_len = 1280
window_width = 720
win = pygame.display.set_mode((window_len, window_width))
pygame.display.set_caption("Halloween Math")
u_dead = pygame.image.load('res/youdied.png')
pygame.mixer.music.load('res/electro_zombies.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


#Welcome statement
print('My name is Greggroll and this is my first pygame.')


# TODO
# crop out whitespace on undertale
# create animated frames for movement

# input box rect
input_box = pygame.Rect(540, 250, 100, 32)
text = ''
active = False
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive

# creates retry button using class from game
retry_button = Button((255, 255, 255), 540, 500, 200, 75, 'Retry?')
new_game_button = Button((255, 255, 255), 540, 500, 200, 75, 'Next level?')

bg = pygame.image.load('res/graveyard(1280x720).png')
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

font = pygame.font.SysFont('comicsans', 30, True)

user = User(83, 560, 10, 10, 'res/ghost-trick-or-treating-hi.png')


def redraw_game_window():
    # draw background
    win.blit(bg, (0, 0))
    # draw current level
    level_text = (font.render(f'level: {level}', 1, (0, 0, 0)))
    win.blit(level_text, (1150, 10))
    # draw health with background
    health = font.render(f'lives: {lives} ', 1, (255, 255, 255))  # 81x21
    pygame.draw.rect(win, (160, 160, 160), (589.5, 90, 105, 41))
    win.blit(health, (599.5, 100))
    # draw question
    question_text = font.render(question, 1, (255, 255, 255))
    pygame.draw.rect(win, (160, 160, 160), (547, 190, 186, 41))
    win.blit(question_text, (557, 200))  # 166, 21
    # draw sprite
    win.blit(user.image, (user.x, user.y, user.width, user.height))
    # update
    answer_txt = font.render(text, True, (255, 255, 255))
    width = max(200, answer_txt.get_width() + 10)
    input_box.w = width
    win.blit(answer_txt, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(win, (255, 100, 0), input_box, 2)

    if is_dead:
        win.blit(u_dead, (0, 0, 1280, 720))
        retry_button.draw(win)
    if progress == 5:
        # TODO
        # make screen or animation for winning
        new_game_button.draw(win)
    pygame.display.update()


def get_question():
    nums = generate_nums(difficulty)
    question = get_question_text(nums)
    answer = str(get_answer(nums))
    return question, answer


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
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(f'your answer: {text}')
                    print(f'correct answer: {answer}')
                    if text == answer:
                        progress += 1
                    print(f'you are at {progress}/5')
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        if done:
            if text == answer:
                get_new_question = True
                for i in range(20):
                    user.x += 10.25
                    redraw_game_window()
                while progress >= 5:
                    # make screen freeze so you cant input more
                    redraw_game_window()
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if new_game_button.is_over(pos):
                                progress = 0
                                user.x = 83
                                done = False
                                difficulty += 2
                                level += 1
                                lives += 1
            else:
                lives -= 1
                if lives == 0:
                    is_dead = True
                    get_new_question = True
        redraw_game_window()
    while is_dead:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_over(pos):
                    lives = 3
                    is_dead = False
                    user.x = 83
                    level = 1
                    difficulty = 10

    redraw_game_window()
