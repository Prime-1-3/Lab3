from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from bres_circle import CircleDrawer

app = Flask(__name__)

# ---------------- Algorithms ---------------- #
def draw_dda(x1, y1, x2, y2):
    x, y = x1, y1
    points = [(round(x), round(y))]
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    for _ in range(steps):
        x += x_inc
        y += y_inc
        points.append((round(x), round(y)))
    return points

def draw_bresenham(x1, y1, x2, y2):
    CircleDrawer().run()
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    if dy <= dx:
        p = 2 * dy - dx
        for _ in range(dx):
            points.append((x, y))
            x += sx
            if p < 0:
                p += 2 * dy
            else:
                y += sy
                p += 2 * (dy - dx)
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            points.append((x, y))
            y += sy
            if p < 0:
                p += 2 * dx
            else:
                x += sx
                p += 2 * (dx - dy)
    points.append((x2, y2))
    return points

def draw_midpoint_circle(radius, xc, yc):
    points = []
    x = 0
    y = radius
    p = 1 - radius
    while x <= y:
        symmetric_points = [
            (x + xc, y + yc), (-x + xc, y + yc),
            (x + xc, -y + yc), (-x + xc, -y + yc),
            (y + xc, x + yc), (-y + xc, x + yc),
            (y + xc, -x + yc), (-y + xc, -x + yc)
        ]
        points.extend(symmetric_points)
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
    return points

# ---------------- Transformations ---------------- #
def translate(points, tx, ty):
    return [(x + tx, y + ty) for x, y in points]

def rotate(points, angle_deg):
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    return [(round(x * cos_a - y * sin_a), round(x * sin_a + y * cos_a)) for x, y in points]

def reflect_x(points):
    return [(x, -y) for x, y in points]

def reflect_y(points):
    return [(-x, y) for x, y in points]

# ---------------- Plot ---------------- #
def plot(points_before, points_after):
    plt.figure(figsize=(6, 6))
    if points_before:
        x1, y1 = zip(*points_before)
        plt.plot(x1, y1, 'bo-', label='Before')
    if points_after:
        x2, y2 = zip(*points_after)
        plt.plot(x2, y2, 'ro-', label='After')
    plt.axhline(0, color='gray')
    plt.axvline(0, color='gray')
    plt.grid(True)
    plt.legend()
    plt.title("Before and After Transformation")
    plt.savefig('static/plot.png')
    plt.close()

# ---------------- Routes ---------------- #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    shape = request.form['shape']
    algorithm = request.form['algorithm']
    transformation = request.form['transformation']

    before_points = []
    after_points = []

    start_time = time.time()

    if shape == 'line':
        x1, y1, x2, y2 = 10, 10, 100, 50
        if algorithm == 'DDA':
            before_points = draw_dda(x1, y1, x2, y2)
        elif algorithm == 'Bresenham':
            before_points = draw_bresenham(x1, y1, x2, y2)
        else:
            before_points = draw_dda(x1, y1, x2, y2)  # fallback
    else:
        r = 40
        xc, yc = 50, 50
        if algorithm == 'Midpoint':
            before_points = draw_midpoint_circle(r, xc, yc)
        else:
            before_points = draw_midpoint_circle(r, xc, yc)  # fallback

    # Apply Transformation
    if transformation == 'Translation':
        after_points = translate(before_points, 50, 30)
    elif transformation == 'Rotation':
        after_points = rotate(before_points, 45)
    elif transformation == 'ReflectionX':
        after_points = reflect_x(before_points)
    elif transformation == 'ReflectionY':
        after_points = reflect_y(before_points)

    end_time = time.time()
    runtime = round(end_time - start_time, 4)

    plot(before_points, after_points)

    return render_template('result.html', img_path='static/plot.png', runtime=runtime)

# ---------------- Run ---------------- #
if __name__ == '__main__':
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
