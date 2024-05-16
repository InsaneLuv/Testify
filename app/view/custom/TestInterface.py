# coding:utf-8
import json
import os
from random import randint
from enum import Enum
import inspect
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon, setFont, InfoBarIcon, PushButton, MessageBox, NavigationItemPosition, setTheme, \
    RoundMenu, TabItem, SubtitleLabel, IconWidget
from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAction, QGridLayout, QFrame, QSpacerItem, QSizePolicy
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TogglePushButton, ToggleToolButton, TransparentPushButton, TransparentToolButton,
                            TransparentToggleToolButton, TransparentTogglePushButton, TransparentDropDownToolButton,
                            PillPushButton, PillToolButton, setCustomStyleSheet,
                            CustomStyleSheet, LineEdit, RadioButton, CheckBox, BodyLabel, TitleLabel)
from qfluentwidgets import FluentIcon as FIF

from .ResultInterface import ResultInterface
from .Ui_TestInterface import Ui_TestInterface


class TestInterface(Ui_TestInterface, QWidget):

    def __init__(self, parent=None, filePath=None, userName=None):
        self.parent = parent
        super().__init__(parent=parent)
        self.setupUi(self)

        self.testNameLabel.setText(filePath)
        self.userNameLabel.setText(userName)

        self.testIcon.setIcon(FIF.DICTIONARY)
        self.timeIcon.setIcon(FIF.DATE_TIME)
        self.userNameIcon.setIcon(FIF.PEOPLE)
        self.prevButton.setIcon(FIF.CARE_LEFT_SOLID)
        self.nextButton.setIcon(FIF.CARE_RIGHT_SOLID)
        self.endButton.setText('Завершить тест')
        self.saveButton.setText('Сохранить ответ')


        ########################################
        self.QuizWidget = QuizWidget()
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        quiz_title = data.get('quiz_title')
        self.testNameLabel.setText(quiz_title)
        total_time_minutes = 15

        self.questions = []
        for q_data in data.get('questions', []):
            title = q_data.get('title')
            mode = q_data.get('mode')
            variants = q_data.get('variants', [])
            # Создание списка правильных ответов
            correct_answer = [v['text'] for v in variants if v.get('is_checked')]
            question = Question(
                title=title,
                description='This is a sample choose question.',
                mode=mode,
                variants=variants,
                correct_answer=correct_answer
            )
            self.questions.append(question)

        self.QuizWidget.setup(
            ui=self,
            questions=self.questions,
            totalTimeMin=total_time_minutes
        )
        self.QuizWidget.started = True
        self.ProgressBar.setMaximum(len(self.questions))

        # self.QuizWidget = QuizWidget()
        # self.QuizWidget.setup(questions=self.questions, totalTimeMin=1, ui=self)

    def showResult(self):
        newTestInterface = ResultInterface(self.parent, self.questions)
        newTestInterface.setObjectName('ResultInterface')
        widget = newTestInterface
        self.bottomCard.deleteLater()
        self.bodyCard.layout().addWidget(widget)




class QuizWidget:
    def __init__(self):
        self.timerManager = None
        self.QuizManager = None
        self.ui = None
        self.started = False
        self.ended = False

    def setup(self, questions, totalTimeMin, ui):
        if not self.started:
            self.ui = ui
            self.QuizManager = QuizManager(questions)
            self.timerManager = TimerManager(totalTimeMin, self.updateTimeLabel)
            self.ended = False
            self.onStartup()

    def updateTimeLabel(self, time):
        self.ui.timeLabel.setText(time.toString("hh:mm:ss"))

    def onStartup(self):
        self.ui.timeLabel.setText("00:00:00")
        self.QuizManager.select_question()
        self.resetQuestion()
        self.setupButtonCallbacks()
        self.timerManager.start_timer()

    def setupButtonCallbacks(self):
        self.ui.endButton.clicked.connect(self.endButtonCall)
        self.ui.saveButton.setShortcut('Esc')

        self.ui.saveButton.clicked.connect(self.saveButtonCall)
        self.ui.saveButton.setShortcut('Return')

        self.ui.nextButton.clicked.connect(lambda _=None, direction='next': self.navButtonCall(_, direction))
        self.ui.nextButton.setShortcut('right')

        self.ui.prevButton.clicked.connect(lambda _=None, direction='prev': self.navButtonCall(_, direction))
        self.ui.prevButton.setShortcut('left')

    def setRemain(self):
        self.ui.ProgressBar.setValue(self.ui.ProgressBar.value() + 1)
        if self.ui.ProgressBar.value() == len(self.QuizManager.questions):
            self.finishQuiz()

    def finishQuiz(self):
        self.endButtonCall()


    def saveButtonCall(self):
        self.setRemain()
        self.QuizManager.selected_question.submitted = True
        self.QuizManager.selected_question.user_answer = self.QuizManager.selected_question.temp_user_answer_selected
        if not self.ended:
            self.navButtonCall(None, 'next')

    def endButtonCall(self):
        self.clear_layout(self.ui.bodyCard.layout())
        self.clear_layout(self.ui.verticalLayout.layout())
        self.timerManager.stop_timer()
        self.ui.bottomCard.setEnabled(False)
        self.ui.showResult()

    def navButtonCall(self, _, direction):
        self.QuizManager.scroll_question(direction)
        self.resetQuestion()

    def resetQuestion(self):
        self.ui.questionTitleLabel.setText(self.QuizManager.selected_question.title)
        self.setupAnswers()


    def setupAnswers(self):
        answer_box = self.ui.answerBox
        self.clear_layout(answer_box.layout())
        self.answer_widgets = []
        question = self.QuizManager.selected_question

        if question.mode == 'input':
            input_lineedit = LineEdit()
            input_lineedit.setPlaceholderText("Введите ответ")
            input_lineedit.textChanged.connect(self.handleAnswerChanged)
            answer_box.layout().addWidget(input_lineedit)
            self.answer_widgets.append(input_lineedit)

        if question.mode == 'choose_one':
            for variant in question.variants:
                print(variant)
                radio_button = RadioButton(variant['text'])
                radio_button.setShortcut(QKeySequence(str(question.variants.index(variant) + 1)))
                radio_button.clicked.connect(self.handleAnswerChanged)
                answer_box.layout().addWidget(radio_button)
                self.answer_widgets.append(radio_button)

        if question.mode == 'choose':
            for variant in question.variants:
                checkbox = CheckBox(variant['text'])
                checkbox.setShortcut(QKeySequence(str(question.variants.index(variant) + 1)))
                checkbox.clicked.connect(self.handleAnswerChanged)
                answer_box.layout().addWidget(checkbox)
                self.answer_widgets.append(checkbox)

        self.keepChosen()

    def handleAnswerChanged(self):
        user_answer = None
        question = self.QuizManager.selected_question

        if question.mode == 'input':
            user_answer = self.answer_widgets[0].text()

        elif question.mode == 'choose_one':
            for widget in self.answer_widgets:
                if widget.isChecked():
                    user_answer = widget.text()

        elif question.mode == 'choose':
            user_answer = []
            for widget in self.answer_widgets:
                if widget.isChecked():
                    user_answer.append(widget.text())
            question.user_answer = user_answer

        if question.temp_user_answer_selected != user_answer:
            question.set_temp_user_answer_selected(user_answer)

        self.ui.saveButton.setEnabled(bool(user_answer))

    def keepChosen(self):
        question = self.QuizManager.selected_question
        if question.temp_user_answer_selected:
            if question.mode == 'input':
                self.answer_widgets[0].setText(question.temp_user_answer_selected)

            if question.mode == 'choose_one':
                for widget in self.answer_widgets:
                    if widget.text() == question.temp_user_answer_selected:
                        widget.setChecked(True)

            if question.mode == 'choose':
                for widget in self.answer_widgets:
                    if widget.text() in question.temp_user_answer_selected:
                        widget.setChecked(True)

        self.ui.saveButton.setEnabled(bool(question.temp_user_answer_selected))

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                spacer = item.spacerItem()
                if spacer:
                    layout.removeItem(spacer)

    # def get_grade(self):
    #     grade = []
    #     for question in self.QuizManager.questions:
    #         i = [self.QuizManager.questions.index(question)+1, question.title, question.check_answer(), question.correct_answer, question.user_answer]
    #         grade.append(i)
    #     return grade


