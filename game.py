import pygame
###########################################################(반드시 필요)
pygame.init() #처음 초기화 하는 기능

#화면 크기 설정
screen_width= 480
screen_height = 640

screen = pygame.display.set_mode((screen_width,screen_height)) #실제로 적용됨

#화면 타이틀 설정
pygame.display.set_caption("Nado Game") #게임 이름 설정

# FPS
clock =pygame.time.Clock()

#########################################################################
# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

#배경 이미지 불러오기
background = pygame.image.load("C:/testpy/python_ex/pyton_game_background.png")

#캐릭터 불러오기
character = pygame.image.load("C:/testpy/python_ex/pyton_game_character.png")
character_size = character.get_rect().size #이미지의 크기를 구해옴
character_width = character_size[0] #캐릭터의 가로 크기
character_height = character_size[1] #캐릭터의 세로 크기
character_x_pos = (screen_width - character_width) /2 #화면 괄호의 절반에 해당하는 곳에 위치하기 위한 값 (가로)
character_y_pos = screen_height - character_height #화면 바닥에 위치하기 위한 값 (세로)

#이동할 좌표
to_x=0
to_y=0

#이동 속도
character_speed = 1

#적 enemy 캐릭터
enemy = pygame.image.load("C:/testpy/python_ex/pyton_game_enemy.png")
enemy_size = enemy.get_rect().size #이미지의 크기를 구해옴
enemy_width = enemy_size[0] #적군의 가로 크기
enemy_height = enemy_size[1] #적군의 세로 크기
enemy_x_pos = (screen_width - enemy_width) /2 #화면 괄호의 절반에 해당하는 곳에 위치하기 위한 값 (가로)
enemy_y_pos = (screen_height - enemy_height) /2 #화면 괄호의 절반에 해당하는 곳에 위치하기 위한 값 (세로)

#이동할 좌표
to_x=0
to_y=0

#이동 속도
character_speed = 1

#폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체 생성 (폰트, 크기)

#총 시간
total_time = 10

# 시간 계산
start_ticks = pygame.time.get_ticks() #현재 tick을 받아옴
#########################################################################


#이벤트 루프 설정 : 게임이 꺼지지 않게 하는 코드
running = True #게임이 진행중인가?
while running:
    dt = clock.tick(60) #게임 화면의 초당 프레임 수
    #프레임때문에 이동속도 제한이 걸리지 않도록 프레임 수를 조정해야한다.

# 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생할 때 
            running=False #게임이 진행중이 아니다.

        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로
                to_x-=character_speed
            elif event.key == pygame.K_RIGHT: #캐릭터를 오른쪽으로
                to_x+=character_speed
            elif event.key == pygame.K_UP: #캐릭터를 위쪽으로
                to_y-=character_speed
            elif event.key == pygame.K_DOWN: #캐릭터를 아래쪽으로
                to_y+=character_speed

        if event.type == pygame.KEYUP: #키를 땠는지 확인
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #캐릭터 좌우로 가던걸 멈춤
                to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN: #캐릭터 상하로 가던걸 멈춤
                to_y = 0
###################################################################################################

# 3. 게임 캐릭터 위치 정의
    #캐릭터의 이동 설정
    character_x_pos+=to_x * dt #dt를 곱해주는 이유는 FPS와 상관없이 속도를 조절하기 위함
    character_y_pos+=to_y * dt

    #가로 경계값 설정
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos> screen_width - character_width:
        character_x_pos= screen_width - character_width
    
    #세로 경계값 설정
    if character_y_pos<0:
        character_y_pos=0
    elif character_y_pos>screen_height - character_height:
        character_y_pos=screen_height - character_height
######################################################################

#4. 충돌 처리
    #충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    #충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요!")
        running = False
###############################################################

# 5. 화면에 그리기
#    screen.fill((127,127,127)) #게임의 색 채우기
    screen.blit(background, (0,0)) #배경 그리기
    screen.blit(character, (character_x_pos,character_y_pos)) #캐릭터 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) #적 캐릭터 그리기

    #타이머 시간 넣기
    #경계 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) /1000
    #경과 시간을 1000으로 나누어 초단위로 표시
    
    timer = game_font.render(str(int(total_time -elapsed_time)),True,(255,255,255))
    #출력할 글자, True, 글자 색상
    screen.blit(timer,(10,10))

    #만약 시간이 0미만이면 게임 종료
    if total_time< elapsed_time:
        print("Time Out!")
        running = False
######################################################################################

# 6. 업데이트 (필수)
    pygame.display.update() # 게임화면 다시 그리기
###########################################################

# 7. 종료전 대기 (없어도 되는 부분)
#잠시 대기 (종료되는 모든 순간에 적용)
pygame.time.delay(2000) #2초 정도 대기 (단위 : ms)
###########################################################

# 8. pygame 종료 (필수)
#게임 종료하고 pygame도 종료 할 때
pygame.quit()
###########################################