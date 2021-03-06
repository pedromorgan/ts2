#
#   Copyright (C) 2008-2013 by Nicolas Piganeau
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

from ts2 import simulation


class Clock(QtGui.QLCDNumber):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setFrameShadow(QtGui.QFrame.Plain)
        self.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.setNumDigits(8)
        self.display("--:--:--")
        self.resize(100,20)

    @QtCore.pyqtSlot(QtCore.QTime)
    def setTime(self, t):
        self.display(t.toString("hh:mm:ss"))

class ZoomWidget(QtGui.QWidget):
    """Zoom slider bar with associated spinBox."""

    def __init__(self, parent=None):
        """Constructor for the ZoomWidget class."""
        super().__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        self.button = QtGui.QPushButton(self.tr("100%"), self)

        self.slider = QtGui.QSlider(Qt.Horizontal, self)
        self.slider.setRange(10, 200)
        self.slider.setValue(100)
        self.slider.setSingleStep(10)

        self.spinBox = QtGui.QSpinBox(self)
        self.spinBox.setRange(10,200)
        self.spinBox.setSingleStep(1)
        self.spinBox.setValue(100)
        self.spinBox.setSuffix("%")
        self.spinBox.setCorrectionMode(
                                QtGui.QAbstractSpinBox.CorrectToNearestValue)

        self.button.clicked.connect(self.setDefaultZoom)
        self.slider.valueChanged.connect(self.spinBox.setValue)
        self.spinBox.valueChanged.connect(self.slider.setValue)
        self.spinBox.valueChanged.connect(self.valueChanged)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.button)
        hlayout.addWidget(self.slider)
        hlayout.addWidget(self.spinBox)
        hlayout.setMargin(0)
        self.setLayout(hlayout)

    valueChanged = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot()
    def setDefaultZoom(self):
        """Sets the zoom to 100%."""
        self.spinBox.setValue(100)

    def sizeHint(self):
        return QtCore.QSize(300,50)

    def minimumSizeHint(self):
        return QtCore.QSize(300,50)


class Panel(QtGui.QWidget):
    """The panel is the display rectangle below the scene holding the widgets
    necessary to play the simulation (e.g. clock)."""

    def __init__(self, parent, simulationWindow):
        """Constructor for the Panel class."""
        super().__init__(parent)
        self.simulation = None
        self.simulationWindow = simulationWindow
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Fixed)
        # Clock
        self.clock = Clock(self)
        # Pause button
        self.pauseButton = QtGui.QPushButton(self.tr("Pause"), self)
        self.pauseButton.setCheckable(True)
        # Time factor spinBox
        self.timeFactorSpinBox = QtGui.QSpinBox(self)
        self.timeFactorSpinBox.setRange(0, 10)
        self.timeFactorSpinBox.setSingleStep(1)
        self.timeFactorSpinBox.setValue(1)
        self.timeFactorSpinBox.setSuffix("x")
        # Zoom spinBox
        self.zoomWidget = ZoomWidget(self)
        self.zoomWidget.valueChanged.connect(self.simulationWindow.zoom)
        # score display
        self.scoreDisplay = QtGui.QLCDNumber(self)
        self.scoreDisplay.setFrameShape(QtGui.QFrame.NoFrame)
        self.scoreDisplay.setFrameShadow(QtGui.QFrame.Plain)
        self.scoreDisplay.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.scoreDisplay.setNumDigits(5)
        self.scoreDisplay.resize(70, 25)

        layout = QtGui.QHBoxLayout()
        layout.addSpacing(5)
        layout.addWidget(self.clock)
        layout.addSpacing(5)
        layout.addWidget(self.pauseButton)
        layout.addSpacing(5)
        layout.addWidget(QtGui.QLabel(self.tr("Simulation speed: ")))
        layout.addWidget(self.timeFactorSpinBox)
        layout.addSpacing(5)
        # layout.addWidget(QtGui.QLabel(self.tr("Zoom: ")))
        layout.addWidget(self.zoomWidget)
        layout.addStretch()
        layout.addWidget(QtGui.QLabel(self.tr("Penalty points: ")))
        layout.addWidget(self.scoreDisplay)
        self.setLayout(layout)

        self.simulationWindow.simulationLoaded.connect(self.activate)

    @QtCore.pyqtSlot(simulation.Simulation)
    def activate(self, sim):
        """Activates the panel with the given simulation."""
        self.simulation = sim
        self.pauseButton.toggled.connect(self.simulation.pause)
        self.pauseButton.toggled.connect(self.changePauseButtonText)
        self.timeFactorSpinBox.valueChanged.connect(
                                            self.simulation.setTimeFactor)
        self.timeFactorSpinBox.setValue(
                                float(self.simulation.option("timeFactor")))

    zoomChanged = QtCore.pyqtSignal(int)

    def sizeHint(self):
        return QtCore.QSize(800,40)

    def minimumSizeHint(self):
        return QtCore.QSize(200,40)


    @QtCore.pyqtSlot(bool)
    def changePauseButtonText(self, paused):
        if paused:
            self.pauseButton.setText(self.tr("Continue"))
        else:
            self.pauseButton.setText(self.tr("Pause"))

    @QtCore.pyqtSlot(int)
    def zoomWidgetChanged(self, percent):
        self.zoomChanged.emit(percent)