class QuestionModes(Enum):
    CHOOSE = 'choose'
    CHOOSE_ONE = 'choose_one'
    INPUT = 'input'


class Question:
    def __init__(self, title, description=None, mode=None, variants=None, correct_answer=None, threshold_similarity=0.4,
                 threshold_length_diff=2):
        self.title = title
        self.description = description
        self.mode = mode
        self.variants = variants
        self.correct_answer = correct_answer

        self.threshold_similarity = threshold_similarity
        self.threshold_length_diff = threshold_length_diff

        self.temp_user_answer_selected = None

        self.user_answer = None

        self.submitted = False

        self.user_properly = None

    def fill_not_submitted(self):
        if not self.submitted:
            self.submitted = True

    def set_temp_user_answer_selected(self, selected):
        caller_frame = inspect.currentframe().f_back
        caller_func_name = caller_frame.f_code.co_name
        print(f'Caller {caller_func_name} = {selected}')
        self.temp_user_answer_selected = selected
        self.user_properly = self.check_answer()

    def check_answer(self):
        if not self.user_answer:
            if self.temp_user_answer_selected:
                self.user_answer = self.temp_user_answer_selected
            else:
                return False

        if self.mode == 'input':

            return self.user_answer.lower() == self.correct_answer[0].lower()

        elif self.mode == 'choose_one':

            return self.user_answer in self.correct_answer

        elif self.mode == 'choose':
            print(self.user_answer, self.correct_answer)
            return self.user_answer == self.correct_answer


class TimerManager:
    def __init__(self, total_time_minutes, update_callback):
        self.total_time_seconds = total_time_minutes * 60
        self.elapsed_time_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.update_callback = update_callback

    def start_timer(self):
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        self.elapsed_time_seconds += 1
        remaining_time = self.calculate_remaining_time()
        self.update_callback(remaining_time)

        if remaining_time == QTime(0, 0):
            self.timer.stop()

    def calculate_remaining_time(self):
        remaining_time_seconds = max(0, int(self.total_time_seconds) - self.elapsed_time_seconds)
        remaining_time = QTime(0, 0).addSecs(remaining_time_seconds)
        return remaining_time

class QuizManager:
    def __init__(self, questions):
        self.questions = questions
        self.selected_question = None
        self.selected_question_index = 0

    def select_question(self):
        for index, question in enumerate(self.questions):
            if not question.submitted:
                self.selected_question = question
                self.selected_question_index = index
                return question

    def scroll_question(self, mode):
        direction = 1 if mode == 'next' else -1
        original_index = self.selected_question_index
        while True:
            self.selected_question_index = (self.selected_question_index + direction) % len(self.questions)
            if self.selected_question_index == original_index:
                break
            if not self.questions[self.selected_question_index].submitted:
                self.selected_question = self.questions[self.selected_question_index]
                return self.selected_question

    def get_unsubmitted(self):
        return [question for question in self.questions if not question.submitted]

    def get_grade(self):
        grade = []
        for question in self.questions:
            i = [self.questions.index(question), question.title, question.check_answer(), question.correct_answer, question.user_answer]
            grade.append(i)