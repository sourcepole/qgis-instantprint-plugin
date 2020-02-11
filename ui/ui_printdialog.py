# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printdialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        InstantPrintDialog.setObjectName(_fromUtf8("InstantPrintDialog"))
        InstantPrintDialog.resize(357, 157)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("printer"))
        InstantPrintDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(InstantPrintDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_composers = QtGui.QLabel(InstantPrintDialog)
        self.label_composers.setObjectName(_fromUtf8("label_composers"))
        self.gridLayout.addWidget(self.label_composers, 0, 0, 1, 1)
        self.comboBox_composers = QtGui.QComboBox(InstantPrintDialog)
        self.comboBox_composers.setEditable(False)
        self.comboBox_composers.setObjectName(_fromUtf8("comboBox_composers"))
        self.gridLayout.addWidget(self.comboBox_composers, 0, 1, 1, 1)
        self.label = QtGui.QLabel(InstantPrintDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        ### Ben Wirf 6/2/2020
        self.label_rotation = QtGui.QLabel(InstantPrintDialog)
        self.label_rotation.setObjectName("label_rotation")
        self.gridLayout.addWidget(self.label_rotation, 2, 0, 1, 1)
        self.spinBox_rotation = QtGui.QSpinBox(InstantPrintDialog)
        self.spinBox_rotation.setObjectName("spinBox_rotation")
        self.gridLayout.addWidget(self.spinBox_rotation, 2, 1, 1, 1)
        self.label_useRotation = QtGui.QLabel(InstantPrintDialog)
        self.label_useRotation.setObjectName("label_useRotation")
        self.gridLayout.addWidget(self.label_useRotation, 3, 0, 1, 1)
        self.comboBox_useRotation = QtGui.QComboBox(InstantPrintDialog)
        self.comboBox_useRotation.setObjectName("comboBox_useRotation")
        self.gridLayout.addWidget(self.comboBox_useRotation, 3, 1, 1, 1)
        ###
        self.label_fileformat = QtGui.QLabel(InstantPrintDialog)
        self.label_fileformat.setObjectName(_fromUtf8("label_fileformat"))
        self.gridLayout.addWidget(self.label_fileformat, 4, 0, 1, 1)
        self.comboBox_fileformat = QtGui.QComboBox(InstantPrintDialog)
        self.comboBox_fileformat.setObjectName(_fromUtf8("comboBox_fileformat"))
        self.gridLayout.addWidget(self.comboBox_fileformat, 4, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InstantPrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.widget = QtGui.QWidget(InstantPrintDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox_scale = QgsScaleComboBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_scale.sizePolicy().hasHeightForWidth())
        self.comboBox_scale.setSizePolicy(sizePolicy)
        self.comboBox_scale.setEditable(True)
        self.comboBox_scale.setObjectName(_fromUtf8("comboBox_scale"))
        self.horizontalLayout.addWidget(self.comboBox_scale)
        self.deleteScale = QtGui.QToolButton(self.widget)
        self.deleteScale.setText(_fromUtf8(""))
        self.deleteScale.setObjectName(_fromUtf8("deleteScale"))
        self.horizontalLayout.addWidget(self.deleteScale)
        self.addScale = QtGui.QToolButton(self.widget)
        self.addScale.setText(_fromUtf8(""))
        self.addScale.setObjectName(_fromUtf8("addScale"))
        self.horizontalLayout.addWidget(self.addScale)
        self.gridLayout.addWidget(self.widget, 1, 1, 1, 1)

        self.retranslateUi(InstantPrintDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InstantPrintDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InstantPrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InstantPrintDialog)

    def retranslateUi(self, InstantPrintDialog):
        InstantPrintDialog.setWindowTitle(_translate("InstantPrintDialog", "Instant Print", None))
        self.label_composers.setText(_translate("InstantPrintDialog", "Composer:", None))
        self.label.setText(_translate("InstantPrintDialog", "Scale:", None))
        self.label_fileformat.setText(_translate("InstantPrintDialog", "File format:", None))
        ### Ben Wirf 6/5/2020
        self.label_rotation.setText(_translate("InstantPrintDialog", "Set Rotation:", None))
        self.label_useRotation.setText(_translate("InstantPrintDialog", "Use rotation value:", None))
        ###

from qgis.gui import QgsScaleComboBox
