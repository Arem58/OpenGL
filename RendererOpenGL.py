import pygame
import numpy as np
import glm
from pygame.locals import *
import shaders
from gl import Renderer, Model

width = 940
height = 540

deltaTime = 0.0

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)

face = Model('model.obj', 'model.bmp')
face.position.z = -5

radius =  ((rend.camPosition.x - face.position.x) ** 2 + (rend.camPosition.y - face.position.y) ** 2 + (rend.camPosition.z - face.position.z) ** 2)**0.5
angle = 0
def movCircular(angle):
    x = glm.cos(angle) * radius * deltaTime
    z = glm.sin(angle) * radius * deltaTime
    rend.camPosition.x += x
    rend.camPosition.z += z

rend.scene.append( face )

isRunning = True
while isRunning:

    keys = pygame.key.get_pressed()

    # Traslacion de camara
    if keys[K_d]:
        rend.camPosition.x += 1 * deltaTime
    if keys[K_a]:
        rend.camPosition.x -= 1 * deltaTime
    if keys[K_w]:
        rend.camPosition.z += 1 * deltaTime
    if keys[K_s]:
        rend.camPosition.z -= 1 * deltaTime
    if keys[K_q]:
        rend.camPosition.y -= 1 * deltaTime
    if keys[K_e]:
        rend.camPosition.y += 1 * deltaTime

    # Rotacion de camara
    if keys[K_z]:
        rend.horizontal_rotation(deltaTime)
    if keys[K_x]:
        rend.horizontal_rotation(-deltaTime)
    
    #Zoom de camara
    if keys[K_g]:
        if rend.fov > glm.radians(5):
            rend.fov -= glm.radians(5)
            rend.projectionMatrix = glm.perspective(rend.fov, 
                                                    rend.width / rend.height, 
                                                    0.1, 
                                                    1000) 
    if keys[K_h]:
        if rend.fov <= glm.radians(60):
            rend.fov += glm.radians(5)
            rend.projectionMatrix = glm.perspective(rend.fov, 
                                                    rend.width / rend.height, 
                                                    0.1, 
                                                    1000) 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            if ev.key == K_1:
                rend.filledMode()
            if ev.key == K_2:
                rend.wireframeMode()
    
    #Movimiento del objeto
    #rend.scene[0].rotation.x += 10 * deltaTime
    #rend.scene[0].rotation.y += 10 * deltaTime
    #rend.scene[0].rotation.z += 10 * deltaTime
    
    rend.render()

    clock.tick(60)
    deltaTime = clock.tick(60) / 1000
    pygame.display.flip()

pygame.quit()