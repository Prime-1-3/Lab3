# midpoint_circle_module.py
import pygame
import random
import time
import win32gui, win32con
import winsound  # For system beep (Windows only)


class MidpointCircleDrawer:
    def __init__(self, N, x0=None, y0=None, r=None):
        
        pygame.init()
        pygame.display.set_caption("Midpoint Circle Drawing")
        self.width = 600
        self.height = 600
        self.N = N
        self.total_time = 0.0

        self.fixed_x0 = x0
        self.fixed_y0 = y0
        self.fixed_r = r

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))

        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    @staticmethod
    def draw_symmetric_points(x_centre, y_centre, x, y, surface, color):
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
            if 0 <= point[0] < surface.get_width() and 0 <= point[1] < surface.get_height():
                surface.set_at(point, color)

    @staticmethod
    def midpoint_circle_draw(x_centre, y_centre, r, surface):
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        x = 0
        y = r
        p = 1 - r

        while x <= y:
            MidpointCircleDrawer.draw_symmetric_points(x_centre, y_centre, x, y, surface, color)

            if p < 0:
                p += 2 * x + 3
            else:
                p += 2 * (x - y) + 5
                y -= 1
            x += 1

    def run(self):
        for _ in range(self.N):
            x_centre = random.randint(50, self.width - 50)
            y_centre = random.randint(50, self.height - 50)
            r = random.randint(10, 100)

            start_time = time.time()
            self.midpoint_circle_draw(x_centre, y_centre, r, self.screen)
            self.total_time += time.time() - start_time

            pygame.display.update()

        pygame.image.save(self.screen, "midpoint_circles.png")
        pygame.image.save(self.screen, "static/plot.png")
        
        winsound.MessageBeep()  

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        print(f"Time taken to draw {self.N} circle(s): {self.total_time:.3f} seconds")
        return self.total_time


if __name__ == "__main__":
    drawer = MidpointCircleDrawer(N=5, x0=300, y0=300, r=80)

    drawer.run()
