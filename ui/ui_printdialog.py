# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/printdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qgis.PyQt.QtCore import QUrl, QCoreApplication, QTranslator, QSettings

class Ui_InstantPrintDialog(object):
    
    def tr(self,string):
        return QCoreApplication.translate('Ui_InstantPrintDialog', string)
    
    def setupUi(self, InstantPrintDialog):
        InstantPrintDialog.setObjectName("InstantPrintDialog")
        InstantPrintDialog.resize(357, 157)
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
        self.gridLayout.addWidget(self.label_fileformat, 2, 0, 1, 1)
        self.comboBox_fileformat = QtWidgets.QComboBox(InstantPrintDialog)
        self.comboBox_fileformat.setObjectName("comboBox_fileformat")
        self.gridLayout.addWidget(self.comboBox_fileformat, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(InstantPrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.widget = QtWidgets.QWidget(InstantPrintDialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_scale = QgsScaleComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_scale.sizePolicy().hasHeightForWidth())
        self.comboBox_scale.setSizePolicy(sizePolicy)
        self.comboBox_scale.setEditable(True)
        self.comboBox_scale.setObjectName("comboBox_scale")
        self.horizontalLayout.addWidget(self.comboBox_scale)
        self.deleteScale = QtWidgets.QToolButton(self.widget)
        self.deleteScale.setEnabled(False)
        self.deleteScale.setText("")
        self.deleteScale.setObjectName("deleteScale")
        self.horizontalLayout.addWidget(self.deleteScale)
        self.addScale = QtWidgets.QToolButton(self.widget)
        self.addScale.setEnabled(False)
        self.addScale.setText("")
        self.addScale.setObjectName("addScale")
        self.horizontalLayout.addWidget(self.addScale)
        self.gridLayout.addWidget(self.widget, 1, 1, 1, 1)

        self.retranslateUi(InstantPrintDialog)
        self.buttonBox.accepted.connect(InstantPrintDialog.accept)
        self.buttonBox.rejected.connect(InstantPrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InstantPrintDialog)

    def retranslateUi(self, InstantPrintDialog):
        _translate = QtCore.QCoreApplication.translate
        InstantPrintDialog.setWindowTitle(_translate("InstantPrintDialog", self.tr("Instant Print")))
        self.label_layout.setText(_translate("InstantPrintDialog", self.tr("Layout:")))
        self.label.setText(_translate("InstantPrintDialog", self.tr("Scale:")))
        self.label_fileformat.setText(_translate("InstantPrintDialog", self.tr("File format:")))

from qgis.gui import QgsScaleComboBox
