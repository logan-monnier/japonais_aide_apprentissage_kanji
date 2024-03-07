import pygame
from pygame.locals import *
from random import randint, choice
import os

WHITE = (255,255,255)
BLACK = (  0,  0,  0)

GREY = (128,128,128)

RED   = (255,  0,  0,128)
GREEN = (  0,255,  0,128)
BLUE  = (  0,  0,255,128)

YELLOW = (255,255, 0)

SCREEN_W = 800
SCREEN_H = 600

def button_create(text, inactive_color, active_color, action):
    font = pygame.font.Font(None, 40)
    text = font.render(text, True, BLACK)

    return [text, inactive_color, active_color, action, False]

def button_check(info, grandeur, event):
    text, inactive_color, active_color, action, hover = info
    rect = pygame.Rect(grandeur)
    text_rect = text.get_rect(center=rect.center)

    if event.type == pygame.MOUSEMOTION:
        # hover = True/False
        info[-1] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action()

def button_draw(screen, grandeur, info):
    text, inactive_color, active_color, action, hover = info
    rect = pygame.Rect(grandeur)
    text_rect = text.get_rect(center=rect.center)
    transparent = pygame.Surface((grandeur[2], grandeur[3]), pygame.SRCALPHA)

    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(transparent, color, transparent.get_rect())
    screen.blit(transparent, (grandeur[0], grandeur[1]))
    screen.blit(text, text_rect)

def checkbox_draw(screen, grandeur, color, checked):
    rect = pygame.Rect(grandeur)
    
    pygame.draw.rect(screen, color, rect, 1)
    if checked:
        pygame.draw.circle(screen, color, (rect[0]+rect[3]//2, rect[1]+rect[3]//2), rect[3]//2-2)

def text_draw(screen, text, color, centre, font_width):
    japanesefont = pygame.font.Font("ipaexg.ttf", font_width)
    text = japanesefont.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = centre
    screen.blit(text, textRect)

def choose_kanji(l):
    return [choice(list(quiz_dict_kanji.items()))]*3

def on_click_button_1():
    global stage
    stage = 'apprendre'

def on_click_button_2():
    global stage
    stage = 'options'

def on_click_button_3():
    global stage
    global running

    stage = 'quitter'
    running = False

def on_click_button_kanji():
    global stage
    stage = 'kanji'

def on_click_button_GO():
    global stage
    global quiz_dict_kanji
    if stage == 'kanji' and [checkboxs[i][0] for i in range(len(checkboxs))].count(True) >= 3:
        stage = 'quiz_kanji'
        quiz_dict_kanji = {}
        i = 0
        for key, elem in dict_kanji.items():
            if checkboxs[i][0]:
                quiz_dict_kanji[key] = elem
            i += 1

def on_click_button_return():
    global stage
    if stage == 'kanji':
        stage = 'apprendre'
    elif stage in ['apprendre', 'options']:
        stage = 'menu'
    elif stage == 'quiz_kanji':
        stage = 'kanji'

def on_click_button_next():
    global choose
    if stage == 'quiz_kanji':
        choose = 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H), RESIZABLE)

checkboxs = []

f = open('kanji.txt','r', encoding="utf8")
message = f.read()
dict_kanji = {}
liste = message.split("\n")
for i in liste:
    mot = i.split("|")
    dict_kanji[mot[0]] = mot[1:]
    checkboxs.append([False, (0, 0)])

f.close()

quiz_dict_kanji = {}

stage = 'menu'

choose = 0
new_kanji = ""
kanji = ""

button_1 = button_create("APPRENDRE", RED, GREEN, on_click_button_1)
button_2 = button_create("OPTIONS", RED, GREEN, on_click_button_2)
button_3 = button_create("QUITTER", RED, GREEN, on_click_button_3)

button_kanji = button_create("KANJI", RED, GREEN, on_click_button_kanji)

button_GO = button_create("GO", RED, GREEN, on_click_button_GO)

button_return = button_create("RETOUR", RED, GREEN, on_click_button_return)

button_next = button_create("Suivant", RED, GREEN, on_click_button_next)

# - mainloop -
            
running = True

