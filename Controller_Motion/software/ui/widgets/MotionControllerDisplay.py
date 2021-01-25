import PySide6.QtOpenGL

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets
#from PySide6.QtOpenGLFunctions import QOpenGLFunctions_4_3_Core
from PySide6.QtCore import QRect

from OpenGL import GL

class MotionControllerDisplay(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("instantiating MotionControllerDisplay")

        self.context = QtGui.QOpenGLContext()
        print(self.context.format())

        self.draw_params = {
            'marker_size_rel_w' : 0.03,
            'menu_stroke_width_rel_w' : 0.01,
            'channel_top_height_rel' : 0.1
        }
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setBrush(QtCore.Qt.white)
        self.pen_outlines = pen
        self.mouse_pos = (0, 0)

        print(self.geometry())

    def abs2rel(self, x, y):
        return (x / self.width(), y / self.height())
    def rel2abs(self, x, y):
        return (x * self.width(), y * self.height())

    def paintGL(self):
        gl = self.context.functions()
        gl.glClearColor(0, 0.05, 0.1, 1)
        gl.glClear(GL.GL_COLOR_BUFFER_BIT)

        painter = QtGui.QPainter(self)

        painter.setBrush(QtCore.Qt.red)
        ms = self.rel2abs(self.draw_params['marker_size_rel_w'], 0)[0]
        print(ms)
        marker = QRect(self.mouse_pos[0] - ms/2, self.mouse_pos[1] - ms/2, ms, ms)
        painter.drawEllipse(marker)

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(self.pen_outlines)
        size = self.rel2abs(1, self.draw_params['channel_top_height_rel'])
        channel_top = QRect(0, 0, size[0], size[1])
        painter.drawRect(channel_top)

        # painter.setPen(QtCore.Qt.yellow)
        # painter.drawText(10, 50, "HELLO OPENGL")

    def mouseMoveEvent(self, event):
        # rel = self.abs2rel(event.x(), event.y())
        self.mouse_pos = (event.x(), event.y())
        print(self.geometry())
        self.repaint()

    def poti_changed(self, channel, row, value):
        print("channel " + str(channel) + " poti " + str(row) + " value changed: " + str(value))

    def encoder_motion(self, channel, direction):
        print("channel " + str(channel) + " encoder moved in direction: " + str(direction))
    def encoder_pressed(self, channel):
        print("channel " + str(channel) + " encoder pressed ")
    def encoder_released(self, channel):
        print("channel " + str(channel) + " encoder released ")

    def button_pressed(self, channel, row):
        print("channel " + str(channel) + " button " + str(row) + " pressed ")
    def button_released(self, channel, row):
        print("channel " + str(channel) + " button " + str(row) + " released ")
