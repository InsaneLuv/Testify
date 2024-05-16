# coding: utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from .custom.DevelopInterface import DevelopInterface
from .custom.EditorInterface import EditorInterface
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.homeInterface = HomeInterface(self)
        self.developInterface = DevelopInterface(self)
        self.editorInterface = EditorInterface(self)
        self.settingInterface = SettingInterface(self)

        self.navigationInterface.setAcrylicEnabled(True)

        self.initNavigation()
        self.splashScreen.finish()

    def addNewSubInterface(self, interface, icon, name):
        self.addSubInterface(interface, icon, name)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Домашняя страница'))
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.developInterface, FIF.EDUCATION,'Начать новый тест')
        self.addSubInterface(self.editorInterface, FIF.EDIT, 'Редактор')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Настройки'), NavigationItemPosition.BOTTOM)
        self.switchTo(self.editorInterface)

    def initWindow(self):
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(':/gallery/images/Singer.png'))
        self.setWindowTitle('Testify')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(200, 200))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())