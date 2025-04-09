import pygame
import random
import time
import win32gui, win32con  

class CircleDrawer:
    def __init__(self, width=800, height=600, N=1):
        pygame.init()
        self.width = width
        self.height = height
        self.N = N
        self.total_time = 0.0
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
            x0 = random.randint(50, self.width - 50)
            y0 = random.randint(50, self.height - 50)
            r = random.randint(10, 50)
            color = self.random_color()

            start_time = time.time()
            self.draw_circle(x0, y0, r, color, self.screen)
            self.total_time += time.time() - start_time

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            if not running:
                break
        pygame.image.save(self.screen, "bres_circles.png")
        pygame.time.wait(2000)
        pygame.quit()
        print(f"Time taken to draw {self.N} circles is: {self.total_time:.3f} seconds")

if __name__ == "__main__":
    drawer = CircleDrawer()
    drawer.run()
