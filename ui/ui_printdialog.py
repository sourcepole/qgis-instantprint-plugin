# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_InstantPrintDialog(object):
    def setupUi(self, InstantPrintDialog):
        InstantPrintDialog.setObjectName("InstantPrintDialog")
        InstantPrintDialog.resize(263, 162)
        icon = QtGui.QIcon.fromTheme("printer")
        InstantPrintDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(InstantPrintDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_layout = QtWidgets.QLabel(InstantPrintDialog)
        self.label_layout.setObjectName("label_layout")
        self.gridLayout.addWidget(self.label_layout, 0, 0, 1, 1)
        self.comboBox_layouts = QtWidgets.QComboBox(InstantPrintDialog)
        self.comboBox_layouts.setEditable(False)
        self.comboBox_layouts.setObjectName("comboBox_layouts")
        self.gridLayout.addWidget(self.comboBox_layouts, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(InstantPrintDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_fileformat = QtWidgets.QLabel(InstantPrintDialog)
        self.label_fileformat.setObjectName("label_fileformat")
        self.gridLayout.addWidget(self.label_fileformat, 3, 0, 1, 1)
        self.comboBox_fileformat = QtWidgets.QComboBox(InstantPrintDialog)
        self.comboBox_fileformat.setObjectName("comboBox_fileformat")
        self.gridLayout.addWidget(self.comboBox_fileformat, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(InstantPrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.spinBoxScale = QtWidgets.QSpinBox(InstantPrintDialog)
        self.spinBoxScale.setPrefix("1:")
        self.spinBoxScale.setMinimum(1)
        self.spinBoxScale.setMaximum(1000000000)
        self.spinBoxScale.setObjectName("spinBoxScale")
        self.gridLayout.addWidget(self.spinBoxScale, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(InstantPrintDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.retranslateUi(InstantPrintDialog)
        self.buttonBox.accepted.connect(InstantPrintDialog.accept)
        self.buttonBox.rejected.connect(InstantPrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InstantPrintDialog)

    def retranslateUi(self, InstantPrintDialog):
        _translate = QtCore.QCoreApplication.translate
        InstantPrintDialog.setWindowTitle(_translate("InstantPrintDialog", "Instant Print"))
        self.label_layout.setText(_translate("InstantPrintDialog", "Layout:"))
        self.label.setText(_translate("InstantPrintDialog", "Scale:"))
        self.label_fileformat.setText(_translate("InstantPrintDialog", "File format:"))

from qgis.gui import QgsScaleComboBox
