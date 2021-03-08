import pygame
import random
pygame.init()

screen_width= 480
screen_height = 640

screen = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("똥피하기")

clock =pygame.time.Clock()

background = pygame.image.load("C:/testpy/python_ex/images/pyton_game_background.png")

character = pygame.image.load("C:/testpy/python_ex/images/pyton_game_character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) /2
character_y_pos = screen_height - character_height

to_x=0
to_y=0

enemy = pygame.image.load("C:/testpy/python_ex/images/pyton_game_enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0,screen_width-enemy_width)
enemy_y_pos = 0

character_speed = 1
enemy_speed = 1


running = True
while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x-=character_speed
            elif event.key == pygame.K_RIGHT:
                to_x+=character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos+=to_x * dt
    character_y_pos+=to_y * dt

    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos> screen_width - character_width:
        character_x_pos= screen_width - character_width
    
    enemy_y_pos+=enemy_speed * dt
    
    if enemy_y_pos > screen_height:
        enemy_y_pos=0
        enemy_x_pos = random.randint(0,screen_width-enemy_width)

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos
    
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요!")
        running = False

    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos,character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    pygame.display.update()
    
pygame.time.delay(1000)

pygame.quit()