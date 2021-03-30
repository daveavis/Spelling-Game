import pygame, sys, random, datetime
from pygame.locals import *

def load_words():
    global words_list, words_right_dict
    with open('words.txt', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.strip().split(',')
            words_list.append(line_list)
            words_right_dict[line_list[0]] = False

def select_word():
    global done
    found = False
    if False in words_right_dict.values():
        while not found:
            word = random.choice(list(words_right_dict.keys()))
            if words_right_dict[word] == False:
                found = True
                return word
    else:
        done = True
    #for word in words_right_dict:
    #    if words_right_dict[word] == False:
    #        return word

def select_distractor(word):
    for word_line in words_list:
        if word_line[0] == word:
            choice = random.randint(1,len(word_line)-1)
            return word_line[choice]


pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Spelling Game')
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

BG_COLOR = (255, 255, 255)

font = pygame.font.Font(None, 72)

result_txt = ''
result_color = (0,0,0)
result = font.render(result_txt, True, result_color)
result_rect = result.get_rect()
result_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

done_msg = font.render('You Win!!!', True, (0, 0, 255))
done_rect = done_msg.get_rect()
done_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

display_time_diff = 1
display_result = False
done = False
correct_dir = ''
correct = ''
word = ''
distractor = ''
l_word = 'error'
r_word = 'error'
load_new_word = True
load_new_distractor = True
words_list = []
words_right_dict = {}
load_words()

while True:
    if load_new_word:
        word = select_word()
        load_new_word = False
        if random.random() < 0.5:
            correct_dir = 'l'
        else:
            correct_dir = 'r'
    
    if load_new_distractor:
        distractor = select_distractor(word)
        load_new_distractor = False

    if correct_dir == 'l':
        l_word = word
        r_word = distractor
    else:
        l_word = distractor
        r_word = word
        
    left_word = font.render(l_word, True, (0,0,0))
    left_word_rect = left_word.get_rect()
    left_word_rect.center = (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2)

    right_word = font.render(r_word, True, (0,0,0))
    right_word_rect = right_word.get_rect()
    right_word_rect.center = (SCREEN_WIDTH * 2 / 3, SCREEN_HEIGHT / 2)

    screen.fill(BG_COLOR)
    screen.blit(left_word, left_word_rect)
    screen.blit(right_word, right_word_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT and correct_dir == 'r' or event.key == K_LEFT and correct_dir == 'l':
                correct = 'y'
                words_right_dict[word] = True
            if event.key == K_RIGHT and correct_dir == 'l' or event.key == K_LEFT and correct_dir == 'r':
                correct = 'n'

    if correct == 'y':
        display_result = True
        result_txt = 'Yes!!!'
        result_color = (0, 255, 0)
        load_new_word = True
        load_new_distractor = True
        correct = ''
        display_start = datetime.datetime.now()
    if correct == 'n':
        display_result = True
        result_txt = 'No, try again.'
        result_color = (255, 0, 0)
        load_new_word = True
        load_new_distractor = True
        correct = ''
        display_start = datetime.datetime.now()
    
    if display_result == True:
        if (datetime.datetime.now() - display_start).total_seconds() < display_time_diff:
            result = font.render(result_txt, True, result_color)
            result_rect = result.get_rect()
            result_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            screen.blit(result, result_rect)
        else:
            display_result = False

    if done == True:
        if (datetime.datetime.now() - display_start).total_seconds() > display_time_diff:
            screen.fill(BG_COLOR)
            screen.blit(done_msg, done_rect)

    pygame.display.update()
    fpsClock.tick(FPS)
