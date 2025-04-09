import pygame
import random
import time
import win32gui, win32con
import winsound


class BresenhamDrawer:
    def __init__(self, N, x1=None, y1=None, x2=None, y2=None):
        pygame.init()
        pygame.display.set_caption("Bresenham Line Drawing")

        self.N = N
        self.WINDOW_SIZE = 600
        self.total_time = 0.0
        self.fixed_coords = (x1, y1, x2, y2)

        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        self.screen.fill((0, 0, 0))

        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    @staticmethod
    def bresenham(x1, y1, x2, y2, color, surface):
        x, y = x1, y1
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dt = 2 * (dy - dx)
        ds = 2 * dy
        d = 2 * dy - dx

        surface.set_at((x, y), color)
        while x < x2:
            x += 1
            if d < 0:
                d += ds
            else:
                y += 1
                d += dt
            if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                surface.set_at((x, y), color)

    def run(self):
        for _ in range(self.N):
            while True:
                x1 = random.randint(0, self.WINDOW_SIZE - 1)
                y1 = random.randint(0, self.WINDOW_SIZE - 1)
                x2 = random.randint(x1 + 1, self.WINDOW_SIZE - 1)
                y2 = random.randint(y1, self.WINDOW_SIZE - 1)
                if x1 != x2 and 0 <= (y2 - y1) / (x2 - x1) <= 1:
                    break
          
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )

            start_time = time.time()
            self.bresenham(x1, y1, x2, y2, color, self.screen)
            self.total_time += time.time() - start_time

            pygame.display.update()

        pygame.image.save(self.screen, "bresenham_lines.png")
        pygame.image.save(self.screen, "static/plot.png")
        
        winsound.MessageBeep()
        print(f"Image saved as 'bresenham_lines.png'")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        print(f"Time taken to draw {self.N} lines is: {self.total_time:.3f} seconds")
        return self.total_time


if __name__ == "__main__":
    drawer = BresenhamDrawer(N=10, x1=100, y1=100, x2=400, y2=300)

    drawer.run()
