import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Initialize PyGame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glClearColor(1.0, 1.0, 1.0, 1.0)  # White background

# Setup perspective
glMatrixMode(GL_PROJECTION)
gluPerspective(45, display[0]/display[1], 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Position the camera
glTranslatef(0.0, 0.0, -10)

def draw_triangle(vertices, colors=None):
    """Draws a triangle with optional per-vertex colors."""
    glBegin(GL_TRIANGLES)
    for i in range(3):
        if colors:
            glColor3fv(colors[i])
        glVertex3fv(vertices[i])
    glEnd()

def get_compound_matrix():
    """Compute the compound transformation matrix."""
    # Translate to origin
    T1 = np.identity(4)
    T1[:3, 3] = [-1.0, -2.0, 0.0]

    # Rotate around Y axis
    theta = math.radians(60)
    R = np.identity(4)
    R[0, 0] = math.cos(theta)
    R[0, 2] = math.sin(theta)
    R[2, 0] = -math.sin(theta)
    R[2, 2] = math.cos(theta)

    # Translate back
    T2 = np.identity(4)
    T2[:3, 3] = [1.0, 2.0, 0.0]

    # Combine transformations: T_back * R * T_origin
    return T2 @ R @ T1

def apply_matrix(matrix):
    """Apply a 4x4 transformation matrix to OpenGL."""
    glMultMatrixf(matrix.T)

# Original red triangle (matching the one from the slides)
red_triangle = [
    [1.0, 3.0, 0.0],
    [0.0, 1.0, 0.0],
    [2.0, 1.0, 0.0]
]

# Green right-angle triangle
green_triangle = [
    [-3.0, -1.0, 0.0],
    [-5.0, -1.0, 0.0],
    [-5.0, 1.0, 0.0]
]

# Equilateral triangle with color blending
blend_triangle = [
    [3.0, 1.0, 0.0],
    [4.5, 3.6, 0.0],
    [6.0, 1.0, 0.0]
]
blend_colors = [
    [1.0, 0.0, 0.0],  # red
    [0.0, 1.0, 0.0],  # green
    [0.0, 0.0, 1.0],  # blue
]

# Main loop
running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10)

    # Draw red triangle with compound transformation
    glPushMatrix()
    compound = get_compound_matrix()
    apply_matrix(compound)
    glColor3f(1.0, 0.0, 0.0)
    draw_triangle(red_triangle)
    glPopMatrix()

    # Draw green right-angled triangle (no transformation)
    glColor3f(0.0, 1.0, 0.0)
    draw_triangle(green_triangle)

    # Draw equilateral triangle with blended color
    draw_triangle(blend_triangle, blend_colors)

    pygame.display.flip()
    pygame.time.wait(10)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
