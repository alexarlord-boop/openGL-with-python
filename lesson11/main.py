import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time
from PIL import Image

# Load texture from file
def load_texture(path):
    texture_surface = Image.open(path)
    texture_data = texture_surface.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
    width, height = texture_surface.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

# Draw a textured sphere
def draw_planet(radius, texture_id, self_rotation_angle=0):
    # glBindTexture(GL_TEXTURE_2D, texture_id)
    # quad = gluNewQuadric()
    # gluQuadricTexture(quad, GL_TRUE)
    # gluSphere(quad, radius, 36, 18)
    # gluDeleteQuadric(quad)
    glPushMatrix()

     # Apply self-rotation around Y-axis (planet's own axis)
    glRotatef(self_rotation_angle, 0, 1, 0)

    glRotatef(-90, 1, 0, 0)  # Align texture poles vertically
    glBindTexture(GL_TEXTURE_2D, texture_id)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, 50, 50)
    gluDeleteQuadric(quad)
    glPopMatrix()

# Setup lighting
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR,  (1.0, 1.0, 1.0, 1.0))

# Initialize OpenGL context
def init():
    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    setup_lighting()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Load textures for each planet
def load_textures():
    return {
        "sun":   load_texture("textures/sunmap.jpg"),
        "earth": load_texture("textures/earthmap.jpg"),
        "mars":  load_texture("textures/marsmap.jpg"),
    }

def main():
    init()
    textures = load_textures()

    clock = pygame.time.Clock()
    start_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 8, 25, 0, 0, 0, 0, 1, 0)

        elapsed = time.time() - start_time

        # Draw Sun at the origin
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(1, 1, 0)
        draw_planet(2.5, textures["sun"], self_rotation_angle=(elapsed * 5) % 360)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        # Draw Earth orbiting the Sun
        glPushMatrix()
        angle = (elapsed * 20) % 360
        self_rot_angle = (elapsed * 80) % 360  # faster self-rotation
        glRotatef(angle, 0, 1, 0)
        glTranslatef(8, 0, 0)
        draw_planet(1, textures["earth"], self_rotation_angle=self_rot_angle)
        glPopMatrix()

        # Draw Mars orbiting further
        glPushMatrix()
        angle_mars = (elapsed * 10) % 360
        self_rot_angle_mars = (elapsed * 60) % 360
        glRotatef(angle_mars, 0, 1, 0)
        glTranslatef(12, 0, 0)
        draw_planet(0.8, textures["mars"], self_rotation_angle=self_rot_angle_mars)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
