import math
import random
from collections import namedtuple
import serial
import pygame
from pygame import mixer
# Intialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
Colour= namedtuple('Color',['red','green','blue'])
rectColor = Colour(0,0,0)
# Background
background = pygame.image.load('./backgroundImage.png')
rect= pygame.draw.rect(screen,rectColor,[0,0,100,100])
# Sound
winsound = pygame.mixer.Sound("./pluck-loop-91bpm-132429.mp3")
mixer.music.load("backgrounds.wav")
mixer.music.play(-1)
#joystick
import serial
arduino = serial.Serial('COM6', 9600)
def read_arduino_data():
    try:
        serial_data = arduino.readline().decode().strip().split(",")
        joystick_x = int(serial_data[0])
        joystick_y = int(serial_data[1])
        print(joystick_x,joystick_y)
    except (ValueError, IndexError):
        joystick_x, joystick_y = 0, 0
    # Map joystick values to directions
    if joystick_x > 520:
        direction_x = 'right'
    elif joystick_x < 500:
        direction_x = 'left'
    else:
        direction_x = 'center'
    if joystick_y > 540:
        direction_y = 'up'
    elif joystick_y < 520:
        direction_y = 'down'
    else:
        direction_y = 'center'
    return direction_x, direction_y
# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('uf.png')
pygame.display.set_icon(icon)
# Player
playerImg = pygame.image.load('gun.png')
playerX = 370
playerY = 480
playerX_change = 0
# playerY_change = 0
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemies.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(30)
    enemyY_change.append(10)
# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullets.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10
# Game Over
textFont = pygame.font.Font('freesansbold.ttf', 64)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text = textFont.render("GAME OVER YOU LOOSE", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def win_text():
    win = textFont.render("You Win !!!!!", True, (255, 255, 255))
    screen.blit(win, (200, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen,rectColor,[2,500,1000,4])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         playerX_change = -5
        #     if event.key == pygame.K_RIGHT:
        #         playerX_change = 5
    x, y = read_arduino_data()
    print(x,y)
    # Dtermine direction based on joystick position
     # Joystick is tilted more horizontally
    if x == 'right':     playerX_change = 15     # Right
    elif x == 'left':   playerX_change = -15
    else :playerX_change=0    # Left
    # else:  # Joystick is tilted more vertically
    #     if y > 512:       playerY_change = 5   # Down
    #     elif y < 512:      playerY_change = 5 
    if y == 'up':
        if bullet_state is "ready":
            bulletSound = mixer.Sound("lasers.wav")
            bulletSound.play()
            # Get the current x cordinate of the spaceship
            bulletX = playerX
            fire_bullet(bulletX, bulletY)
    # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        #         playerX_change = 0
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # playerY += playerY_change
    # if playerY <= 0:
    #     playerY = 0
    # elif playerY >= 736:
    #     playerY = 736
    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -8
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosions.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if score_value == 20 :
       num_of_enemies = 0
       background = pygame.image.load('./backG.png')
       winsound.play()
       screen.blit(background, (0, 0))
       win_text()
    #    running = False
    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

