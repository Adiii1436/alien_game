from pygame import mixer
import pygame
import random
import math


pygame.init()

screen = pygame.display.set_mode((900, 600))
background = pygame.image.load("5471985.bmp")
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Arcade Shooting")
icon = pygame.image.load("ufo(2).png")
pygame.display.set_icon(icon)


# Making a space ship
player_img = pygame.image.load("space-invaders.bmp")
player_x = 430
player_y = 535
player_x_change = 0


# displaying space ship on the screen
def player(x, y):
    screen.blit(player_img, (x, y))


# movement of spaceship
def spacemov(player_x, player_x_change):
    player_x += player_x_change

    # conditions for restricting space ship inside the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 836:
        player_x = 836

    return player_x


# Making an alien ship
alien_img = pygame.image.load("ufo(1).png")
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
no_of_aliens = 10


#Making fleet of aliens appear randomly
for i in range(no_of_aliens):
    alien_x.append(random.randint(0, 835))
    alien_y.append(random.randint(10, 200))
    alien_x_change.append(0.3)
    alien_y_change.append(60)


# displaying alien ship on the screen
def alien(x, y):
    screen.blit(alien_img, (x, y))


#Displaying score 
score = 0
font = pygame.font.Font("freesansbold.ttf", 28)
text_x = 10
text_y = 10


def show_score(x, y):
    score_value = font.render("Score: "+str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


# Making an bullet
bullet_img = pygame.image.load("bullet.bmp")
bullet_x = 0
bullet_y = 535
bullet_x_change = 0
bullet_y_change = 5
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


#Checking collision between aliens and bullets
def iscollision(alien_x, alien_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(alien_x-bullet_x, 2) +
                         math.pow(alien_y-bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (247, 250))


# Actual game runs here
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # For movement of space ship
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.4
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # alien and space ship movement
    player_x = spacemov(player_x, player_x_change)

    for i in range(no_of_aliens):

        # game over
        if alien_y[i] > 500:
            for j in range(no_of_aliens):
                alien_y[j] = 2000
            game_over_text()
            break

        alien_x[i] += alien_x_change[i]
        if alien_x[i] <= 0:
            alien_x_change[i] = 0.3
            alien_y[i] += alien_y_change[i]
        elif alien_x[i] >= 836:
            alien_x_change[i] = -0.3
            alien_y[i] += alien_y_change[i]

        collision = iscollision(alien_x[i], alien_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 535
            bullet_state = "ready"
            score += 1
            alien_x[i] = random.randint(0, 835)
            alien_y[i] = random.randint(10, 200)

        alien(alien_x[i], alien_y[i])

    # bullet firing
    if bullet_y <= 0:
        bullet_y = 535
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet_y -= bullet_y_change
        fire_bullet(bullet_x, bullet_y)

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
