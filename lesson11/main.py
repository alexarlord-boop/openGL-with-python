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
# def setup_lighting():
#     glEnable(GL_LIGHTING)
#     glEnable(GL_LIGHT0)
#     glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 0, 1))
#     glLightfv(GL_LIGHT0, GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
#     glLightfv(GL_LIGHT0, GL_SPECULAR,  (1.0, 1.0, 1.0, 1.0))
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # Light positioned at the origin (Sun's position)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR,  (1.0, 1.0, 1.0, 1.0))
    # Optional: set ambient light low or zero to make Sun the sole source
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.05, 0.05, 0.05, 1))

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

# def main():
#     init()
#     textures = load_textures()

#     clock = pygame.time.Clock()
#     start_time = time.time()

#     while True:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 return

#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glLoadIdentity()
#         gluLookAt(0, 8, 25, 0, 0, 0, 0, 1, 0)

#         elapsed = time.time() - start_time

#         # Draw Sun at the origin
#         glPushMatrix()
#         glDisable(GL_LIGHTING)
#         glColor3f(1, 1, 0)
#         draw_planet(2.5, textures["sun"], self_rotation_angle=(elapsed * 5) % 360)
#         glEnable(GL_LIGHTING)
#         glPopMatrix()

#         # Draw Earth orbiting the Sun
#         glPushMatrix()
#         angle = (elapsed * 20) % 360
#         self_rot_angle = (elapsed * 80) % 360  # faster self-rotation
#         glRotatef(angle, 0, 1, 0)
#         glTranslatef(8, 0, 0)
#         draw_planet(1, textures["earth"], self_rotation_angle=self_rot_angle)
#         glPopMatrix()

#         # Draw Mars orbiting further
#         glPushMatrix()
#         angle_mars = (elapsed * 10) % 360
#         self_rot_angle_mars = (elapsed * 60) % 360
#         glRotatef(angle_mars, 0, 1, 0)
#         glTranslatef(12, 0, 0)
#         draw_planet(0.8, textures["mars"], self_rotation_angle=self_rot_angle_mars)
#         glPopMatrix()

#         pygame.display.flip()
#         clock.tick(60)

def main():
    init()
    
    zoom_distance = 70  # initial camera zoom


    textures = {
        "sun": load_texture("textures/sunmap.jpg"),
        "mercury": load_texture("textures/mercurymap.jpg"),
        "venus": load_texture("textures/venusmap.jpg"),
        "earth": load_texture("textures/earthmap.jpg"),
        "mars": load_texture("textures/marsmap.jpg"),
        "jupiter": load_texture("textures/jupitermap.jpg"),
        "saturn": load_texture("textures/saturnmap.jpg"),
        "uranus": load_texture("textures/uranusmap.jpg"),
        "neptune": load_texture("textures/neptunemap.jpg"),
    }

    # planets = [
    #     {"name": "mercury", "radius": 0.3, "distance": 4,  "orbit_speed": 47.4, "spin_speed": 10},
    #     {"name": "venus",   "radius": 0.6, "distance": 5.5,"orbit_speed": 35.0, "spin_speed": -6},
    #     {"name": "earth",   "radius": 1.0, "distance": 8,  "orbit_speed": 29.8, "spin_speed": 80},
    #     {"name": "mars",    "radius": 0.8, "distance": 10, "orbit_speed": 24.1, "spin_speed": 60},
    #     {"name": "jupiter", "radius": 1.8, "distance": 13, "orbit_speed": 13.1, "spin_speed": 100},
    #     {"name": "saturn",  "radius": 1.6, "distance": 16, "orbit_speed": 9.7,  "spin_speed": 80},
    #     {"name": "uranus",  "radius": 1.2, "distance": 19, "orbit_speed": 6.8,  "spin_speed": -70},
    #     {"name": "neptune", "radius": 1.2, "distance": 22, "orbit_speed": 5.4,  "spin_speed": 60},
    # ]

    planets = [
        {"name": "mercury", "radius": 0.2, "distance": 10, "orbit_speed": 47.4, "spin_speed": 10},
        {"name": "venus",   "radius": 0.5, "distance": 13, "orbit_speed": 35.0, "spin_speed": -6},
        {"name": "earth",   "radius": 0.6, "distance": 16, "orbit_speed": 29.8, "spin_speed": 80},
        {"name": "mars",    "radius": 0.4, "distance": 20, "orbit_speed": 24.1, "spin_speed": 60},
        {"name": "jupiter", "radius": 1.2, "distance": 28, "orbit_speed": 13.1, "spin_speed": 100},
        {"name": "saturn",  "radius": 1.0, "distance": 34, "orbit_speed": 9.7,  "spin_speed": 80},
        {"name": "uranus",  "radius": 0.8, "distance": 38, "orbit_speed": 6.8,  "spin_speed": -70},
        {"name": "neptune", "radius": 0.8, "distance": 42, "orbit_speed": 5.4,  "spin_speed": 60},
    ]

    clock = pygame.time.Clock()
    start_time = time.time()

    while True:
        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         pygame.quit()
        #         return
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEWHEEL:
                zoom_distance -= event.y * 2  # scroll up = zoom in, down = zoom out
                zoom_distance = max(10, min(200, zoom_distance))  # clamp zoom

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # gluLookAt(0, 8, 35, 0, 0, 0, 0, 1, 0)
        gluLookAt(0, 15, zoom_distance, 0, 0, 0, 0, 1, 0)

        # Set up lighting, fixing camera-source lightning
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 0.0, 1.0))  # Sun at origin


        elapsed = time.time() - start_time

        # Draw Sun
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(1, 1, 0)
        # draw_planet(2.5, textures["sun"], self_rotation_angle=(elapsed * 5) % 360)
        draw_planet(7.0, textures["sun"], self_rotation_angle=(elapsed * 2) % 360)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        # Draw each planet orbiting and rotating
        for p in planets:
            glPushMatrix()
            orbit_angle = (elapsed * p["orbit_speed"]) % 360
            spin_angle = (elapsed * p["spin_speed"]) % 360
            glRotatef(orbit_angle, 0, 1, 0)
            glTranslatef(p["distance"], 0, 0)
            draw_planet(p["radius"], textures[p["name"]], self_rotation_angle=spin_angle)
            glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
