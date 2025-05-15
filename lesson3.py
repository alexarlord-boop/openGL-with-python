import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def initializeGL():
    # Set "clearing" or background color
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black and opaque


def display_init():
    glClear(GL_COLOR_BUFFER_BIT);   

  
    glBegin(GL_TRIANGLES);         
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 0.0);     
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.5, 0.0)      
    glColor3f(0.0, 1.0, 0.0) 
    glVertex2f(0.0, 0.5);     
    glEnd()

    glFlush(); 

def display_right():
    # glClear(GL_COLOR_BUFFER_BIT)  # Clear the color buffer with current clearing color

    # Draw an equilateral triangle
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex2f(-0.5, -0.289)  # Bottom left vertex
    glColor3f(1.0, 0.0, 0.0)  # Red 
    glVertex2f(0.5, -0.289)   # Bottom right vertex
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex2f(0.0, 0.577)    # Top vertex
    glEnd()

    glFlush()  # Render now 


def main():
    pygame.init()
    screen_size = (320, 320)
    pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Triangle")

    initializeGL()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # display_init()
        display_right()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
