#시작하자마자 꺼짐 오류 발견해야함

import os
import pygame
pygame.init()

screen_width= 640
screen_height = 480

screen = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("공 깨기")

clock =pygame.time.Clock()

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
images_path = os.path.join(current_path, "images") #현재 파일 위치에서 images 파일 반환

background = pygame.image.load(os.path.join(images_path, "background.png"))

stage = pygame.image.load(os.path.join(images_path, "stage.png"))
stage_size = stage.get_rect().size #이미지의 크기를 구해옴
stage_height = stage_size[1] #stage의 세로 크기

character = pygame.image.load(os.path.join(images_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) /2
character_y_pos = screen_height - character_height-stage_height

#이동할 좌표
character_to_x=0

#이동 속도
character_speed = 1

# weapon 무기
weapon = pygame.image.load(os.path.join(images_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 한번에 여러발 발사 가능
weapons = []
weapon_speed = 5


# ball 공(4가지)
ball_images = [
    pygame.image.load(os.path.join(images_path, "balloon1.png")),
    pygame.image.load(os.path.join(images_path, "balloon2.png")),
    pygame.image.load(os.path.join(images_path, "balloon3.png")),
    pygame.image.load(os.path.join(images_path, "balloon4.png"))
    ]

#공 크기에 대한 최초의 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공들
balls = []

balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y" : 50, #공의 y좌표
    "img_idx" : 0, #공의 이미지 index
    "to_x" : 3, #x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
    "to_y" : -6, #y축 이동방향,
    "init_spd_y" : ball_speed_y[0]#y의 최초속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

#Font 정의
game_font = pygame.font.Font(None,40)
total_time = 100
start_ticks = pygame.time.get_ticks() #시작 시간 정의

# 게임 종료 메시지
# Time Out(시간 초과, 실패)
# Mission Complete (성공)
# Game Over (캐릭터에 공 맞음, 실패)
game_result = "Game Over"

#이벤트 루프 설정 : 게임이 꺼지지 않게 하는 코드
running = True
while running:
    dt = clock.tick(60) #게임 화면의 초당 프레임 수
    #프레임때문에 이동속도 제한이 걸리지 않도록 프레임 수를 조정해야한다.

# 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생할 때 
            running=False #게임이 진행중이 아니다.

        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로
                character_to_x-=character_speed
            elif event.key == pygame.K_RIGHT: #캐릭터를 오른쪽으로
                character_to_x+=character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width - weapon_width)/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])

        if event.type == pygame.KEYUP: #키를 땠는지 확인
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #캐릭터 좌우로 가던걸 멈춤
                character_to_x = 0


# 3. 게임 캐릭터 위치 정의
    #캐릭터의 이동 설정
    character_x_pos+=character_to_x * dt #dt를 곱해주는 이유는 FPS와 상관없이 속도를 조절하기 위함

    #가로 경계값 설정
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos> screen_width - character_width:
        character_x_pos= screen_width - character_width

    weapons = [[w[0],w[1] - weapon_speed] for w in weapons]# 무기 위치를 위로
    weapons = [[w[0],w[1]] for w in weapons if w[1] > 0 ]# 무기 위치를 위로

    # 공의 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]    
        ball_img_idx=ball_val["img_idx"]

        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로 벽에 닿았을 때, 공 이동 위치 변경(튕겨 나오는 효과)
        if ball_pos_x <0 or ball_pos_x>screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * (-1)

        #세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >=screen_height -stage_height -ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"]+=0.5

        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]

# 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]    
        ball_img_idx=ball_val["img_idx"]

        #공의 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx #해당 공 없애기 위한 값 설정
                
                #가장 작은 공이 아니면 다음 단계 공으로 나눠준다.
                if ball_img_idx < 3:
                    #현재 공 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튕겨나가는 작은 공                                    
                    balls.append({
                        "pos_x" : ball_pos_x +(ball_width-small_ball_width)/2, #공의 x좌표
                        "pos_y" : ball_pos_y+(ball_height-small_ball_height)/2, #공의 y좌표
                        "img_idx" : ball_img_idx+1, #공의 이미지 index
                        "to_x" : -3, #x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
                        "to_y" : -6, #y축 이동방향,
                        "init_spd_y" : ball_speed_y[ball_img_idx+1]#y의 최초속도
                    })
                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x +(ball_width-small_ball_width)/2, #공의 x좌표
                        "pos_y" : ball_pos_y+(ball_height-small_ball_height)/2, #공의 y좌표
                        "img_idx" : ball_img_idx+1, #공의 이미지 index
                        "to_x" : 3, #x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
                        "to_y" : -6, #y축 이동방향,
                        "init_spd_y" : ball_speed_y[ball_img_idx+1 ]#y의 최초속도
                    })

                break
        else: # 계속 게임을 진행
            continue # 안쪽 for 문 조건이 맞지 않으면 continue. 바깥 for 문 계속 수행
        break # 안쪽 for 문에서 break 를 만나면 여기로 진입 2중 for문을 한번에 탈출

    #충돌된 공과 무기 없애기
    if ball_to_remove>-1:
        del balls[ball_to_remove]
        ball_to_remove=-1

    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1

    #모든 공이 없어졌을 때 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

# 5. 화면에 그리기
    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos,weapon_y_pos))
    
    for idx, val in enumerate(balls):
        ball_pos_x= val["pos_x"]
        ball_pos_y= val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))     

    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character, (character_x_pos,character_y_pos)) #캐릭터 그리기

    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks)/1000 #ms->s
    timer = game_font.render(f"Time : {int(total_time-elapsed_time)}", True, (255,255,255))
    screen.blit(timer, (10,10))

    #시간이 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Out"
        running = False


    pygame.display.update()

#게임 오버 메시지
msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(screen_width//2,screen_height//2))
screen.blit(msg, msg_rect)
pygame.display.update()

#2초 대기
pygame.time.delay(2000)

pygame.quit()