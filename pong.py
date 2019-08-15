import random, pygame, sys
from math import radians, cos, sin
from pygame.locals import *

FPS = 60 # frames per second, the general speed of the program
WINDOWWIDTH = 480 # size of window's width in pixels
WINDOWHEIGHT = 640 # size of windows' height in pixels
PADDLE_WIDTH = 50
PADDLE_HEIGHT = 10
paddleSpeed = 3.5
ballSpeed = 5
ballSize = 10

#            R    G    B
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)

BGCOLOR = NAVYBLUE

def getBallDirection():
    angle = random.randint(0,360)
    while angle % 90 == 0:
        angle = random.randint(0, 360)
    return angle

def getWallDirection(angle):
    reflected_angle = 360 - angle
    return reflected_angle

def getPaddleContactDirection(angle):
    if angle < 180:
        reflected_angle = 180 - angle
    elif angle > 180:
        reflected_angle = 540 - angle
    return reflected_angle

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.mixer.init(22100, -16, 2, 64)
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FONT = pygame.font.SysFont("impact", 20)
    pygame.display.set_caption('PONG')
    pygame.mixer.music.load("hit_sound.wav")
    
    paddleX = WINDOWWIDTH/2 -25
    paddleY = WINDOWHEIGHT - 20
    direction = 0

    paddleX2 = WINDOWWIDTH / 2 - 25
    paddleY2 = 10
    direction2 = 0

    ballX = WINDOWWIDTH / 2
    ballY = WINDOWHEIGHT / 2
    ballDirection = getBallDirection()

    score = [0,0]

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = -1
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                if event.key == pygame.K_a:
                    direction2 = -1
                elif event.key == pygame.K_d:
                    direction2 = 1
                elif event.key == pygame.K_SPACE:
                    score = [0, 0]
                    ballX = WINDOWWIDTH / 2
                    ballY = WINDOWHEIGHT / 2
                    ballDirection = getBallDirection()
            state = pygame.key.get_pressed()
            if not state[pygame.K_LEFT] and not state[pygame.K_RIGHT]:
                direction = 0
            if not state[pygame.K_a] and not state[pygame.K_d]:
                direction2 = 0

        paddleX += direction * paddleSpeed
        paddleX2 += direction2 * paddleSpeed

        if (ballY - ballSize)>= WINDOWHEIGHT: #paddle 1 side (bottom)
            ballDirection = getBallDirection()
            ballX = WINDOWWIDTH / 2
            ballY = WINDOWHEIGHT / 2
            score[1] = score[1] + 1
        elif (ballY - ballSize)<= 0: #paddle 2 side (top)
            ballDirection = getBallDirection()
            ballX = WINDOWWIDTH / 2
            ballY = WINDOWHEIGHT / 2
            score[0] = score[0] + 1
        elif (ballX + ballSize) >= WINDOWWIDTH or (ballX - ballSize) <= 0:
            ballDirection = getWallDirection(ballDirection)
        elif (ballY + ballSize)>=(WINDOWHEIGHT - 20) and (paddleX)<=ballX<=(paddleX + 50): # for the paddle 1
            ballDirection = getPaddleContactDirection(ballDirection)
            pygame.mixer.music.play(0)
        elif (ballY - ballSize)<=20 and (paddleX2)<=ballX<=(paddleX2 + 50): # for the paddle 2
            ballDirection = getPaddleContactDirection(ballDirection)
            pygame.mixer.music.play(0)
        ballX += sin(radians(ballDirection)) * ballSpeed
        ballY += cos(radians(ballDirection)) * ballSpeed * -1

        DISPLAYSURF.fill(BGCOLOR)
        if score[0] == 2:
            text = FONT.render("Player 1 Wins", True, WHITE)
            DISPLAYSURF.blit(text, (WINDOWWIDTH / 2 - text.get_width() // 2, WINDOWHEIGHT / 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(1000)
            score = [0, 0]
            ballDirection = getBallDirection()
        elif score[1] ==2:
            text = FONT.render("Player 2 Wins", True, WHITE)
            DISPLAYSURF.blit(text, (WINDOWWIDTH / 2 - text.get_width() // 2, WINDOWHEIGHT / 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(1000)
            score = [0, 0]
            ballDirection = getBallDirection()
        else:
            scoreSTR = [str(x) for x in score]
            text = FONT.render("-".join(scoreSTR), True, WHITE)
            DISPLAYSURF.blit(text, (WINDOWWIDTH / 2 - text.get_width() // 2, WINDOWHEIGHT / 2 - text.get_height() // 2))
            pygame.draw.rect(DISPLAYSURF, WHITE, (paddleX, paddleY, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.rect(DISPLAYSURF, WHITE, (paddleX2, paddleY2, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.circle(DISPLAYSURF, WHITE, (int(ballX), int(ballY)), ballSize)

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
