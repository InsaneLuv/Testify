# coding:utf-8
import os
import random
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import QColor, QKeySequence, QIcon
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QCompleter, QTableWidget
from qfluentwidgets import FluentIcon, setFont, InfoBarIcon, PushButton, MessageBox, NavigationItemPosition, setTheme, \
    RoundMenu, TabBar, MSFluentTitleBar, MessageBoxBase, SearchLineEdit
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAction, QGridLayout, QTableWidgetItem
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TogglePushButton, ToggleToolButton, TransparentPushButton, TransparentToolButton,
                            TransparentToggleToolButton, TransparentTogglePushButton, TransparentDropDownToolButton,
                            TransparentDropDownPushButton, PillPushButton, PillToolButton, setCustomStyleSheet,
                            CustomStyleSheet, SubtitleLabel, LineEdit, CaptionLabel, TableWidget)
from qfluentwidgets import FluentIcon as FIF

from .Ui_ResultInterface import Ui_ResultInterface
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Theme, Action
from ...common.config import cfg
from ...common.icon import Icon
from ...common.style_sheet import StyleSheet


class ResultInterface(Ui_ResultInterface, QWidget):
    def __init__(self, parent=None, questions=None):
        self.parent = parent
        super().__init__(parent=parent)
        self.setupUi(self)
        self.questions = questions

        self.headerTitleIcon.setIcon(FIF.EDUCATION)
        self.headerTitleLabel.setText('Тест завершен')

        self.totalIcon.setIcon(FIF.MENU)
        self.totalTitleLabel.setText('Всего вопросов')
        self.totalNumberLabel.setText(str(len(self.questions)))

        self.correctIcon.setIcon(FIF.ADD)
        self.correctTitleLabel.setText('Правильных ответов')
        self.correctInt = self.getCorrectInt()
        self.correctNumberLabel.setText(str(self.correctInt))


        self.missIcon.setIcon(FIF.REMOVE)
        self.missTitleLabel.setText('Ошибок')
        self.missNumberLabel.setText(f'{len(self.questions) - self.correctInt}')

        self.gradeIcon.setIcon(FIF.ACCEPT)
        self.gradeInt = self.getGradeInt(correct=self.correctInt, total=len(self.questions))
        self.gradeTitleLabel.setText('Ваша оценка')
        self.gradeNumberLabel.setText(str(self.gradeInt))

        self.SaveToFileButton.setText('Сохранить в файл')
        self.SaveToFileButton.setIcon(FIF.SAVE)
        self.SaveToFileButton.setEnabled(False)

        self.CloseButton.setText('Назад')
        self.CloseButton.setEnabled(False)

        TableHandler(self.TableWidget, questions)
        # self.TableWidget.setIt


        # self.TableWidget.setUpdatesEnabled(False)


    def getCorrectInt(self):
        correct = 0
        for question in self.questions:
            if question.check_answer(): correct += 1
        return correct


    def getGradeInt(self, correct, total):
        percentage = (correct / total) * 100

        if percentage >= 90:
            grade = 5
        elif percentage >= 75:
            grade = 4
        elif percentage >= 50:
            grade = 3
        elif percentage >= 25:
            grade = 2
        else:
            grade = 2

        return grade

class TableHandler:
    def __init__(self, tableWidget, questions):
        tableWidget.verticalHeader().hide()
        tableWidget.setBorderRadius(8)
        tableWidget.setBorderVisible(True)

        tableWidget.setColumnCount(5)
        tableWidget.setRowCount(len(questions))
        tableWidget.setHorizontalHeaderLabels([
            '№', 'Вопрос', 'Верно', 'Правильный ответ', 'Ваш ответ'
        ])

        questionsRef = []
        for question in questions:
            questionRef = [questions.index(question)+1, question.title, question.check_answer(), question.correct_answer, question.temp_user_answer_selected]
            questionsRef.append(questionRef)

        for i, question in enumerate(questionsRef):
            for j, item_value in enumerate(question):
                # Проверяем, является ли item_value списком
                if isinstance(item_value, list):
                    # Преобразуем список в строку с элементами, разделенными запятой
                    item_value = ', '.join(map(str, item_value))
                else:
                    item_value = str(item_value)

                # Заменяем значения на текстовые альтернативы
                if item_value == 'None':
                    item_value = 'Нет ответа'
                elif item_value == 'False':
                    item_value = 'Нет'
                elif item_value == 'True':
                    item_value = 'Да'

                # Создаем элемент QTableWidgetItem с обновленным значением
                item = QTableWidgetItem(item_value)
                # Устанавливаем элемент в таблицу
                tableWidget.setItem(i, j, item)

        # Подгоняем размер столбцов
        tableWidget.resizeColumnsToContents()
