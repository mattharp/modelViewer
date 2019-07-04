import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import glm
import trackball
from objLoader import *


class Viewer():
    def __init__(self, obj):
        self.initWindow()
        self.initGL()
        self.initView()
        self.obj = OBJ(obj, True)
        self.inputs = Input()

    def initWindow(self):
        glutInit()
        glutInitWindowSize(800,600)
        glutCreateWindow("MODEL VIEW")
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutDisplayFunc(self.render)

    def initGL(self):
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # set up lighting
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)

        glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 1, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glClearColor(0, 0, 0, 1)

    def initView(self):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        aspect_ratio = float(xSize) / float(ySize)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()    

        glViewport(0, 0, xSize, ySize)
        gluPerspective(70, aspect_ratio, 0.1, 4000.0)
        
        glTranslated(0, 0, -15)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        loc = self.inputs.translation
        glTranslated(loc[0], loc[1], loc[2])
        glMultMatrixf(self.inputs.trackball.matrix)

        # execute display list
        glCallList(self.obj.glList)

        glPopMatrix()
        glutSwapBuffers()

    def main(self):
        glutMainLoop()


class Input():
    def __init__(self):
        self.pressed = None
        self.translation = [0, 0, 0, 0]
        self.trackball = trackball.Trackball(theta = -25, distance=15)
        self.mouseLocation = None

        glutMouseFunc(self.mouseButtonEvent)
        glutMotionFunc(self.mouseMoveEvent)

    def translate(self, x, y, z):
        self.translation[0] += x
        self.translation[1] += y
        self.translation[2] += z

    def mouseButtonEvent(self, button, mode, x, y):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        # invert the y coordinate because OpenGL is inverted
        y = ySize - y  
        self.mouseLocation = (x, y)

        if mode == GLUT_DOWN:
            self.pressed = button
            if button == GLUT_RIGHT_BUTTON:
                pass
            elif button == GLUT_LEFT_BUTTON:
                pass
            # mouse wheel up:
            elif button == 3:
                self.translate(0, 0, 1.0)
            # mouse wheel down:
            elif button == 4:
                self.translate(0, 0, -1.0)
        else:
            self.pressed = None
        glutPostRedisplay()

    def mouseMoveEvent(self, x, screenY):
        xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
        # invert the y coordinate because OpenGL is inverted
        y = ySize - screenY  
        if self.pressed is not None:
            dx = x - self.mouseLocation[0]
            dy = y - self.mouseLocation[1]
            if self.pressed == GLUT_RIGHT_BUTTON and self.trackball is not None:
                self.trackball.drag_to(self.mouseLocation[0], self.mouseLocation[1], dx, dy)
            elif self.pressed == GLUT_MIDDLE_BUTTON:
                self.translate(dx/60.0, dy/60.0, 0)
            
            glutPostRedisplay()
        self.mouseLocation = (x, y)


if __name__ == "__main__":
    viewer = Viewer(sys.argv[1])
    viewer.main()


