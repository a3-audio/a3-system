import PySide6.QtOpenGL

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets
#from PySide6.QtOpenGLFunctions import QOpenGLFunctions_4_3_Core
from PySide6.QtCore import QObject, QThread, Signal, Slot, QRect
from PySide6.QtGui import QColor, QFont, QImage

from Track import PlaybackParameters

from OpenGL import GL

class MotionControllerDisplay(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.context = QtGui.QOpenGLContext()
        print(self.context.format())

        self.draw_params = {
            'marker_size_rel_w' : 0.03,
            'menu_stroke_width_rel_w' : 0.01,
            'channel_top_height_rel' : 0.07,
            'channel_bottom_height_rel' : 0.1,
            'text_pad_rel_w' : 0.02,
            'text_pad_rel_h' : 0.012,
            'font_scale' : 0.015,
            'line_spacing_rel_h' : 0.028
        }

        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setBrush(QtCore.Qt.white)
        self.pen_outlines = pen
        self.mouse_pos = (0, 0)

        self.image_orientation = QImage("resources/orientation.png")

        self.tracks = None

    def setTracks(self, tracks):
        self.tracks = tracks

    def abs_to_rel(self, x, y):
        return (x / self.width(), y / self.height())
    def rel_to_abs(self, x, y):
        return (x * self.width(), y * self.height())
    def rel_to_abs_width(self, x):
        return x * self.width()
    def rel_to_abs_height(self, y):
        return y * self.height()

    def paintGL(self):
        gl = self.context.functions()
        gl.glClearColor(0, 0.05, 0.1, 1)
        gl.glClear(GL.GL_COLOR_BUFFER_BIT)

        self.draw_params_dynamic = {
            'left_pad' : self.rel_to_abs_width(self.draw_params['text_pad_rel_w']),
            'top_pad' : self.rel_to_abs_height(self.draw_params['text_pad_rel_h']),
            'line_spacing' : self.rel_to_abs_height(self.draw_params['line_spacing_rel_h']),
            'header_height' : self.rel_to_abs_height(self.draw_params['channel_top_height_rel']),
            'footer_height' : self.rel_to_abs_height(self.draw_params['channel_bottom_height_rel']),
        }

        painter = QtGui.QPainter(self)
        painter.setFont(QtGui.QFont('monospace', self.height() * self.draw_params['font_scale']))

        painter.setBrush(QtCore.Qt.red)
        ms = self.rel_to_abs_width(self.draw_params['marker_size_rel_w'])

        if self.tracks:
            num_tracks = len(self.tracks)
            for t in range(num_tracks):
                track_width = self.width() / num_tracks
                region = QRect(t*track_width, 0, track_width, self.height())
                color = QColor()
                color.setHsl(int(255/num_tracks*t), 100, 150)

                header_region = QRect(region)
                header_region.setHeight(self.draw_params_dynamic['header_height'])
                self.drawTrackHeader(painter, self.tracks[t], header_region, color)

                footer_region = QRect(region)
                footer_region.setBottom(self.height())
                footer_region.setTop(self.height() - self.draw_params_dynamic['footer_height'])
                self.drawTrackFooter(painter, self.tracks[t], footer_region, color)

    def drawTrackHeader(self, painter, track, region, color):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        text_region = QRect(region)
        text_region.adjust(self.draw_params_dynamic['left_pad'],
                           self.draw_params_dynamic['top_pad'], 0, 0)

        painter.setPen(QtCore.Qt.black)
        width_string = f'Width: {track.ambi_params.width:.0f}°'
        painter.drawText(text_region, width_string)

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        side_string = f'Side: {track.ambi_params.side:.1f}dB'
        painter.drawText(text_region, side_string)

    def drawTrackFooter(self, painter, track, region, color):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        text_region = QRect(region)
        text_region.adjust(self.draw_params_dynamic['left_pad'],
                           self.draw_params_dynamic['top_pad'], 0, 0)

        painter.setPen(QtCore.Qt.black)
        ambi_mode_string = track.ambi_params.mode.name
        painter.drawText(text_region, "Mode: " + ambi_mode_string)

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        painter.drawText(text_region, "Length: " + str(track.playback_params.length))

        text_region.adjust(0, self.draw_params_dynamic['line_spacing'], 0, 0)
        playback_mode_string = track.playback_params.mode.name
        painter.drawText(text_region, "Loop: " + playback_mode_string)

    def mouseMoveEvent(self, event):
        # rel = self.abs2rel(event.x(), event.y())
        self.mouse_pos = (event.x(), event.y())
        self.repaint()

    @Slot(int, int, float)
    def poti_changed(self, track, row, value):
        print("track " + str(track) + " poti " + str(row) + " value changed: " + str(value))
        if row == 0:
            self.tracks[track].ambi_params.width = value*180
        if row == 1:
            self.tracks[track].ambi_params.side = value*9

        self.repaint()

    @Slot(int, int)
    def encoder_motion(self, channel, direction):
        print("channel " + str(channel) + " encoder moved in direction: " + str(direction))
    @Slot(int)
    def encoder_pressed(self, channel):
        print("channel " + str(channel) + " encoder pressed ")
    @Slot(int)
    def encoder_released(self, channel):
        print("channel " + str(channel) + " encoder released ")

    @Slot(int, int)
    def button_pressed(self, channel, row):
        print("channel " + str(channel) + " button " + str(row) + " pressed ")
    @Slot(int, int)
    def button_released(self, channel, row):
        print("channel " + str(channel) + " button " + str(row) + " released ")
