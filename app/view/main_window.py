# coding: utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from app.view.develop_interface import DevelopInterface
from app.view.editor_interface import EditorInterface
from .components.customBoxBase import ExitConfirmMessageBox
from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from ..common.config import cfg
from ..common import resource

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.alertMessage = None
        self.navigationInterface.setAcrylicEnabled(True)

        '''' interface init '''
        self.homeInterface = HomeInterface(self)
        self.developInterface = DevelopInterface(self)
        self.editorInterface = EditorInterface(self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()
        self.splashScreen.finish()

        '''' rewrite close event '''
        self.closeEvent = self.closeEvent

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Домашняя страница'))

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.developInterface, FIF.EDUCATION, 'Начать новый тест')
        self.addSubInterface(self.editorInterface, FIF.EDIT, 'Редактор')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Настройки'), NavigationItemPosition.BOTTOM)

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
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def closeEvent(self, event):
        if self.alertMessage:
            w = ExitConfirmMessageBox(self, 'Закрыть окно', self.alertMessage)
            if not w.exec():
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

