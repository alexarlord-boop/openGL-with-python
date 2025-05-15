import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

def Cube():
    # Gradient colors for surfaces
    colors = [
        (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
        (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)
    ]
    
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    # Reset color to white
    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_LINES)
    for edge in edges:
        glColor3f(1.0, 1.0, 1.0)
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Navigation
            if event.type == pygame.KEYDOWN:
                # Translation
                if event.key == pygame.K_w:
                    glTranslatef(0, 0, 1.0)
                    print("w")  
                if event.key == pygame.K_s:
                    glTranslatef(0, 0, -1.0)
                    print("s")
                if event.key == pygame.K_a:
                    glTranslatef(1.0, 0, 0)
                    print("a")
                if event.key == pygame.K_d:
                    glTranslatef(-1.0, 0, 0)
                    print("d")
                if event.key == pygame.K_q:
                    glTranslatef(0, 1.0, 0)
                    print("q")
                if event.key == pygame.K_e:
                    glTranslatef(0, -1.0, 0)
                    print("e")
                    print(glGetFloatv(GL_MODELVIEW_MATRIX))
                    
                # Rotation
                if event.key == pygame.K_LEFT:
                    glRotatef(15, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(15, 0, -1, 0)
                if event.key == pygame.K_UP:
                    glRotatef(15, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(15, -1, 0, 0)

        # glRotatef(1, 3, 1, 1)
        glRotatef(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

