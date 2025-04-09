# dda_module.py
import pygame
import random
import time
import win32gui, win32con  


class DDADrawer:
    def __init__(self, x1, y1, x2, y2, N):
        pygame.init()
        self.window_size = 600
        self.n_lines = N
        self.total_time = 0.0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("DDA")
        
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


    @staticmethod
    def dda(x1, y1, x2, y2, color, surface):
        dx = x2 - x1
        dy = y2 - y1
        
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        
        x, y = x1, y1
        
        for _ in range(steps + 1):
            surface.set_at((round(x), round(y)), color)
            x += x_inc
            y += y_inc

    def run(self):
        self.screen.fill((0, 0, 0))
        running = True

        for _ in range(self.n_lines):
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
            
            start_time = time.time()
            self.dda(self.x1, self.y1, self.x2, self.y2, color, self.screen)
            self.total_time += time.time() - start_time
            self.x1 = random.randint(0, self.window_size - 1)
            self.y1 = random.randint(0, self.window_size - 1)
            self.x2 = random.randint(self.x1 + 1, self.window_size - 1)
            self.y2 = random.randint(self.y1, self.window_size - 1)
            
            pygame.display.update()
            
            running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.image.save(self.screen, "static/plot.png")

        pygame.quit()
        print(f"Time taken to draw {self.n_lines} lines is: {self.total_time:.3f} seconds")
        return self.total_time

if __name__ == "__main__":
    drawer = DDADrawer(50, 50, 550, 550, n_lines=10)
    drawer.run()
