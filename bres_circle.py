import pygame
import random
import time
import win32gui, win32con  

class CircleDrawer:
    def __init__(self, x0, y0, r, N):
        pygame.init()
        pygame.display.set_caption("Bresenham Circle Drawing")
        self.width = 600
        self.height = 600
        self.N = N
        self.total_time = 0.0
        self.x0 = x0
        self.y0 = y0
        self.r = r
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    @staticmethod
    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def draw_circle(x0, y0, r, color, screen):
        x = 0
        y = r
        d = 3 - 2 * r
        while x <= y:
            screen.set_at((x0 + x, y0 + y), color)
            screen.set_at((x0 - x, y0 + y), color)
            screen.set_at((x0 + x, y0 - y), color)
            screen.set_at((x0 - x, y0 - y), color)
            screen.set_at((x0 + y, y0 + x), color)
            screen.set_at((x0 - y, y0 + x), color)
            screen.set_at((x0 + y, y0 - x), color)
            screen.set_at((x0 - y, y0 - x), color)

            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def run(self):
        running = True
        for _ in range(self.N):
            color = self.random_color()

            start_time = time.time()
            self.draw_circle(self.x0, self.y0, self.r, color, self.screen)
            self.total_time += time.time() - start_time
            self.x0 = random.randint(50, self.width - 50)
            self.y0 = random.randint(50, self.height - 50)
            self.r = random.randint(10, 100)

            pygame.display.update()

        pygame.image.save(self.screen, "bres_circles.png")
        pygame.image.save(self.screen, "static/plot.png")
        
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        print(f"Time taken to draw {self.N} circles is: {self.total_time:.3f} seconds")
        return self.total_time

if __name__ == "__main__":
    # Draw 10 circles centered at (300, 300) with radius 100
    drawer = CircleDrawer(300, 300, 100, N=10)
    drawer.run()
