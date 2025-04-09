import pygame
import random
import time

pygame.init()

N=3000
T_time = 0

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
def midPointCircleDraw(x_centre, y_centre, r, surface):
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    
    x = 0
    y = r
    p = 1 - r  

    while x <= y:
        drawSymmetricPoints(x_centre, y_centre, x, y, surface, color)

        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * (x - y) + 5
            y -= 1

        x += 1
def drawSymmetricPoints(x_centre, y_centre, x, y, surface, color):
    points = [
        (x_centre + x, y_centre + y),
        (x_centre - x, y_centre + y),
        (x_centre + x, y_centre - y),
        (x_centre - x, y_centre - y),
        (x_centre + y, y_centre + x),
        (x_centre - y, y_centre + x),
        (x_centre + y, y_centre - x),
        (x_centre - y, y_centre - x)
    ]
    
    for point in points:
        surface.set_at(point, color)  
win.fill((0,0,0))  
for _ in range(N):
    x_centre = random.randint(50, WIDTH - 50)
    y_centre = random.randint(50, HEIGHT - 50)
    r = random.randint(10, 100)

    start_time = time.time()
    midPointCircleDraw(x_centre, y_centre, r, win)
    end_time = time.time()
    T_time = end_time - start_time
    
    pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()

print(f"Time taken to draw {N} circles is: {(T_time):.3f} seconds")