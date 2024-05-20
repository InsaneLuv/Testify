# coding:utf-8
import json
import os
import random
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QCompleter
from qfluentwidgets import FluentIcon, setFont, InfoBarIcon, PushButton, MessageBox, NavigationItemPosition, setTheme, \
    RoundMenu, TabBar, MSFluentTitleBar, MessageBoxBase, SearchLineEdit
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAction, QGridLayout
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TogglePushButton, ToggleToolButton, TransparentPushButton, TransparentToolButton,
                            TransparentToggleToolButton, TransparentTogglePushButton, TransparentDropDownToolButton,
                            TransparentDropDownPushButton, PillPushButton, PillToolButton, setCustomStyleSheet,
                            CustomStyleSheet, SubtitleLabel, LineEdit, CaptionLabel)
from qfluentwidgets import FluentIcon as FIF

from .test_interface import TestInterface, Question
from .Ui_DevelopInterface import Ui_DevelopInterface
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Theme, Action
from app.common.config import cfg
from app.common.icon import Icon
from app.common.style_sheet import StyleSheet

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('Введите ваши данные'), self)
        self.viewLayout.addWidget(self.titleLabel)

        self.userNameEdit = SearchLineEdit(self)
        self.userNameEdit.setPlaceholderText(self.tr('Имя Фамилия'))
        self.userNameEdit.setClearButtonEnabled(True)
        self.userNameEdit.setMaxLength(50)
        self.completerNames = cfg.get(cfg.userHistory)
        completer = QCompleter(self.completerNames, self.userNameEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(3)
        self.userNameEdit.setCompleter(completer)
        self.viewLayout.addWidget(self.userNameEdit)

        self.yesButton.setText('Начать тест')
        self.yesButton.setShortcut("Return")
        self.yesButton.setIcon(FIF.PLAY)
        self.cancelButton.setText('Отменить')
        self.cancelButton.setShortcut("Esc")

        self.widget.setMinimumWidth(400)
        self.yesButton.setDisabled(True)
        self.userNameEdit.textChanged.connect(self.ifTextInput)

    def ifTextInput(self, text):
        if len(text.split()) >= 2:
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)


class DevelopInterface(Ui_DevelopInterface, QWidget):

    def __init__(self, parent=None,):
        self.parent = parent
        super().__init__(parent=parent)
        self.setObjectName('developInterface')
        self.setupUi(self)
        self.nameWindow = CustomMessageBox(self.window())
        self.name = None
        self._initInterface()
        self.createdFileInterfaces = []
        # newTestInterface = TestInterface(self, filePath='D:/Users/luv/Desktop/Testify/Новый тест.tstf', userName='Данила Данилов')
        # newTestInterface.setObjectName('D:/Users/luv/Desktop/Testify/Новый тест.tstf')
        # self.addInterfaceToSuperview(newTestInterface, 'D:/Users/luv/Desktop/Testify/Новый тест.tstf')
        # self.parent.switchTo(newTestInterface)

    def _initInterface(self):

        self.ChooseFileIcon.setIcon(FIF.SHARE)
        self.ChooseFileButton.clicked.connect(self.ChooseFileButtonAction)

        self.ChooseFileButton.setIcon(FIF.FOLDER)
        self.ChooseFileDrop.setIcon(FIF.SEND)


        self.LastSeenFill()


    def LastSeenFill(self):
        self.lastSeen = cfg.get(cfg.lastViewTest)

        menu = RoundMenu(parent=self)
        menu.setMaxVisibleItems(4)
        for filePath in self.lastSeen:
            action = Action(FIF.DOCUMENT, filePath)
            action.triggered.connect(self.showCustomDialog)
            action.triggered.connect(lambda _=None, button=action: self.createNewTestInterface(_, button))
            # action.triggered.connect(self.showCustomDialog)

            menu.addAction(action)

        self.ChooseFileDrop.setMenu(menu)

    def showCustomDialog(self):
        if not self.name:
            w = CustomMessageBox(self.window())
            if w.exec():
                self.name = w.userNameEdit.text()
                newCompleterNames = cfg.get(cfg.userHistory)
                if isinstance(newCompleterNames, list):
                    if self.name in newCompleterNames:
                        newCompleterNames.remove(self.name)
                newCompleterNames.insert(0, self.name)
                cfg.set(cfg.userHistory, newCompleterNames)
                cfg.save()
    def createNewTestInterface(self, _, button):
        if self.name:
            if isinstance(button, str):
                filePath = button
            else:
                filePath = button.text()

            for i in self.createdFileInterfaces:
                if i['name'] == filePath:
                    self.refill(filePath)
                    self.parent.switchTo(i['interface'])
                    return

            newTestInterface = TestInterface(self, filePath=filePath, userName=self.name)
            newTestInterface.setObjectName(filePath)
            self.addInterfaceToSuperview(newTestInterface, filePath)
            self.parent.switchTo(newTestInterface)
            self.createdFileInterfaces.append({
                'name': filePath,
                'interface': newTestInterface
            })
            self.refill(filePath)

    def addInterfaceToSuperview(self, newInterface, filePath):
        self.parent.stackedWidget.addWidget(newInterface)
        self.parent.addNewSubInterface(icon=FIF.DOCUMENT, name=filePath, interface=newInterface)

    def ChooseFileButtonAction(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseCustomDirectoryIcons
        filePath, _ = QFileDialog.getOpenFileName(self, "Testify", "",
                                                  "Тест Testify (*.tstf)", options=options)
        if filePath:
            self.loadQuiz(filePath)

    def loadQuiz(self, filePath):
        self.refill(filePath)
        self.showCustomDialog()
        self.createNewTestInterface(None, filePath)

    def refill(self, filePath):
        lastSeen = cfg.get(cfg.lastViewTest)
        if isinstance(lastSeen, list):
            if filePath in lastSeen:
                lastSeen.remove(filePath)
            lastSeen.insert(0, filePath)  # Вставляем filePath в начало списка
            cfg.set(cfg.lastViewTest, lastSeen)
            cfg.save()
            self.LastSeenFill()

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 50))
        shadowEffect.setBlurRadius(50)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
