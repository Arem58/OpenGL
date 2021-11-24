import glm
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Model(object):
    def __init__(self, verts):

        self.createVertexBuffer(verts)

    def createVertexBuffer(self, verts):
        self.vertBuffer = verts
        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object

    def renderInScene(self):
        
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        glBufferData(GL_ARRAY_BUFFER, #Buffer ID
                     self.vertBuffer.nbytes, #Buffer size in bytes
                     self.vertBuffer, #Buffer data
                     GL_STATIC_DRAW) #Usage

        #Atributos de posicion
        glVertexAttribPointer(0, #Attibute number
                              3, # Size
                              GL_FLOAT, #Type
                              GL_FALSE, # It is normalized?
                              4 * 6, # Stride
                              ctypes.c_void_p(0)) #Offset

        glEnableVertexAttribArray(0)

        #Atributos de color
        glVertexAttribPointer(1, #Attibute number
                              3, # Size
                              GL_FLOAT, #Type
                              GL_FALSE, # It is normalized?
                              4 * 6, # Stride
                              ctypes.c_void_p(4 * 3)) #Offset

        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, 3)

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.scene = []

    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None and fragShader is not None:
            self.active_shader = compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                                 compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

    def render(self):
        glClearColor(0.2,0.2,0.2,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.active_shader)

        for model in self.scene:
            model.renderInScene()