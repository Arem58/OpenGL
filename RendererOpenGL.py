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

radius =  ((rend.camPosition.x - face.position.x) ** 2 + (rend.camPosition.y - face.position.y) ** 2 + (rend.camPosition.z - face.position.z) ** 2)**0.5
angle = 0
xtemp = rend.camPosition.x
ytemp = rend.camPosition.y
ztemp = rend.camPosition.z
angleTemp = 0
def circularMov(angle):
    if angle == 0:
        angle = angleTemp
    x = glm.sin(angle) * radius
    z = glm.cos(angle) * radius
    rend.viewMatix = glm.lookAt(glm.vec3(x, ytemp, z), face.position, glm.vec3(0.0, 1.0, 0.0))
    return x, z, angle

rend.scene.append( face )

isRunning = True
while isRunning:

    keys = pygame.key.get_pressed()

    # Traslacion de camara
    if keys[K_w]:
        radius += 1 * deltaTime
        circularMov(0)
    if keys[K_s]:
        radius -= 1 * deltaTime
        circularMov(0)
    if keys[K_q]:
        ytemp -= 1 * deltaTime
        rend.viewMatix = glm.lookAt(glm.vec3(xtemp, ytemp, ztemp), face.position, glm.vec3(0.0, 1.0, 0.0))
    if keys[K_e]:
        ytemp += 1 * deltaTime 
        rend.viewMatix = glm.lookAt(glm.vec3(xtemp, ytemp, ztemp), face.position, glm.vec3(0.0, 1.0, 0.0))

    # Rotacion de camara
    if keys[K_d]:
        angle += deltaTime
        xtemp, ztemp, angleTemp = circularMov(angle)
    if keys[K_a]:
        angle -= deltaTime
        xtemp, ztemp, angleTemp = circularMov(angle)
    
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

    deltaTime = clock.tick(60) / 1000
    pygame.display.flip()

pygame.quit()