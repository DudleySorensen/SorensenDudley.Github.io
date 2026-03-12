'''
Dudley Sorensen
January 19, 2026
Project 2: Turtle Graphics (using function calls) Assignment

This scene shows a nighttime landscape with a house, a moon,
and stars in the sky above grassy ground.
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


# ALL drawing must be inside this function
def draw_scene(t):
    screen = t.getscreen()
    screen.bgcolor("darkblue")

    # Ground
    jump_to(t, -400, -250)
    draw_rectangle(t, 800, 200, "darkgreen")

    # Draw tree trunk
    jump_to(t, -300, -200)
    draw_rectangle(t, 30, 80, "brown")

    # Draw tree foliage (stacked triangles)
    foliage_sizes = [90, 80, 70, 60, 50, 40, 30]  # sizes for triangles
    start_y = -200  # starting y position for foliage

    for size in foliage_sizes:
        jump_to(t, -300 - (size - 30)//2, start_y)  # center triangles above trunk
        draw_triangle(t, size, "forestgreen")
        start_y += size - 20  # move up for next triangle

    # House base
    jump_to(t, -60, -150)
    draw_rectangle(t, 180, 100, "red")

    # Roof
    jump_to(t, -80, -150)
    draw_triangle(t, 220, "darkgrey")

    # Door
    jump_to(t, 60, -190)
    draw_rectangle(t, 40, 60, "saddlebrown")

    # Door knob
    jump_to(t, 90, -230)
    draw_circle(t, 5, "gold")

    # Window
    jump_to(t, -30, -180)
    draw_rectangle(t, 40, 40, "lightblue")

    # Vertical pane
    jump_to(t, -12, -180)
    draw_rectangle(t, 5, 40, "white")

    # Horizontal pane
    jump_to(t, -30, -200)
    draw_rectangle(t, 40, 5, "white")

    # Moon
    # Moon outline
    jump_to(t, 230, 180)
    draw_circle(t, 50, "lightgrey")

    # Moon craters
    crater_positions = [(250, 240), (210, 190), (220, 210), (260, 200), (220, 250)]
    for x, y in crater_positions:
        jump_to(t, x, y)
        draw_circle(t, 7, "grey")

    # Stars (avoid moon area)
    moon_x, moon_y, moon_radius = 230, 230, 50
    buffer = 30

    for _ in range(30):
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

    t.hideturtle()


def main():
    t, screen = setup_turtle()
    draw_scene(t)
    screen.mainloop()


if __name__ == "__main__":
    main()