# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    copyright            : (C) 2014-2015 by Sandro Mani / Sourcepole AG
#    email                : smani@sourcepole.ch

from PyQt5.QtCore import Qt, QSettings, QPointF, QRectF, QRect, QUrl, pyqtSignal, QLocale
from PyQt5.QtGui import QColor, QDesktopServices, QIcon
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QFileDialog
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from qgis.core import QgsRectangle, QgsLayoutManager, QgsPointXY as QgsPoint, Qgis, QgsProject, QgsWkbTypes, QgsLayoutExporter, PROJECT_SCALES, QgsLayoutItemMap
from qgis.gui import QgisInterface, QgsMapTool, QgsRubberBand
import os
from .instantprint_dialog import Ui_InstantPrintDialog


class InstantPrintDialog(QDialog):

    hidden = pyqtSignal()

    def __init__(self, parent):
        QDialog.__init__(self, parent)

    def hideEvent(self, ev):
        self.hidden.emit()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hidden.emit()


class InstantPrintTool(QgsMapTool, InstantPrintDialog):

    def __init__(self, iface, populateCompositionFz=None):
        QgsMapTool.__init__(self, iface.mapCanvas())

        self.iface = iface
        projectInstance = QgsProject.instance()
        self.projectLayoutManager = projectInstance.layoutManager()
        self.rubberband = None
        self.oldrubberband = None
        self.pressPos = None
        self.printer = QPrinter()
        self.mapitem = None
        self.populateCompositionFz = populateCompositionFz

        self.dialog = InstantPrintDialog(self.iface.mainWindow())
        self.dialogui = Ui_InstantPrintDialog()
        self.dialogui.setupUi(self.dialog)
        self.dialogui.addScale.setIcon(QIcon(":/images/themes/default/mActionAdd.svg"))
        self.dialogui.deleteScale.setIcon(QIcon(":/images/themes/default/symbologyRemove.svg"))
        self.dialog.hidden.connect(self.__onDialogHidden)
        self.exportButton = self.dialogui.buttonBox.addButton(self.tr("Export"), QDialogButtonBox.ActionRole)
        self.printButton = self.dialogui.buttonBox.addButton(self.tr("Print"), QDialogButtonBox.ActionRole)
        self.helpButton = self.dialogui.buttonBox.addButton(self.tr("Help"), QDialogButtonBox.HelpRole)
        self.dialogui.comboBox_fileformat.addItem("PDF", self.tr("PDF Document (*.pdf);;"))
        self.dialogui.comboBox_fileformat.addItem("JPG", self.tr("JPG Image (*.jpg);;"))
        self.dialogui.comboBox_fileformat.addItem("BMP", self.tr("BMP Image (*.bmp);;"))
        self.dialogui.comboBox_fileformat.addItem("PNG", self.tr("PNG Image (*.png);;"))
        self.iface.layoutDesignerOpened.connect(lambda view: self.__reloadLayouts())
        self.iface.layoutDesignerWillBeClosed.connect(self.__reloadLayouts)
        self.dialogui.comboBox_layouts.currentIndexChanged.connect(self.__selectLayout)
        self.dialogui.comboBox_scale.lineEdit().textChanged.connect(self.__changeScale)
        self.dialogui.comboBox_scale.scaleChanged.connect(self.__changeScale)
        self.exportButton.clicked.connect(self.__export)
        self.printButton.clicked.connect(self.__print)
        self.helpButton.clicked.connect(self.__help)
        self.dialogui.buttonBox.button(QDialogButtonBox.Close).clicked.connect(lambda: self.dialog.hide())
        self.dialogui.addScale.clicked.connect(self.add_new_scale)
        self.dialogui.deleteScale.clicked.connect(self.remove_scale)
        self.deactivated.connect(self.__cleanup)
        self.setCursor(Qt.OpenHandCursor)

        settings = QSettings()
        if settings.value("instantprint/geometry") is not None:
            self.dialog.restoreGeometry(settings.value("instantprint/geometry"))
        if settings.value("instantprint/scales") is not None:
            for scale in settings.value("instantprint/scales").split(";"):
                if scale:
                    self.retrieve_scales(scale)
        self.check_scales()

    def __onDialogHidden(self):
        self.setEnabled(False)
        self.iface.mapCanvas().unsetMapTool(self)
        QSettings().setValue("instantprint/geometry", self.dialog.saveGeometry())
        list = []
        for i in range(self.dialogui.comboBox_scale.count()):
            list.append(self.dialogui.comboBox_scale.itemText(i))
        QSettings().setValue("instantprint/scales", ";".join(list))

    def retrieve_scales(self, checkScale):
        if self.dialogui.comboBox_scale.findText(checkScale) == -1:
            self.dialogui.comboBox_scale.addItem(checkScale)

    def add_new_scale(self):
        new_layout = self.dialogui.comboBox_scale.currentText()
        if self.dialogui.comboBox_scale.findText(new_layout) == -1:
            self.dialogui.comboBox_scale.addItem(new_layout)
        self.check_scales()

    def remove_scale(self):
        layout_to_delete = self.dialogui.comboBox_scale.currentIndex()
        self.dialogui.comboBox_scale.removeItem(layout_to_delete)
        self.check_scales()

    def setEnabled(self, enabled):
        if enabled:
            self.dialog.setVisible(True)
            self.__reloadLayouts()
            self.iface.mapCanvas().setMapTool(self)
        else:
            self.dialog.setVisible(False)
            self.iface.mapCanvas().unsetMapTool(self)

    def __changeScale(self):
        if not self.mapitem:
            return
        newscale = self.dialogui.comboBox_scale.scale()
        if abs(newscale) < 1E-6:
            return
        extent = self.mapitem.extent()
        center = extent.center()
        newwidth = extent.width() / self.mapitem.scale() * newscale
        newheight = extent.height() / self.mapitem.scale() * newscale
        x1 = center.x() - 0.5 * newwidth
        y1 = center.y() - 0.5 * newheight
        x2 = center.x() + 0.5 * newwidth
        y2 = center.y() + 0.5 * newheight
        self.mapitem.setExtent(QgsRectangle(x1, y1, x2, y2))
        self.__createRubberBand()
        self.check_scales()

    def __selectLayout(self):
        if not self.dialog.isVisible():
            return
        activeIndex = self.dialogui.comboBox_layouts.currentIndex()
        if activeIndex < 0:
            return

        layoutView = self.dialogui.comboBox_layouts.itemData(activeIndex)
        maps = []
        layout_name = self.dialogui.comboBox_layouts.currentText()
        layout = self.projectLayoutManager.layoutByName(layout_name)
        for item in layoutView.items():
            if isinstance(item, QgsLayoutItemMap):
                maps.append(item)
        if len(maps) != 1:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Invalid layout"), self.tr("The layout must have exactly one map item."))
            self.exportButton.setEnabled(False)
            self.iface.mapCanvas().scene().removeItem(self.rubberband)
            self.rubberband = None
            self.dialogui.comboBox_scale.setEnabled(False)
            return

        self.dialogui.comboBox_scale.setEnabled(True)
        self.exportButton.setEnabled(True)

        self.layoutView = layoutView
        self.mapitem = layout.referenceMap()
        self.dialogui.comboBox_scale.setScale(self.mapitem.scale())
        self.__createRubberBand()

    def __createRubberBand(self):
        self.__cleanup()
        extent = self.mapitem.extent()
        center = self.iface.mapCanvas().extent().center()
        self.corner = QPointF(center.x() - 0.5 * extent.width(), center.y() - 0.5 * extent.height())
        self.rect = QRectF(self.corner.x(), self.corner.y(), extent.width(), extent.height())
        self.mapitem.setExtent(QgsRectangle(self.rect))
        self.rubberband = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
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
            self.oldrubberband = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
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
            self.mapitem.setExtent(QgsRectangle(self.rect))

    def __canvasRect(self, rect):
        mtp = self.iface.mapCanvas().mapSettings().mapToPixel()
        p1 = mtp.transform(QgsPoint(rect.left(), rect.top()))
        p2 = mtp.transform(QgsPoint(rect.right(), rect.bottom()))
        return QRect(p1.x(), p1.y(), p2.x() - p1.x(), p2.y() - p1.y())

    def __export(self):
        settings = QSettings()
        format = self.dialogui.comboBox_fileformat.itemData(self.dialogui.comboBox_fileformat.currentIndex())
        filepath = QFileDialog.getSaveFileName(
            self.iface.mainWindow(),
            self.tr("Export Layout"),
            settings.value("/instantprint/lastfile", ""),
            format
        )
        if not all(filepath):
            return

        # Ensure output filename has correct extension
        filename = os.path.splitext(filepath[0])[0] + "." + self.dialogui.comboBox_fileformat.currentText().lower()
        settings.setValue("/instantprint/lastfile", filepath[0])

        if self.populateCompositionFz:
            self.populateCompositionFz(self.layoutView.composition())

        success = False
        layout_name = self.dialogui.comboBox_layouts.currentText()
        layout_item = self.projectLayoutManager.layoutByName(layout_name)
        exporter = QgsLayoutExporter(layout_item)
        if filename[-3:].lower() == u"pdf":
            success = exporter.exportToPdf(filepath[0], QgsLayoutExporter.PdfExportSettings())
        else:
            success = exporter.exportToImage(filepath[0], QgsLayoutExporter.ImageExportSettings())
        if success != 0:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Export Failed"), self.tr("Failed to export the layout."))

    def __print(self):
        layout_name = self.dialogui.comboBox_layouts.currentText()
        layout_item = self.projectLayoutManager.layoutByName(layout_name)
        actual_printer = QgsLayoutExporter(layout_item)

        printdialog = QPrintDialog(self.printer)
        if printdialog.exec_() != QDialog.Accepted:
            return

        success = actual_printer.print(self.printer, QgsLayoutExporter.PrintExportSettings())

        if success != 0:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Print Failed"), self.tr("Failed to print the layout."))

    def __reloadLayouts(self, removed=None):
        if not self.dialog.isVisible():
            # Make it less likely to hit the issue outlined in https://github.com/qgis/QGIS/pull/1938
            return

        self.dialogui.comboBox_layouts.blockSignals(True)
        prev = None
        if self.dialogui.comboBox_layouts.currentIndex() >= 0:
            prev = self.dialogui.comboBox_layouts.currentText()
        self.dialogui.comboBox_layouts.clear()
        active = 0
        for layout in self.projectLayoutManager.layouts():
            if layout != removed and layout.name():
                cur = layout.name()
                self.dialogui.comboBox_layouts.addItem(cur, layout)
                if prev == cur:
                    active = self.dialogui.comboBox_layouts.count() - 1
        self.dialogui.comboBox_layouts.setCurrentIndex(-1)  # Ensure setCurrentIndex below actually changes an index
        self.dialogui.comboBox_layouts.blockSignals(False)
        if self.dialogui.comboBox_layouts.count() > 0:
            self.dialogui.comboBox_layouts.setCurrentIndex(active)
            self.dialogui.comboBox_scale.setEnabled(True)
            self.exportButton.setEnabled(True)
        else:
            self.exportButton.setEnabled(False)
            self.dialogui.comboBox_scale.setEnabled(False)

    def __help(self):
        manualPath = os.path.join(os.path.dirname(__file__), "help", "documentation.pdf")
        QDesktopServices.openUrl(QUrl.fromLocalFile(manualPath))

    def scaleFromString(self, scaleText):
        locale = QLocale()
        parts = [locale.toInt(part) for part in scaleText.split(":")]
        try:
            if len(parts) == 2 and parts[0][1] and parts[1][1] and parts[0][0] != 0 and parts[1][0] != 0:
                return float(parts[0][0]) / float(parts[1][0])
            else:
                return None
        except ZeroDivisionError:
            return

    def check_scales(self):
        predefScalesStr = QSettings().value("Map/scales", PROJECT_SCALES).split(",")
        predefScales = [self.scaleFromString(scaleString) for scaleString in predefScalesStr]

        comboScalesStr = [self.dialogui.comboBox_scale.itemText(i) for i in range(self.dialogui.comboBox_scale.count())]
        comboScales = [self.scaleFromString(scaleString) for scaleString in comboScalesStr]

        currentScale = self.scaleFromString(self.dialogui.comboBox_scale.currentText())

        if not currentScale:
            self.dialogui.comboBox_scale.lineEdit().setStyleSheet("background: #FF7777; color: #FFFFFF;")
            self.dialogui.addScale.setVisible(True)
            self.dialogui.addScale.setEnabled(False)
            self.dialogui.deleteScale.setVisible(False)
        else:
            self.dialogui.comboBox_scale.lineEdit().setStyleSheet("")
            if currentScale in comboScales:
                # If entry scale is already in the list, allow removing it unless it is a predefined scale
                self.dialogui.addScale.setVisible(False)
                self.dialogui.deleteScale.setVisible(True)
                self.dialogui.deleteScale.setEnabled(currentScale not in predefScales)
            else:
                # Otherwise, show button to add it
                self.dialogui.addScale.setVisible(True)
                self.dialogui.addScale.setEnabled(True)
                self.dialogui.deleteScale.setVisible(False)
