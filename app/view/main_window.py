# coding: utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen, MessageBoxBase, SubtitleLabel, BodyLabel)
from qfluentwidgets import FluentIcon as FIF

from app.view.develop_interface import DevelopInterface
from app.view.editor_interface import EditorInterface
from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from ..common.config import cfg
from ..common import resource
from .test_interface import TimerManager

class CustomMessageBox(MessageBoxBase):
    def __init__(self, parent, title=None, message=None):
        super().__init__(parent)

        self.cancelButton.setEnabled(False)

        self.titleLabel = SubtitleLabel(title, self)
        self.viewLayout.addWidget(self.titleLabel)

        self.subLabel = BodyLabel(message, self)
        self.viewLayout.addWidget(self.subLabel)

        self.widget.setMinimumWidth(360)

        self.yesButton.setText('Отменить')
        self.yesButton.setShortcut("Return")

        self.cancelButton.setText(f'Выйти')

        self.timer = TimerManager(3 / 60, self.updateCancelButton, self.enableCancelButton)
        self.timer.start_timer()

    def enableCancelButton(self):
        self.cancelButton.setEnabled(True)
        self.cancelButton.setText(f'Выйти')

    def updateCancelButton(self, time):
        self.cancelButton.setText(f'Выйти ({time.toString("s")})')



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
        self.alertMessage = None

        self.closeEvent = self.closeEvent

    def closeEvent(self, event):
        if self.alertMessage:
            w = CustomMessageBox(self, 'Закрыть окно', self.alertMessage)
            if not w.exec():
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def addNewSubInterface(self, interface, icon, name):
        self.addSubInterface(interface, icon, name)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Домашняя страница'))
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.developInterface, FIF.EDUCATION,'Начать новый тест')
        self.addSubInterface(self.editorInterface, FIF.EDIT, 'Редактор')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Настройки'), NavigationItemPosition.BOTTOM)
        self.switchTo(self.developInterface)

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