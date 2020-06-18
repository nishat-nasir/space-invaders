import math
import random
import time
import pygame
import os
from pygame import mixer

pygame.init()
pygame.font.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

clock = pygame.time.Clock()
# main menu
main_menu = pygame.image.load('main_menu.png')
green = (0, 200, 0)
bright_green = (0, 255, 0)

# Sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)+


# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Ready = can't see the bullet on the screen
# Fire = bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Enemy
num_of_enemies = 3

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Menu press enter
press_enter = font.render("Press Enter", True, green)

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

red = (255, 0, 0)
green = (0, 200, 0)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, green)
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


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


# Enemy
# speed of enemy according to level of the game
class enemy_lvl:
    def __init__(self, enemy_speed_x, enemy_speed_y, level=100):
        self.speed_x = enemy_speed_x
        self.speed_y = enemy_speed_y

    # method
    def speed_level(self):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = self.speed_x
            enemyY[i] += enemyY_change[i]
            clock.tick(60)
        elif enemyX[i] >= 736:
            enemyX_change[i] = self.speed_y
            enemyY[i] += enemyY_change[i]


# Boss Class

class Boss:
    def __init__(self, boss_pic, boss_pos_X, boss_pos_Y, boss_move_X):
        self.boss_pic = boss_pic
        self.boss_pos_X = boss_pos_X
        self.boss_pos_Y = boss_pos_Y
        self.boss_move_X = boss_move_X

    def Boss_level(self):
        screen.blit(self.boss_pic, (self.boss_pos_X, self.boss_pos_Y))
        self.boss_pos_X += self.boss_move_X
        if self.boss_pos_X <= 0:
            self.boss_move_X = 1
        elif self.boss_pos_X >= 640:
            self.boss_move_X = -1

    def Boss_collision(self, bulletX, bulletY):
        distance = math.sqrt(math.pow(self.boss_pos_X - bulletX, 2) + (math.pow(self.boss_pos_Y - bulletY, 2)))
        print(distance)
        if distance < 200:
            return True
        else:
            return False


# objects for enemy speed level
enemy_level_one = enemy_lvl(2, -2)
enemy_level_two = enemy_lvl(5, -5)
enemy_level_three = enemy_lvl(8, -8)
# boss object
boss_lvl_1_img = pygame.image.load('boss_level_1.png')
boss_lvl_1 = Boss(boss_lvl_1_img, 320, 50, 3)

# Game Loop
run = True
menu_run = True
while run:
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    screen.blit(main_menu, (0, 0))
    screen.blit(press_enter, (300, 320))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Keydown = press key
        # keyup = don't press key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = True
                while running:
                    # RGB = Red, Green, Blue
                    screen.fill((0, 0, 0))
                    # Background Image
                    screen.blit(background, (0, 0))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            # close both (game and main_menu)
                            run = False
                            running = False

                        # if keystroke is pressed check whether its right or left
                        if event.type == pygame.KEYDOWN:
                            # close game and return to main menu
                            if event.key == pygame.K_ESCAPE:
                                running = False

                            if event.key == pygame.K_LEFT:
                                playerX_change = -5
                            if event.key == pygame.K_RIGHT:
                                playerX_change = 5
                            if event.key == pygame.K_SPACE:
                                if bullet_state is "ready":
                                    bulletSound = mixer.Sound("laser.wav")
                                    bulletSound.play()
                                    # Get the current x coordinate of the spaceship
                                    bulletX = playerX
                                    fire_bullet(bulletX, bulletY)

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                playerX_change = 0

                    playerX += playerX_change
                    if playerX <= 0:
                        playerX = 0
                    elif playerX >= 736:
                        playerX = 736

                    # Enemy Movement
                    for i in range(num_of_enemies):

                        # Game Over
                        if enemyY[i] > 440:
                            for j in range(num_of_enemies):
                                enemyY[j] = 2000
                            game_over_text()
                            break

                        if 0 <= score_value < 5:
                            enemy_level_one.speed_level()
                            img = font.render("Level 1", True, green)
                            screen.blit(img, (680, 10))
                            enemy(enemyX[i], enemyY[i], i)

                        elif 5 <= score_value < 10:
                            enemy_level_two.speed_level()
                            img = font.render("Level 2", True, green)
                            screen.blit(img, (680, 10))
                            enemy(enemyX[i], enemyY[i], i)

                        elif 10 <= score_value < 15:
                            enemy_level_three.speed_level()
                            img = font.render("Level 3", True, green)
                            screen.blit(img, (680, 10))
                            enemy(enemyX[i], enemyY[i], i)

                        elif 15 <= score_value < 25:
                            boss_lvl_1.Boss_level()
                            img = font.render("Boss", True, red)
                            screen.blit(img, (680, 10))
                        else:
                            running = False

                        # Enemy Collision
                        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                        if collision:
                            explosionSound = mixer.Sound("explosion.wav")
                            explosionSound.play()
                            bulletY = 480
                            bullet_state = "ready"
                            score_value += 1
                            enemyX[i] = random.randint(0, 736)
                            enemyY[i] = random.randint(50, 150)

                        # Boss collision

                        bossCollision = boss_lvl_1.Boss_collision(0, 40)
                        if bossCollision:
                            explosionSound = mixer.Sound("explosion.wav")
                            explosionSound.play()
                            bulletY = 480
                            bullet_state = "ready"
                            score_value += 1

                    clock.tick(60)

                    # Bullet Movement
                    if bulletY <= 0:
                        bulletY = 480
                        bullet_state = "ready"

                    if bullet_state is "fire":
                        fire_bullet(bulletX, bulletY)
                        bulletY -= bulletY_change + 10

                    player(playerX, playerY)
                    show_score(textX, testY)
                    pygame.display.update()

            elif event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()
