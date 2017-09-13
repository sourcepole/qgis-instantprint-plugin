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

from InstantPrintTool import InstantPrintTool


class InstantPrintPlugin(QObject):
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface
        self.pluginDir = os.path.dirname(__file__)
        self.tool = InstantPrintTool(self.iface)

        # Localize
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.pluginDir, 'i18n', 'instantprint_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.toolButton = QToolButton(self.iface.mapNavToolToolBar())
        self.toolButton.setIcon(QIcon(":/plugins/instantprint/icons/icon.png"))
        self.toolButton.setText(self.tr("Instant Print"))
        self.toolButton.setToolTip(self.tr("Instant Print"))
        self.toolButton.setCheckable(True)
        self.toolAction = self.iface.pluginToolBar().addWidget(self.toolButton)

        self.toolButton.toggled.connect(self.__enableTool)
        self.iface.mapCanvas().mapToolSet.connect(self.__onToolSet)

    def unload(self):
        self.tool.setEnabled(False)
        self.tool = None
        self.iface.pluginToolBar().removeAction(self.toolAction)

    def __enableTool(self, active):
        self.tool.setEnabled(active)

    def __onToolSet(self, tool):
        if tool != self.tool:
            self.toolButton.setChecked(False)
