#
#   Copyright (C) 2008-2014 by Nicolas Piganeau
#   npi@m4x.org
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt


class SignalShape:
    """This class holds the possible representation shapes for signal lights.
    """
    NONE = 0
    CIRCLE = 1
    SQUARE = 2
    QUARTER_SW = 10
    QUARTER_NW = 11
    QUARTER_NE = 12
    QUARTER_SE = 13
    BAR_N_S = 20
    BAR_E_W = 21
    BAR_SW_NE = 22
    BAR_NW_SE = 23
    POLE_NS = 31
    POLE_NSW = 32
    POLE_SW = 33
    POLE_NE = 34
    POLE_NSE = 35

class SignalLineStyle:
    """This class holds the possible representation shapes for the line at
    the base of the signal.
    """
    LINE = 0
    BUFFER = 1

class Target:
    """This class defines when a speed limit associated with a signal aspect
    must be applied."""
    ASAP = 0
    BEFORE_THIS_SIGNAL = 1
    BEFORE_NEXT_SIGNAL = 2

class SignalAspect(QtCore.QObject):
    """SignalAspect class represents an aspect of a signal, that is a
    combination of on and off lights with a meaning for the train driver."""

    def __init__(self, parameters):
        """Constructor for the SignalAspect class."""
        super().__init__()
        self.name = parameters["name"]
        self.lineStyle = int(parameters["linestyle"])
        self.outerShapes = eval(str(parameters["outershapes"]))
        self.outerColors = eval(str(parameters["outercolors"]))
        self.shapes = eval(str(parameters["shapes"]))
        self.shapesColors = eval(str(parameters["shapescolors"]))
        self.actions = [(t, s) for t, s in zip(
                                        eval(str(parameters["targets"])),
                                        eval(str(parameters["speedlimits"])))]

    def meansProceed(self):
        """Returns true if this aspect is a proceed aspect, returns false if
        this aspect requires to stop."""
        return self.actions[0] != (0, 0) and self.actions[0] != (1, 0)

    def drawAspect(self, p, linePen, shapePen, persistent=False):
        """Draws the aspect on the given painter p. Draws the line with
        linePen and the shapes with shapePen."""

        if self.lineStyle == SignalLineStyle.BUFFER:
            p.setPen(shapePen)
            brush = QtGui.QBrush(Qt.SolidPattern)
            brush.setColor(Qt.darkGray)
            p.setBrush(brush)
            triangle = QtGui.QPolygonF()
            triangle << QtCore.QPointF(4, -4) \
                     << QtCore.QPointF(4, 4) \
                     << QtCore.QPointF(9, 0)
            p.drawPolygon(triangle)

        elif self.lineStyle == SignalLineStyle.LINE:
            p.setPen(linePen)
            p.drawLine(0, 0, 10, 0)

            # Draw the signal itself
            p.setPen(shapePen)
            brush = QtGui.QBrush(Qt.SolidPattern)
            for i in range(6):
                p.drawLine(2, 0, 2, -7)
                p.drawLine(2, -7, 8, -7)
                r = QtCore.QRect((i // 2) * 8 + 8, -(i % 2) * 8 - 11, 8, 8)
                brush.setColor(QtGui.QColor(self.outerColors[i]))
                p.setBrush(brush)
                self.drawShape(p, self.outerShapes[i], r)
                brush.setColor(QtGui.QColor(self.shapesColors[i]))
                p.setBrush(brush)
                self.drawShape(p, self.shapes[i], r)

            # Draw persistent route marker
            if persistent:
                ppen = QtGui.QPen(Qt.white)
                ppen.setWidthF(2.5)
                ppen.setCapStyle(Qt.FlatCap)
                p.setPen(ppen)
                p.drawLine(6, -10, 6, -3)


    def drawShape(self, p, shape, rect):
        """Draws the shape on painter p inside rect."""
        # TODO: Draw missing shapes
        if shape == SignalShape.CIRCLE:
            p.drawEllipse(rect)
        elif shape == SignalShape.SQUARE:
            p.drawRect(rect)
        elif shape == SignalShape.QUARTER_SW:
            points = {rect.topLeft(), rect.topRight(), rect.bottomLeft()}
            p.drawPolygon(points)
        elif shape == SignalShape.QUARTER_NW:
            points = {rect.topRight(), rect.bottomRight(), rect.topLeft()}
            p.drawPolygon(points)
        elif shape == SignalShape.QUARTER_NE:
            points = {rect.bottomRight(), rect.bottomLeft(), rect.topRight()}
            p.drawPolygon(points)
        elif shape == SignalShape.QUARTER_SE:
            points = {rect.bottomLeft(), rect.topLeft(), rect.bottomRight()}
            p.drawPolygon(points)
        elif shape == SignalShape.BAR_N_S:
            tl = rect.topLeft() + QtCore.QPointF(1, 3)
            p.drawRect(QtCore.QRectF(tl, QtCore.QSizeF(6, 2)))
        elif shape == SignalShape.BAR_E_W:
            tl = rect.topLeft() + QtCore.QPointF(3, 1)
            p.drawRect(QtCore.QRectF(tl, QtCore.QSizeF(2, 6)))
        elif (shape == SignalShape.POLE_NE or
              shape == SignalShape.POLE_NS or
              shape == SignalShape.POLE_NSE or
              shape == SignalShape.POLE_NSW):
            tm = QtCore.QPointF(rect.center().x(), rect.top())
            p.drawLine(rect.center(), tm)
        elif (shape == SignalShape.POLE_NS or
              shape == SignalShape.POLE_NSE or
              shape == SignalShape.POLE_NSW or
              shape == SignalShape.POLE_SW):
            bm = QtCore.QPointF(rect.center().x(), rect.bottom())
            p.drawLine(rect.center(), bm)
        elif (shape == SignalShape.POLE_NE or
              shape == SignalShape.POLE_NSE):
            rm = QtCore.QPointF(rect.right().x(), rect.center().y())
            p.drawLine(rect.center(), rm)
        elif (shape == SignalShape.POLE_NSW or
              shape == SignalShape.POLE_SW):
            lm = QtCore.QPointF(rect.left().x(), rect.center().y())
            p.drawLine(rect.center(), lm)

    def boundingRect(self):
        """Return the boundingRect of this aspect."""
        return QtCore.QRectF(0, -20, 33, 24)

