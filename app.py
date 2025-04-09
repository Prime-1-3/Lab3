from flask import Flask, render_template, request
import numpy as np
import random
import time
import os
from bres_circle import CircleDrawer
from midpoint import MidpointCircleDrawer
from DDA import DDADrawer
from bres_line import BresenhamDrawer

app = Flask(__name__)

# # ---------------- Algorithms ---------------- #
# def draw_dda(x1, y1, x2, y2):
#     x, y = x1, y1
#     points = [(round(x), round(y))]
#     dx = x2 - x1
#     dy = y2 - y1
#     steps = int(max(abs(dx), abs(dy)))
#     x_inc = dx / steps
#     y_inc = dy / steps
#     for _ in range(steps):
#         x += x_inc
#         y += y_inc
#         points.append((round(x), round(y)))
#     return points

# def draw_bresenham(x1, y1, x2, y2):
#     CircleDrawer().run()
#     points = []
#     dx = abs(x2 - x1)
#     dy = abs(y2 - y1)
#     x, y = x1, y1
#     sx = 1 if x2 > x1 else -1
#     sy = 1 if y2 > y1 else -1
#     if dy <= dx:
#         p = 2 * dy - dx
#         for _ in range(dx):
#             points.append((x, y))
#             x += sx
#             if p < 0:
#                 p += 2 * dy
#             else:
#                 y += sy
#                 p += 2 * (dy - dx)
#     else:
#         p = 2 * dx - dy
#         for _ in range(dy):
#             points.append((x, y))
#             y += sy
#             if p < 0:
#                 p += 2 * dx
#             else:
#                 x += sx
#                 p += 2 * (dx - dy)
#     points.append((x2, y2))
#     return points

# def draw_midpoint_circle(radius, x0, y0):
#     points = []
#     x = 0
#     y = radius
#     p = 1 - radius
#     while x <= y:
#         symmetric_points = [
#             (x + x0, y + y0), (-x + x0, y + y0),
#             (x + x0, -y + y0), (-x + x0, -y + y0),
#             (y + x0, x + y0), (-y + x0, x + y0),
#             (y + x0, -x + y0), (-y + x0, -x + y0)
#         ]
#         points.extend(symmetric_points)
#         x += 1
#         if p < 0:
#             p += 2 * x + 1
#         else:
#             y -= 1
#             p += 2 * (x - y) + 1
#     return points

# ---------------- Transformations ---------------- #
def translate_line(x1, y1, x2, y2):

    tx=random.randint(30, 100)
    ty=random.randint(30, 100)
    return [(x1 + tx, y1 + ty), (x2 + tx, y2 + ty)]

def translate_circle(x0, y0, r):
    tx=random.randint(30, 100)
    ty=random.randint(30, 100)
    return [(x0 + tx, y0 + ty), r]

def rotate(points, angle_deg):
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    return [(round(x * cos_a - y * sin_a), round(x * sin_a + y * cos_a)) for x, y in points]

def reflect_x(points):
    return [(x, -y) for x, y in points]

def reflect_y(points):
    return [(-x, y) for x, y in points]



# ---------------- Routes ---------------- #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    shape = request.form['shape']
    algorithm = request.form['algorithm']
    transformation = request.form['transformation']
    N= abs(int(request.form['number']))
    
    if transformation != 'None':
        N=1




    if shape == 'line':
        x1, y1 = random.randint(0, 600-1), random.randint(0, 600-1)
        x2, y2 = random.randint(x1, 600-1), random.randint(y1, 600-1)
    
        if algorithm == 'DDA':
            runtime= DDADrawer(x1=x1, y1=y1, x2=x2, y2=y2,N=N).run()
        elif algorithm == 'Bresenham':
            runtime= BresenhamDrawer(x1=x1, y1=y1, x2=x2, y2=y2,N=N).run()
       
    else:
        x0 = random.randint(50, 600 - 50)
        y0 = random.randint(50, 600 - 50)
        r = random.randint(10, 50)
        if algorithm == 'Midpoint':
            runtime= MidpointCircleDrawer(x0=x0,y0=y0,r=r,N=N).run()
        else:
            runtime=CircleDrawer(x0=x0,y0=y0,r=r,N=N).run()
            


    # Apply Transformation
        if transformation == 'Translation':
            if shape == 'line':
                translate_line(x1, y1, x2, y2)
            else:
                translate_circle(x0, y0, r)
        elif transformation == 'Rotation':
            after_points = rotate(before_points, 45)
        elif transformation == 'ReflectionX':
            after_points = reflect_x(before_points)
        elif transformation == 'ReflectionY':
            after_points = reflect_y(before_points)
    
 

    return render_template('result.html', img_path='static/plot.png', runtime=runtime)

# ---------------- Run ---------------- #
if __name__ == '__main__':
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
