'''
Dudley Sorensen
January 28, 2026
Project 3: Turtle Graphics Scene Refactoring Assignment

Improvements made:
- Broke the large draw_scene function into smaller, single-purpose helper functions
  (ground, tree, house, moon, stars).
- Removed redundancy by generalizing repeated patterns (tree foliage, windows, stars).
- Improved readability and organization by grouping related logic and adding clear comments.
- Demonstrated reusability by adding an enhanced scene with multiple trees.
'''

import turtle
import math
import random


def setup_turtle():
    """Initialize turtle with standard settings"""
    t = turtle.Turtle()
    t.speed(1000)
    screen = turtle.Screen()
    screen.title("Turtle Graphics Assignment")
    return t, screen


# ---------- Basic Drawing Utilities (unchanged) ----------

def draw_rectangle(t, width, height, fill_color=None):
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    if fill_color:
        t.end_fill()


def draw_triangle(t, size, fill_color=None):
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    for _ in range(3):
        t.forward(size)
        t.left(120)
    if fill_color:
        t.end_fill()


def draw_circle(t, radius, fill_color=None):
    if fill_color:
        t.fillcolor(fill_color)
        t.begin_fill()
    t.circle(radius)
    if fill_color:
        t.end_fill()


def jump_to(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()


# ---------- Refactored Composite Drawing Functions ----------

def draw_ground(t):
    jump_to(t, -400, -250)
    draw_rectangle(t, 800, 200, "darkgreen")


def draw_tree(t, x, y):
    # Trunk
    jump_to(t, x, y)
    draw_rectangle(t, 30, 80, "brown")

    # Foliage
    foliage_sizes = [90, 80, 70, 60, 50, 40, 30]
    current_y = y
    for size in foliage_sizes:
        jump_to(t, x - (size - 30) // 2, current_y)
        draw_triangle(t, size, "forestgreen")
        current_y += size - 20


def draw_house(t, x, y):
    # Base
    jump_to(t, x, y)
    draw_rectangle(t, 180, 100, "red")

    # Roof
    jump_to(t, x - 20, y)
    draw_triangle(t, 220, "darkgrey")

    # Door
    jump_to(t, x + 120, y - 40)
    draw_rectangle(t, 40, 60, "saddlebrown")

    # Door knob
    jump_to(t, x + 150, y - 80)
    draw_circle(t, 5, "gold")

    # Window
    draw_window(t, x + 30, y - 30)


def draw_window(t, x, y):
    jump_to(t, x, y)
    draw_rectangle(t, 40, 40, "lightblue")

    jump_to(t, x + 18, y)
    draw_rectangle(t, 5, 40, "white")

    jump_to(t, x, y - 20)
    draw_rectangle(t, 40, 5, "white")


def draw_moon(t, x, y):
    jump_to(t, x, y)
    draw_circle(t, 50, "lightgrey")

    crater_positions = [
        (x + 20, y + 60),
        (x - 20, y + 10),
        (x - 10, y + 30),
        (x + 30, y + 20),
        (x - 10, y + 70),
    ]

    for cx, cy in crater_positions:
        jump_to(t, cx, cy)
        draw_circle(t, 7, "grey")


def draw_stars(t, count, moon_info):
    moon_x, moon_y, moon_radius = moon_info
    buffer = 30

    for _ in range(count):
        while True:
            x = random.randint(-350, 350)
            y = random.randint(100, 300)
            if not (
                moon_x - moon_radius - buffer < x < moon_x + moon_radius + buffer and
                moon_y - moon_radius - buffer < y < moon_y + moon_radius + buffer
            ):
                break

        jump_to(t, x, y)
        t.color("white")
        t.begin_fill()
        for _ in range(5):
            t.forward(10)
            t.right(144)
        t.end_fill()


# ---------- Scene Assembly ----------

def draw_scene(t):
    screen = t.getscreen()
    screen.bgcolor("darkblue")

    # Original Project 2 Scene (unchanged layout)
    draw_ground(t)
    draw_tree(t, -300, -200)
    draw_house(t, -60, -150)
    draw_moon(t, 230, 180)
    draw_stars(t, 30, (230, 230, 50))

    # Enhanced Scene Element (demonstrates reusability)
    draw_tree(t, -200, -200)
    draw_tree(t, 200, -200)

    t.hideturtle()


def main():
    t, screen = setup_turtle()
    draw_scene(t)
    screen.mainloop()


if __name__ == "__main__":
    main()