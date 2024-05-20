import inspect
import json
from enum import Enum

from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QFileDialog
from cryptography.fernet import Fernet
from qfluentwidgets import FluentIcon
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (LineEdit, RadioButton, CheckBox)

from .Ui_TestInterface import Ui_TestInterface
from .components.crypto import QuizCrypto
from .components.customBoxBase import NotifyBox
from .components.tools import TimerManager, time_to_seconds


def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

class TestInterface(Ui_TestInterface, QWidget):

    def __init__(self, parent=None, filePath=None, userName=None, data=None):
        self.parent = parent
        parent.parent.alertMessage = f'Вы уверены что хотите выйти до завершения теста?'
        super().__init__(parent=parent)
        self.setupUi(self)
        self.data = data

        self.testNameLabel.setText(filePath)
        self.userNameLabel.setText(userName)

        self.testIcon.setIcon(FIF.DICTIONARY)
        self.timeIcon.setIcon(FIF.DATE_TIME)
        self.userNameIcon.setIcon(FIF.PEOPLE)
        self.prevButton.setIcon(FIF.LEFT_ARROW)
        self.nextButton.setIcon(FIF.RIGHT_ARROW)
        self.endButton.setText('Завершить тест')
        self.saveButton.setText('Сохранить ответ')


        ########################################
        self.QuizWidget = QuizWidget()

        quiz_title = self.data.get('quiz_title')
        self.testNameLabel.setText(quiz_title)
        total_time_minutes = self.data.get('timeSec', 3600) / 60

        self.questions = []
        for q_data in self.data.get('questions', []):
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
        self.switchToPage(widgetName='quizPage')
        # self.QuizWidget = QuizWidget()
        # self.QuizWidget.setup(questions=self.questions, totalTimeMin=1, ui=self)

    def showResult(self):
        # newTestInterface = z(self.parent, self.questions)
        # newTestInterface.setObjectName('z')
        # widget = newTestInterface
        # self.bottomCard.deleteLater()
        # self.bodyCard.layout().addWidget(widget)
        self.genResultPage()
        self.switchToPage(widgetName='resultPage')

    def getLimits(self):
        self.showAnswers = self.data.get('showAnswers', True)
        self.showAnswersLaterSec = self.data.get('showAnswersLaterSec', 5)

        self.secondTrySec = self.data.get('secondTrySec', 60)

        self.gradePolicy = self.data.get('gradePolicy')
        self.gradeLaterSec = self.data.get('gradeLaterSec', self.showAnswersLaterSec)
        self.gradeShowPercent = self.data.get('gradeShowPercent', True)

    def saveButtonCallback(self):
        correctAnswers = self.getCorrectInt()
        total = self.data.get('total_questions')
        mistakeAnswers = total - correctAnswers
        grade = self.getGrade(correctAnswers, self.data.get('total_questions'))
        manifest = {
            'user': self.userNameLabel.text(),
            'totalQuestions': total,
            'correctAnswers': correctAnswers,
            'mistakeAnswers': mistakeAnswers,
            'grade': grade
        }
        manifest_json = json.dumps(manifest, ensure_ascii=False, indent=4)

        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить результат", self.userNameLabel.text(),
                                                  "TestifyResult Extension(*.tstr)")
        if fileName:
            with open(fileName, 'w') as f:
                f.write(str(manifest_json))

            self.parent.parent.alertMessage = None


    def genResultPage(self):
        self.parent.parent.alertMessage = f'Вы уверены что хотите выйти без сохранения результата?'
        self.headerTitleIcon.setIcon(FIF.EDUCATION)
        self.headerTitleLabel.setText('Тест завершен')

        self.getLimits()

        self.totalIcon.setIcon(FIF.MENU)
        self.totalLabel.setText('Всего вопросов')
        self.totalSubLabel.setText(str(self.data.get('total_questions')))

        self.correctIcon.setIcon(FIF.ADD)
        self.correctLabel.setText('Правильных ответов')
        self.misstakeIcon.setIcon(FIF.REMOVE)
        self.misstakeLabel.setText('Ошибок')
        self.gradeIcon.setIcon(FIF.ACCEPT)
        self.gradeLabel.setText('Ваша оценка')

        self.openTableIcon.setIcon(FluentIcon.TILES)
        self.openTableGoIcon.setIcon(FluentIcon.CHEVRON_RIGHT)
        self.SaveToFileButton.clicked.connect(self.saveButtonCallback)
        if self.showAnswers:
            self.timer = TimerManager(self.showAnswersLaterSec / 60, self.updateTimeLabel, self.hideTableLater)
            self.timer.start_timer()
        else:
            self.openTableLaterLabel.deleteLater()

        self.openTable.clicked.connect(self.handleOpenTable)

        if self.gradeLaterSec:
            self.correctTimer = TimerManager(self.gradeLaterSec / 60, self.updateCorrectLabel, self.countGrade)
            self.correctTimer.start_timer()

            self.mistakeTimer = TimerManager(self.gradeLaterSec / 60, self.updateMisstakeLabel, self.countGrade)
            self.mistakeTimer.start_timer()

            self.gradeTimer = TimerManager(self.gradeLaterSec / 60, self.updateGradeLabel, self.countGrade)
            self.gradeTimer.start_timer()
        else:
            self.countGrade()

    def setShadowEffect(self, card: QWidget, color: QColor):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(color)
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)

    def countGrade(self):
        correctAnswers = self.getCorrectInt()
        total = self.data.get('total_questions')
        mistakeAnswers = total - correctAnswers
        grade = self.getGrade(correctAnswers, self.data.get('total_questions'))
        self.correctSubSabel.setText(str(correctAnswers))
        self.misstakeSubLabel.setText(str(mistakeAnswers))
        if self.gradeShowPercent:
            text = f'{grade} ({(correctAnswers / total) * 100}%)'
        else:
            text = str(grade)
        self.gradeSubLabel.setText(text)
        TableHandler(self.TableWidget, self.questions)
        self.backButton.clicked.connect(lambda _=None, widgetName='resultPage': self.switchToPage(_, widgetName))

        self.setShadowEffect(self.misstakeIcon, QColor(255, 0, 0, 255))
        self.setShadowEffect(self.correctIcon, QColor(0, 255, 0, 255))
        self.setShadowEffect(self.totalIcon, QColor(0, 0, 255, 255))
        if (correctAnswers / total) * 100 >= 90:
            self.setShadowEffect(self.gradeIcon, QColor(0, 255, 0, 255))
        elif (correctAnswers / total) * 100 >= 50:
            self.setShadowEffect(self.gradeIcon, QColor(255, 250, 205, 255))
        else:
            self.setShadowEffect(self.gradeIcon, QColor(255, 0, 0, 255))

    def getGrade(self, correct, total):
        percentage = (correct / total) * 100

        for grade, required_percentage in self.gradePolicy:
            if percentage >= required_percentage:
                return grade
            print(self.gradePolicy[-1][0], percentage)
        return self.gradePolicy[-1][0]
    def updateCorrectLabel(self, time):
        self.correctSubSabel.setText(time.toString("hh:mm:ss"))

    def updateMisstakeLabel(self, time):
        self.misstakeSubLabel.setText(time.toString("hh:mm:ss"))
    def updateGradeLabel(self, time):
        self.gradeSubLabel.setText(time.toString("hh:mm:ss"))

    def handleOpenTable(self):
        if self.showAnswers:
            timer = time_to_seconds(self.openTableLaterLabel.text())
            if timer == 0:
                self.switchToPage(widgetName='tablePage')
            else:
                self.showAnswersFreezedDialog(self, title='Подождите', message=f'Ваши ответы будут доступны через {timer} секунд.')
        else:
            self.showAnswersFreezedDialog(self, title='Ответы скрыты', message=f'Создатель теста отключил доступ к таблице.')


    def hideTableLater(self):
        self.openTableLaterLabel.setHidden(True)

    def updateTimeLabel(self, time):
        self.openTableLaterLabel.setText(time.toString("hh:mm:ss"))

    def switchToPage(self, _=None, widgetName=None):
        if widgetName:
            widget = self.findChild(QWidget, widgetName)
            self.stackedWidget.setCurrentWidget(widget)
        else:
            print(f'Undefined widgetName {widgetName}')

    def showAnswersFreezedDialog(self, _, title, message):
        w = NotifyBox(self.window(), title, message)
        if w.exec():
            print('ok')

    def getCorrectInt(self):
        correct = 0
        for question in self.questions:
            if question.check_answer():
                correct += 1
        return correct

