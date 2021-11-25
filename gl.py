import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Model(object):
    def __init__(self, verts, indices):

        self.createVertexBuffer(verts, indices)

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

    def getModelMatrix(self):
        identity = glm.mat4(1)
        translateMatrix = glm.translate(identity, self.position)
        Pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        Yaw   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        Roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMatrix = Pitch * Yaw * Roll
        scaleMatrix = glm.scale(identity, self.scale)
        return translateMatrix * rotationMatrix * scaleMatrix

    def createVertexBuffer(self, verts, indices):
        self.vertBuffer = verts
        self.indexBuffer = indices
        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object
        self.EAO = glGenBuffers(1) #Element Array Object

    def renderInScene(self):
        
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EAO)

        glBufferData(GL_ARRAY_BUFFER, #Buffer ID
                     self.vertBuffer.nbytes, #Buffer size in bytes
                     self.vertBuffer, #Buffer data
                     GL_STATIC_DRAW) #Usage

        glBufferData(GL_ELEMENT_ARRAY_BUFFER, #Buffer ID
                     self.indexBuffer.nbytes, #Buffer size in bytes
                     self.indexBuffer, #Buffer data
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

        glDrawElements(GL_TRIANGLES, len(self.indexBuffer), GL_UNSIGNED_INT, None)

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.scene = []

        # Viww Matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0) # pitch, yaw, roll

        # ViewportMatrix * projectionMatrix * viewMatrix * modelMatrix * pos

        #Projection Matrix
        self.projectionMatrix = glm.perspective(glm.radians(60), # FOV en radianes
                                                self.width / self.height, # Aspect Ratio
                                                0.1, #Neas Plane distance
                                                1000) #Far plane distance

    def getViewMatrix(self):
        identity = glm.mat4(1)
        translateMatrix = glm.translate(identity, self.camPosition)
        Pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        Yaw   = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0))
        Roll  = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1))

        rotationMatrix = Pitch * Yaw * Roll
        camMatrix = translateMatrix * rotationMatrix
        return glm.inverse(camMatrix)

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))
                                                                    
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

        for model in self.scene:
            if self.active_shader:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "modelMatrix"),
                                1, GL_FALSE, glm.value_ptr(model.getModelMatrix()))
            model.renderInScene()