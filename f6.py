import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Hopper')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
obs_gap = 200
obs_frequency = 1500 #milliseconds
last_obs = pygame.time.get_ticks() - obs_frequency
score = 0
pass_obs = False

#load images
bg = pygame.image.load('bg1.png')
ground_img = pygame.image.load('ground1.png')
button_img = pygame.image.load('restart1.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    obs_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class ast(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ast1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 582:
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

class obs(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obs1.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(obs_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(obs_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

ast_group = pygame.sprite.Group()
obs_group = pygame.sprite.Group()

flappy = ast(100, int(screen_height / 2))
ast_group.add(flappy)

#create restart button instance
button = Button(screen_width // 2 -100, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    ast_group.draw(screen)
    ast_group.update()
    obs_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 582))

    #check the score
    if len(obs_group) > 0:
        if ast_group.sprites()[0].rect.left > obs_group.sprites()[0].rect.left\
            and ast_group.sprites()[0].rect.right < obs_group.sprites()[0].rect.right\
            and pass_obs == False:
            pass_obs = True
        if pass_obs == True:
            if ast_group.sprites()[0].rect.left > obs_group.sprites()[0].rect.right:
                score += 1
                pass_obs = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    #look for collision
    if pygame.sprite.groupcollide(ast_group, obs_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #check if ast has hit the ground
    if flappy.rect.bottom >= 582:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        #generate new obss
        time_now = pygame.time.get_ticks()
        if time_now - last_obs > obs_frequency:
            obs_height = random.randint(-100, 100)
            btm_obs = obs(screen_width, int(screen_height / 2) + obs_height, -1)
            top_obs = obs(screen_width, int(screen_height / 2) + obs_height, 1)
            obs_group.add(btm_obs)
            obs_group.add(top_obs)
            last_obs = time_now

        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        obs_group.update()

    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