while running:

    screen_width, screen_height = screen.get_size()
    
    # - events -
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(checkboxs)):
                if event.pos[0] > checkboxs[i][1][0] and event.pos[0] < checkboxs[i][1][0]+20 and event.pos[1] > checkboxs[i][1][1] and event.pos[1] < checkboxs[i][1][1]+20:
                    if checkboxs[i][0] == True:
                        checkboxs[i][0] = False
                    else:
                        checkboxs[i][0] = True

        if stage == 'menu':
            button_check(button_1, ((3*screen_width)/10, screen_height/5, screen_width/2.5, screen_height/(20/3)), event)
            button_check(button_2, ((3*screen_width)/10, screen_height/2.5, screen_width/2.5, screen_height/(20/3)), event)
            button_check(button_3, ((3*screen_width)/10, screen_height/(5/3), screen_width/2.5, screen_height/(20/3)), event)
        elif stage == 'apprendre':
            button_check(button_kanji, ((3*screen_width)/10, screen_height/5, screen_width/2.5, screen_height/(20/3)), event)
            button_check(button_return, (0, 0, screen_width/5, screen_height/10), event)
        elif stage == 'options':
            button_check(button_return, (0, 0, screen_width/5, screen_height/10), event)
        elif stage == 'kanji':
            button_check(button_return, (0, 0, screen_width/5, screen_height/10), event)
            button_check(button_GO, (screen_width-screen_width/5, 0, screen_width/5, screen_height/10), event)
        elif stage == 'quiz_kanji':
            button_check(button_return, (0, 0, screen_width/5, screen_height/10), event)
            button_check(button_next, (screen_width-screen_width/5, 0, screen_width/5, screen_height/10), event)

    # - draws -
    screen.fill((255, 255, 255))

    if stage == 'menu':
        button_draw(screen, ((3*screen_width)/10, screen_height/5, screen_width/2.5, screen_height/(20/3)), button_1)
        button_draw(screen, ((3*screen_width)/10, screen_height/2.5, screen_width/2.5, screen_height/(20/3)), button_2)
        button_draw(screen, ((3*screen_width)/10, screen_height/(5/3), screen_width/2.5, screen_height/(20/3)), button_3)
    elif stage == 'apprendre':
        button_draw(screen, ((3*screen_width)/10, screen_height/5, screen_width/2.5, screen_height/(20/3)), button_kanji)
        button_draw(screen, (0, 0, screen_width/5, screen_height/10), button_return)
    elif stage == 'options':
        button_draw(screen, (0, 0, screen_width/5, screen_height/10), button_return)
    elif stage == 'kanji':
        i = 1
        j = 1
        nbr_kanji = 0
        liste_kanji = list(dict_kanji.keys())
        japanesefont = pygame.font.Font("ipaexg.ttf", 30)
        while nbr_kanji < len(dict_kanji.keys()):
            text = japanesefont.render(liste_kanji[(j-1)*(screen_width//60-1)+(i-1)], True, BLACK)
            screen.blit(text, (60*i, 60*j+40))
            checkboxs[(j-1)*(screen_width//60-1)+(i-1)][1] = (60*i+35, 60*j+47)
            checkbox_draw(screen, (60*i+35, 60*j+47, 20, 20), BLACK, checkboxs[(j-1)*(screen_width//60-1)+(i-1)][0])

            nbr_kanji += 1
            i += 1
            if 60*i > screen_width-60:
                i = 1
                j += 1

        button_draw(screen, (0, 0, screen_width/5, screen_height/10), button_return)
        button_draw(screen, (screen_width-screen_width/5, 0, screen_width/5, screen_height/10), button_GO)
    elif stage == 'quiz_kanji':
        if choose == 0:
            while new_kanji == kanji:
                new_kanji, new_signification = choice(list(quiz_dict_kanji.items()))
            kanji, signification = new_kanji, new_signification
            choose = 1

        text_draw(screen, kanji, BLACK, (screen_width//2, screen_height//6), 100)

        text_draw(screen, 'Kun: '+signification[0], BLACK, (screen_width//2, screen_height//2.75), 60)
        text_draw(screen, 'On: '+signification[1], BLACK, (screen_width//2, screen_height//1.75), 60)
        text_draw(screen, 'Trad: '+signification[2], BLACK, (screen_width//2, screen_height//1.25), 60)
        
        button_draw(screen, (0, 0, screen_width/5, screen_height/10), button_return)
        button_draw(screen, (screen_width-screen_width/5, 0, screen_width/5, screen_height/10), button_next)

    pygame.display.update()

pygame.quit()
