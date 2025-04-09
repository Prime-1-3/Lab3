from tkinter.tix import WINDOW
import pygame
import random
import time


WINDOW_SIZE = 700
  
pygame.init()

win = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("DDA")


n = 3000 
T_time = 0

def dda(x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    
    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1

    for _ in range(steps + 1):
        win.set_at((round(x), round(y)), color) 
        x += x_inc
        y += y_inc

win.fill((0, 0, 0))  

running = True
for i in range(n): 
    x1, y1 = random.randint(0, WINDOW_SIZE-1), random.randint(0, WINDOW_SIZE-1)
    x2, y2 = random.randint(0, WINDOW_SIZE-1), random.randint(0, WINDOW_SIZE-1)
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    start_time = time.time()
    dda(x1, y1, x2, y2, color)  
    end_time = time.time()
    T_time += (end_time - start_time)

    pygame.display.update()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    if not running:
        break


# time.sleep(2) 
pygame.quit()

print(f"Time taken to draw {n} lines is: {(T_time):.3f} seconds")