class TableHandler:
    def __init__(self, tableWidget, questions):
        tableWidget.verticalHeader().hide()
        tableWidget.setBorderRadius(5)
        tableWidget.setBorderVisible(True)

        labels = [
            '№', 'Вопрос', 'Правильный ответ', 'Ваш ответ'
        ]
        tableWidget.setColumnCount(len(labels))
        tableWidget.setRowCount(len(questions))
        tableWidget.setHorizontalHeaderLabels(labels)


        questionsRef = []
        for question in questions:
            questionRef = [questions.index(question)+1, question.title, question.correct_answer, question.temp_user_answer_selected]
            questionsRef.append(questionRef)

        for i, question in enumerate(questionsRef):
            for j, item_value in enumerate(question):
                if isinstance(item_value, list):
                    item_value = ', '.join(map(str, item_value))
                else:
                    item_value = str(item_value)
                item = QTableWidgetItem(item_value)
                tableWidget.setItem(i, j, item)

        tableWidget.resizeColumnsToContents()
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
            self.timerManager = TimerManager(totalTimeMin, self.updateTimeLabel, self.setEnded)
            self.ended = False
            self.onStartup()

    def setEnded(self):
        self.ended = True
        self.ui.nextButton.setHidden(True)
        self.ui.prevButton.setHidden(True)
        self.ui.endButton.setHidden(True)
        w = NotifyBox(self.ui.window(), 'Время вышло', 'У вас есть время ответить на последний вопрос.\n(Все неподтверждённые ответы были сохранены)')
        w.exec()

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
        else:
            self.endButtonCall()

    def endButtonCall(self):
        self.timerManager.stop_timer()
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