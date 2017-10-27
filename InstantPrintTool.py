# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    copyright            : (C) 2014-2015 by Sandro Mani / Sourcepole AG
#    email                : smani@sourcepole.ch

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os

from ui.ui_printdialog import Ui_InstantPrintDialog


class InstantPrintDialog(QDialog):

    hidden = pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)

    def hideEvent(self, ev):
        self.hidden.emit()


class InstantPrintTool(QgsMapTool, InstantPrintDialog):

    def __init__(self, iface, populateCompositionFz=None):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.iface = iface
        self.rubberband = None
        self.oldrubberband = None
        self.pressPos = None
        self.populateCompositionFz = populateCompositionFz

        self.dialog = InstantPrintDialog()
        self.dialogui = Ui_InstantPrintDialog()
        self.dialogui.setupUi(self.dialog)
        self.dialog.hidden.connect(self.__onDialogHidden)
        self.exportButton = self.dialogui.buttonBox.addButton(self.tr("Export"), QDialogButtonBox.ActionRole)
        self.helpButton = self.dialogui.buttonBox.addButton(self.tr("Help"), QDialogButtonBox.HelpRole)
        self.dialogui.comboBox_fileformat.addItem("PDF", self.tr("PDF Document (*.pdf);;"))
        self.dialogui.comboBox_fileformat.addItem("JPG", self.tr("JPG Image (*.jpg);;"))
        self.dialogui.comboBox_fileformat.addItem("BMP", self.tr("BMP Image (*.bmp);;"))
        self.dialogui.comboBox_fileformat.addItem("PNG", self.tr("PNG Image (*.png);;"))
        self.dialogui.spinBoxScale.valueChanged.connect(self.__changeScale)

        self.iface.composerAdded.connect(lambda view: self.__reloadComposers())
        self.iface.composerWillBeRemoved.connect(self.__reloadComposers)
        self.dialogui.comboBox_composers.currentIndexChanged.connect(self.__selectComposer)
        self.exportButton.clicked.connect(self.__export)
        self.helpButton.clicked.connect(self.__help)
        self.dialogui.buttonBox.button(QDialogButtonBox.Close).clicked.connect(lambda: self.dialog.hide())
        self.deactivated.connect(self.__cleanup)
        self.setCursor(Qt.OpenHandCursor)

        settings = QSettings()
        if not settings.value("geometry") is None:
            self.dialog.restoreGeometry(settings.value("geometry"))

    def __onDialogHidden(self):
        self.setEnabled(False)
        QSettings().setValue("geometry", self.dialog.saveGeometry())

    def setEnabled(self, enabled):
        if enabled:
            self.dialog.setVisible(True)
            self.__reloadComposers()
            self.iface.mapCanvas().setMapTool(self)
        else:
            self.iface.mapCanvas().unsetMapTool(self)

    def __changeScale(self):
        if not self.mapitem:
            return
        newscale = self.dialogui.spinBoxScale.value()
        extent = self.mapitem.extent()
        center = extent.center()
        newwidth = extent.width() / self.mapitem.scale() * newscale
        newheight = extent.height() / self.mapitem.scale() * newscale
        x1 = center.x() - 0.5 * newwidth
        y1 = center.y() - 0.5 * newheight
        x2 = center.x() + 0.5 * newwidth
        y2 = center.y() + 0.5 * newheight
        self.mapitem.setNewExtent(QgsRectangle(x1, y1, x2, y2))
        self.__createRubberBand()

    def __selectComposer(self):
        if not self.dialog.isVisible():
            return
        activeIndex = self.dialogui.comboBox_composers.currentIndex()
        if activeIndex < 0:
            return

        composerView = self.dialogui.comboBox_composers.itemData(activeIndex)
        try:
            maps = composerView.composition().composerMapItems()
        except:
            # composerMapItems is not available with PyQt4 < 4.8.4
            maps = []
            for item in composerView.composition().items():
                if isinstance(item, QgsComposerMap):
                    maps.append(item)
        if len(maps) != 1:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Invalid composer"), self.tr("The composer must have exactly one map item."))
            self.exportButton.setEnabled(False)
            self.iface.mapCanvas().scene().removeItem(self.rubberband)
            self.rubberband = None
            self.dialogui.spinBoxScale.setEnabled(False)
            return

        self.dialogui.spinBoxScale.setEnabled(True)
        self.exportButton.setEnabled(True)

        self.composerView = composerView
        self.mapitem = maps[0]
        self.dialogui.spinBoxScale.setValue(self.mapitem.scale())
        self.__createRubberBand()

    def __createRubberBand(self):
        self.__cleanup()
        extent = self.mapitem.extent()
        center = self.iface.mapCanvas().extent().center()
        self.corner = QPointF(center.x() - 0.5 * extent.width(), center.y() - 0.5 * extent.height())
        self.rect = QRectF(self.corner.x(), self.corner.y(), extent.width(), extent.height())
        self.mapitem.setNewExtent(QgsRectangle(self.rect))

        self.rubberband = QgsRubberBand(self.iface.mapCanvas(), QGis.Polygon)
        self.rubberband.setToCanvasRectangle(self.__canvasRect(self.rect))
        self.rubberband.setColor(QColor(127, 127, 255, 127))

        self.pressPos = None

    def __cleanup(self):
        if self.rubberband:
            self.iface.mapCanvas().scene().removeItem(self.rubberband)
        if self.oldrubberband:
            self.iface.mapCanvas().scene().removeItem(self.oldrubberband)
        self.rubberband = None
        self.oldrubberband = None
        self.pressPos = None

    def canvasPressEvent(self, e):
        if not self.rubberband:
            return
        r = self.__canvasRect(self.rect)
        if e.button() == Qt.LeftButton and self.__canvasRect(self.rect).contains(e.pos()):
            self.oldrect = QRectF(self.rect)
            self.oldrubberband = QgsRubberBand(self.iface.mapCanvas(), QGis.Polygon)
            self.oldrubberband.setToCanvasRectangle(self.__canvasRect(self.oldrect))
            self.oldrubberband.setColor(QColor(127, 127, 255, 31))
            self.pressPos = (e.x(), e.y())
            self.iface.mapCanvas().setCursor(Qt.ClosedHandCursor)

    def canvasMoveEvent(self, e):
        if not self.pressPos:
            return
        mup = self.iface.mapCanvas().mapSettings().mapUnitsPerPixel()
        x = self.corner.x() + (e.x() - self.pressPos[0]) * mup
        y = self.corner.y() + (self.pressPos[1] - e.y()) * mup

        snaptol = 10 * mup
        # Left edge matches with old right
        if abs(x - (self.oldrect.x() + self.oldrect.width())) < snaptol:
            x = self.oldrect.x() + self.oldrect.width()
        # Right edge matches with old left
        elif abs(x + self.rect.width() - self.oldrect.x()) < snaptol:
            x = self.oldrect.x() - self.rect.width()
        # Left edge matches with old left
        elif abs(x - self.oldrect.x()) < snaptol:
            x = self.oldrect.x()
        # Bottom edge matches with old top
        if abs(y - (self.oldrect.y() + self.oldrect.height())) < snaptol:
            y = self.oldrect.y() + self.oldrect.height()
        # Top edge matches with old bottom
        elif abs(y + self.rect.height() - self.oldrect.y()) < snaptol:
            y = self.oldrect.y() - self.rect.height()
        # Bottom edge matches with old bottom
        elif abs(y - self.oldrect.y()) < snaptol:
            y = self.oldrect.y()

        self.rect = QRectF(
            x,
            y,
            self.rect.width(),
            self.rect.height()
        )
        self.rubberband.setToCanvasRectangle(self.__canvasRect(self.rect))

    def canvasReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.pressPos:
            self.corner = QPointF(self.rect.x(), self.rect.y())
            self.pressPos = None
            self.iface.mapCanvas().setCursor(Qt.OpenHandCursor)
            self.iface.mapCanvas().scene().removeItem(self.oldrubberband)
            self.oldrect = None
            self.oldrubberband = None
            self.mapitem.setNewExtent(QgsRectangle(self.rect))

    def __canvasRect(self, rect):
        mtp = self.iface.mapCanvas().mapSettings().mapToPixel()
        p1 = mtp.transform(QgsPoint(rect.left(), rect.top()))
        p2 = mtp.transform(QgsPoint(rect.right(), rect.bottom()))
        return QRect(p1.x(), p1.y(), p2.x() - p1.x(), p2.y() - p1.y())

    def __export(self):
        settings = QSettings()
        format = self.dialogui.comboBox_fileformat.itemData(self.dialogui.comboBox_fileformat.currentIndex())
        filename = QFileDialog.getSaveFileName(
            self.iface.mainWindow(),
            self.tr("Print Composition"),
            settings.value("/instantprint/lastfile", ""),
            format
        )
        if not filename:
            return

        # Ensure output filename has correct extension
        filename = os.path.splitext(filename)[0] + "." + self.dialogui.comboBox_fileformat.currentText().lower()

        settings.setValue("/instantprint/lastfile", filename)

        if self.populateCompositionFz:
            self.populateCompositionFz(self.composerView.composition())

        success = False
        if filename[-3:].lower() == u"pdf":
            success = self.composerView.composition().exportAsPDF(filename)
        else:
            image = self.composerView.composition().printPageAsRaster(self.composerView.composition().itemPageNumber(self.mapitem))
            if not image.isNull():
                success = image.save(filename)
        if not success:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Print Failed"), self.tr("Failed to print the composition."))

    def __reloadComposers(self, removed=None):
        if not self.dialog.isVisible():
            # Make it less likely to hit the issue outlined in https://github.com/qgis/QGIS/pull/1938
            return

        self.dialogui.comboBox_composers.blockSignals(True)
        prev = None
        if self.dialogui.comboBox_composers.currentIndex() >= 0:
            prev = self.dialogui.comboBox_composers.currentText()
        self.dialogui.comboBox_composers.clear()
        active = 0
        for composer in self.iface.activeComposers():
            if composer != removed and composer.composerWindow():
                cur = composer.composerWindow().windowTitle()
                self.dialogui.comboBox_composers.addItem(cur, composer)
                if prev == cur:
                    active = self.dialogui.comboBox_composers.count() - 1
        self.dialogui.comboBox_composers.setCurrentIndex(-1)  # Ensure setCurrentIndex below actually changes an index
        self.dialogui.comboBox_composers.blockSignals(False)
        if self.dialogui.comboBox_composers.count() > 0:
            self.dialogui.comboBox_composers.setCurrentIndex(active)
            self.dialogui.spinBoxScale.setEnabled(True)
            self.exportButton.setEnabled(True)
        else:
            self.exportButton.setEnabled(False)
            self.dialogui.spinBoxScale.setEnabled(False)

    def __help(self):
        manualPath = os.path.join(os.path.dirname(__file__), "help", "documentation.pdf")
        QDesktopServices.openUrl(QUrl.fromLocalFile(manualPath))
