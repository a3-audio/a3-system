import PySide6.QtOpenGL

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGLWidgets
#from PySide6.QtOpenGLFunctions import QOpenGLFunctions_4_3_Core
from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QFont

from Track import PlaybackParameters

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

        self.tracks = None

    def setTracks(self, tracks):
        self.tracks = tracks
        print("got " + str(len(tracks)) + " tracks")

    def abs2rel(self, x, y):
        return (x / self.width(), y / self.height())
    def rel2abs(self, x, y):
        return (x * self.width(), y * self.height())

    def paintGL(self):
        gl = self.context.functions()
        gl.glClearColor(0, 0.05, 0.1, 1)
        gl.glClear(GL.GL_COLOR_BUFFER_BIT)

        painter = QtGui.QPainter(self)
        painter.setFont(QtGui.QFont('monospace', self.height() * self.draw_params['font_scale']))

        painter.setBrush(QtCore.Qt.red)
        ms = self.rel2abs(self.draw_params['marker_size_rel_w'], 0)[0]
        print(ms)

        if self.tracks:
            num_tracks = len(self.tracks)
            for t in range(num_tracks):
                track_width = self.width() / num_tracks
                region = QRect(t*track_width, 0, track_width, self.height())
                color = QColor()
                color.setHsl(int(255/num_tracks*t), 100, 150)
                self.drawTrackIntoRegion(painter, self.tracks[t], region, color)

        # marker = QRect(self.mouse_pos[0] - ms/2, self.mouse_pos[1] - ms/2, ms, ms)
        # painter.drawEllipse(marker)

        # painter.setBrush(QtCore.Qt.NoBrush)
        # painter.setPen(self.pen_outlines)
        # size = self.rel2abs(1, self.draw_params['channel_top_height_rel'])
        # channel_top = QRect(0, 0, size[0], size[1])
        # painter.drawRect(channel_top)

        # painter.setPen(QtCore.Qt.yellow)

    def drawTrackIntoRegion(self, painter, track, region, color):
        header_region = region
        header_region.setHeight(self.rel2abs(0, self.draw_params['channel_top_height_rel'])[1])
        self.drawTrackHeader(painter, track, header_region, color)

        footer_size = self.rel2abs(0, self.draw_params['channel_bottom_height_rel'])[1]
        footer_region = region
        footer_region.setBottom(self.height())
        footer_region.setTop(self.height() - footer_size)
        self.drawTrackFooter(painter, track, footer_region, color)

    def drawTrackHeader(self, painter, track, region, color):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        text_region = QRect(region)
        left_pad = self.rel2abs(self.draw_params['text_pad_rel_w'], 0)[0]
        top_pad = self.rel2abs(0, self.draw_params['text_pad_rel_h'])[1]
        line_spacing = self.rel2abs(0, self.draw_params['line_spacing_rel_h'])[1]
        text_region.adjust(left_pad, top_pad, 0, 0)

        painter.setPen(QtCore.Qt.black)
        width_string = f'Width: {track.ambi_params.width:.0f}°'
        painter.drawText(text_region, width_string)

        text_region.adjust(0, line_spacing, 0, 0)
        side_string = f'Side: {track.ambi_params.side:.1f}dB'
        painter.drawText(text_region, side_string)

    def drawTrackFooter(self, painter, track, region, color):
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(region)

        text_region = QRect(region)
        left_pad = self.rel2abs(self.draw_params['text_pad_rel_w'], 0)[0]
        top_pad = self.rel2abs(0, self.draw_params['text_pad_rel_h'])[1]
        line_spacing = self.rel2abs(0, self.draw_params['line_spacing_rel_h'])[1]
        text_region.adjust(left_pad, top_pad, 0, 0)

        painter.setPen(QtCore.Qt.black)
        ambi_mode_string = track.ambi_params.mode.name
        painter.drawText(text_region, "Mode: " + ambi_mode_string)

        text_region.adjust(0, line_spacing, 0, 0)
        painter.drawText(text_region, "Length: " + str(track.playback_params.length))

        text_region.adjust(0, line_spacing, 0, 0)
        playback_mode_string = track.playback_params.mode.name
        painter.drawText(text_region, "Loop: " + playback_mode_string)

    def mouseMoveEvent(self, event):
        # rel = self.abs2rel(event.x(), event.y())
        self.mouse_pos = (event.x(), event.y())
        print(self.geometry())
        self.repaint()

    def poti_changed(self, track, row, value):
        print("track " + str(track) + " poti " + str(row) + " value changed: " + str(value))
        if row == 0:
            self.tracks[track].ambi_params.width = value*180
        if row == 1:
            self.tracks[track].ambi_params.side = value*12

        self.repaint()

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
