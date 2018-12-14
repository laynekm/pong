import pygame
import random
pygame.init()

size = (720, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

ready = False
done = False
paused = False

colours = [(250, 0, 0),     #red
           (255, 128, 0),   #orange
           (51, 204, 51),   #green
           (191, 0, 255),   #violet
           (255, 0, 191),   #magenta
           (0, 0, 0),       #black
           (255, 255, 0),   #yellow
           (255, 255, 255)] #white

canvasColour = colours[5]
elementColour = colours[7]

class Paddle:
    def __init__(self, x, y, w, h, dy, score):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dy = dy
        self.score = score

class Ball:
    def __init__(self, x, y, r, dx, dy):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy

p1 = Paddle(18, 215, 15, 60, 5, 0)
p2 = Paddle(683, 215, 15, 60, 5, 0)
ball1 = Ball(360, 240, 5, 2, 0)
ball2 = Ball(360, 240, 5, -2, 0)
ball3 = Ball(360, 240, 5, 1, 1)
balls = [ball1, ball2, ball3]

def changeColour():
    randInt = random.randint(0, 7)
    newCanvasColour = colours[randInt]
    if(randInt > 5):
        newElementColour = colours[5]
    else:
        newElementColour = colours[7]
    return [newCanvasColour, newElementColour]

def draw():
    global ready
    screen.fill(canvasColour)
    pygame.draw.rect(screen, elementColour, [p1.x, p1.y, p1.w, p1.h])
    pygame.draw.rect(screen, elementColour, [p2.x, p2.y, p2.w, p2.h])

    for ball in balls:
        pygame.draw.circle(screen, elementColour, [ball.x, ball.y], ball.r)

    for i in range (0, 480, 20):
        pygame.draw.line(screen, elementColour, [360, i], [360, i + 10])

    if not ready:
        font = pygame.font.SysFont("monospace", 20)
        menuText1 = font.render('Press space to start!', 1, elementColour)
        menuText2 = font.render('Player 1 (left) uses W/S, Player 2 (right) uses UP/DOWN', 1, elementColour)
        screen.blit(menuText1, (10, 10))
        screen.blit(menuText2, (10, 50))
    else:
        font = pygame.font.SysFont("monospace", 25)
        p1ScoreText = font.render(str(p1.score), 1, elementColour)
        p2ScoreText = font.render(str(p2.score), 1, elementColour)
        screen.blit(p1ScoreText, (720/4, 40))
        screen.blit(p2ScoreText, (720/4*3, 40))
    if paused:
        font = pygame.font.SysFont("monospace", 20)
        pauseText = font.render('Paused', 1, elementColour)
        screen.blit(pauseText, (10, 10))

def startup():
    global done
    global ready
    while not done and not ready:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                done = True

        key = pygame.key.get_pressed()
        if(key[pygame.K_SPACE]):
            ready = True

        draw()
        pygame.display.flip()
        clock.tick(60)
    play()

def play():
    global done
    global paused
    while not done:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                    done = True

        key = pygame.key.get_pressed()

        #handle pausing
        if(key[pygame.K_p]):
            if not paused:
                paused = True
            else:
                paused = False
            pygame.time.wait(100)

        if paused:
            draw()
            pygame.display.flip()
            clock.tick(60)
            continue

        #handle paddle movement
        if(key[pygame.K_w] and p1.y >= 0):
            p1.y -= p1.dy
        if(key[pygame.K_s] and p1.y + p1.h <= 480):
            p1.y += p1.dy
        if(key[pygame.K_UP] and p2.y >= 0):
            p2.y -= p2.dy
        if(key[pygame.K_DOWN] and p2.y + p2.h <= 480):
            p2.y += p2.dy

        #handle ball movement
        for ball in balls:
            ball.x += ball.dx
            ball.y += ball.dy

            #collission with walls
            if(ball.y - ball.r <= 0):
                ball.dy *= -1
            if(ball.y + ball.r >= 480):
                ball.dy *= -1

            #collission with paddles, give a buffer of a couple pixels
            if(ball.x - ball.r >= p1.x + p1.w - 1
               and ball.x - ball.r <= p1.x + p1.w + 1
               and ball.y >= p1.y
               and ball.y <= p1.y + p1.h):
                ball.dx *= -1
                ball.dy = random.randint(0, 2)
            if(ball.x + ball.r <= p2.x + 1
               and ball.x + ball.r >= p2.x - 1
               and ball.y >= p2.y
               and ball.y <= p2.y + p2.h):
                ball.dx *= -1
                ball.dy = random.randint(0, 2)

            #scoring and replacing ball
            if(ball.x >= 720):
                p1.score += 1
                ball.x = 360
                ball.y = 240
                ball.dx *= -1
                ball.dy = random.randint(0, 2)
                newColours = changeColour()
                canvasColour = newColours[0]
                elementColour = newColours[1]
            if(ball.x <= 0):
                p2.score += 1
                ball.x = 360
                ball.y = 240
                ball.dx *= -1
                ball.dy = random.randint(0, 2)
                newColours = changeColour()
                canvasColour = newColours[0]
                elementColour = newColours[1]

        draw()
        pygame.display.flip()
        clock.tick(60)

startup()
pygame.quit()
