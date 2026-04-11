import pygame

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60


pygame.init() # 1
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) # 2
pygame.display.set_caption("Моя игра") # 3
clock = pygame.time.Clock() # 4

font = pygame.font.SysFont(None, 50)

paddle_speed = 7
ball_active = False
ball_speed_x = 5
ball_speed_y = 5

left_paddle = pygame.Rect(0, 0, 10, 70)
right_paddle = pygame.Rect(0, 0, 10, 70)

left_paddle.midleft = (10, HEIGHT // 2)
right_paddle.midright = (WIDTH - 10, HEIGHT // 2)

ball = pygame.Rect(0, 0, 10, 10)
ball.midleft = (20, HEIGHT // 2)

left_score = 0
right_score = 0
serve_count = 0  # Счетчик текущих подач
current_server = "left"
running = True

while running: # 5
    clock.tick(FPS) 

    for event in pygame.event.get(): # 6
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            
            left_paddle.midleft = (10, HEIGHT // 2)
            right_paddle.midright = (WIDTH - 10, HEIGHT // 2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
        if not ball_active and current_server == "left": 
            ball_speed_y = -5
            ball_active = True

    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed
        if not ball_active and current_server == "left": 
            ball_speed_y = 5
            ball_active = True        

    if keys[pygame.K_o] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
        if not ball_active and current_server == "right": 
            ball_speed_y = -5
            ball_active = True

    if keys[pygame.K_l] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed    
        if not ball_active and current_server == "right": 
            ball_speed_y = 5
            ball_active = True
        
    if ball_active:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1  #  

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1          

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_active = False
        serve_count += 1
        if ball.left <= 0: 
            right_score += 1
        else: 
            left_score += 1

        left_paddle.midleft = (10, HEIGHT // 2)
        right_paddle.midright = (WIDTH - 10, HEIGHT // 2)
        
        if serve_count >= 5:
            serve_count = 0
            if current_server == "left":
                current_server = "right"
            else:
                current_server = "left"

        if current_server == "left":
            ball.midleft = (20, HEIGHT // 2)
        else:
            ball.midright = (WIDTH - 20, HEIGHT // 2)

    screen.fill(BLACK) # 7

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip() # 8

pygame.quit() # 9
