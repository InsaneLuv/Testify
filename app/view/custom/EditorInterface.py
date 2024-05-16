# coding:utf-8
import time
import json
import uuid
from .Ui_EditorInterface import Ui_EditorInterface
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QCompleter
from qfluentwidgets import MessageBoxBase, SearchLineEdit, FluentIcon, TimePicker
from PyQt5.QtCore import Qt, QSize, QPoint, QTime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAction, QGridLayout, QFrame, QHBoxLayout, QSizePolicy, QFileDialog
from qfluentwidgets import SubtitleLabel, LineEdit, PushButton, CheckBox, RadioButton, ComboBox, ScrollArea, ToolButton, SimpleCardWidget
from qfluentwidgets import FluentIcon as FIF
from ...common.config import cfg

def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

class EQuestionHandler:
    def __init__(self, ui):
        self.question_list = []
        self.ui = ui
        self.timer = 0
        self.hideAnswers = False

    def add_question(self):
        question = EQuestion(self)
        question.create_new_question()
        self.question_list.append(question)

        self.ui.questions_container.layout().insertLayout(0, question.soft_frame_layout)

        self.trigger_on_change()

    def save_quiz(self, filename):
        manifest = {
            'questions': []
        }
        for question in self.question_list:
            question_data = {
                "title": question.title if isinstance(question.title, str) else 'Пустой вопрос',
                "mode": question.mode,
                "variants": [
                    {
                        "text": variant.text,
                        "is_checked": variant.is_checked,
                    } for variant in question.variants
                ]
            }
            if question_data['variants']:
                manifest['questions'].append(question_data)

        manifest['quiz_title'] = self.ui.testNameLabel.text()
        manifest['creator_name'] = 'UNSET'
        manifest['created_at'] = time.time()
        manifest['total_questions'] = len(manifest['questions'])
        manifest['time'] = time_to_seconds(self.ui.settingsTimeChangeButton.text())

        fileName, _ = QFileDialog.getSaveFileName(self.ui, "Сохранить тест", self.ui.testNameLabel.text(), "Testify Extension(*.tstf)")
        if fileName:
            with open(fileName, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=4)


    def remove_question(self, question):
        self.question_list.remove(question)
        layout = question.soft_frame_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                layout.removeItem(item)
        question.soft_frame.deleteLater()  # Удаляем сам фрейм
        self.trigger_on_change()

    def trigger_on_change(self):
        print(self.question_list)


class Defaults:
    SOFT_FRAME_HEIGHT = 300
    FOOTER_SCROLL_AREA_HEIGHT = 150

class EQuestion:
    def __init__(self, handler):
        self.handler = handler

        self.soft_frame = None
        self.soft_frame_layout = None

        self.header_frame = None
        self.header_frame_layout = None

        self.footer_frame = None
        self.footer_frame_layout = None

        self.animation_duration = 300
        self.defaults = Defaults()
        self.is_footer_visible = True
        self.combo_items = [
            {
                'text': "Один из списка",
                'mode': 'choose_one'
             },
            {
                'text': "Несколько из списка",
                'mode': 'choose'
            },
            {
                'text': "Текст",
                'mode': 'input'
            }
        ]


        self.title = None
        self.mode = None
        self.variants = []  # List to store variant texts
        # self.correct_answer = []  # List to store correct answer(s)
        # self.variant_widgets = []


    def set_header_callbacks(self):
        self.collapse_button.clicked.connect(self.toggle_footer_visibility)
        self.delete_button.clicked.connect(self.delete_button_action)
        self.combo_box.currentTextChanged.connect(self.mode_changed_action)
        self.title.textChanged.connect(self.title_changed_action)


    def title_changed_action(self, text):
        self.title = str(text)


    def mode_changed_action(self, text):
        for item in self.combo_items:
            if item['text'] == text:
                self.mode = item['mode']
        self.combo_box_onchange_action(text)

    def create_new_question(self, name='QuestionFrame'):
        self.new_soft_frame(name)
        self.set_header_callbacks()

    def new_soft_frame(self, name):
        self.soft_frame = SimpleCardWidget()
        soft_frame_layout = QVBoxLayout()
        self.soft_frame.setObjectName(name)
        self.soft_frame.setMaximumHeight(self.defaults.SOFT_FRAME_HEIGHT)
        self.header_frame = self.new_header_frame(name='Header', combo_items=self.combo_items, soft_frame_layout=soft_frame_layout)
        self.footer_frame = self.new_footer_frame(name='Footer', soft_frame=soft_frame_layout)
        # soft_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.soft_frame_layout = soft_frame_layout

    def new_header_frame(self, name, combo_items, soft_frame_layout):
        header_frame = SimpleCardWidget()
        header_frame.setObjectName(name)
        header_frame_layout = QHBoxLayout(header_frame)

        soft_frame_layout.addWidget(header_frame)

        _input = self.new_input(name='Header_Input', placeholder='Введите вопрос...')
        _combo = self.new_combo(name='Header_Combo', combo_items=combo_items)
        _buttons = self.new_buttons_frame(name='Header_Buttons')

        header_frame_layout.addWidget(_input)
        header_frame_layout.addWidget(_combo)
        header_frame_layout.addWidget(_buttons)
        self.header_frame_layout = header_frame_layout
        return header_frame

    def new_input(self, name, placeholder='PLACEHOLDER'):
        title = LineEdit()
        title.setObjectName(name)
        title.setPlaceholderText(placeholder)
        title.setMinimumSize(200, 0)
        self.title = title
        return title

    def new_combo(self, name, combo_items=None):
        combo_box = NoWheelComboBox()
        combo_box.setObjectName(name)
        combo_box.setMaximumWidth(200)
        if combo_items:
            for idx, item in enumerate(combo_items):
                icon = item.get('icon')
                text = item.get('text')
                if text:
                    combo_box.addItem(text)
                    if icon:
                        combo_box.setItemIcon(idx, icon)
        self.combo_box = combo_box
        return combo_box

    def new_footer_frame(self, name, soft_frame):
        footer_frame = SimpleCardWidget()
        footer_frame.setObjectName(name)
        footer_frame_layout = QVBoxLayout(footer_frame)
        footer_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        footer_frame_layout.setContentsMargins(0, 0, 0, 0)

        footer_scroll_area = self.new_scroll_area('Scroll_Area')
        footer_scroll_area.setWidget(footer_frame)
        self.footer_scroll_area = footer_scroll_area
        self.footer_layout = footer_frame_layout
        self.mode_changed_action(self.combo_items[0]['text'])
        soft_frame.addWidget(footer_scroll_area)
        return footer_frame

    def new_scroll_area(self, name):
        footer_scroll_area = ScrollArea()
        footer_scroll_area.setObjectName(name)
        footer_scroll_area.setWidgetResizable(True)
        footer_scroll_area.setFixedHeight(self.defaults.FOOTER_SCROLL_AREA_HEIGHT)
        return footer_scroll_area

    def new_button(self, icon):
        button = ToolButton()
        button.setIcon(icon)
        button.setMaximumSize(30, 30)
        button.setMinimumSize(30, 30)
        return button

    def new_buttons_frame(self, name):
        button_frame = QFrame()
        button_frame.setObjectName(name)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(6)

        collapse_button = self.new_button(FIF.HIDE)
        delete_button = self.new_button(FIF.DELETE)
        button_layout.addWidget(collapse_button)
        button_layout.addWidget(delete_button)
        self.collapse_button = collapse_button
        self.delete_button = delete_button

        return button_frame

    def remove_variant(self, variant_frame):
        if len(self.variants) > 1:
            input_field = variant_frame.findChild(LineEdit)
            type_button = variant_frame.findChild(RadioButton) or variant_frame.findChild(CheckBox)
            unique_id = None
            for variant in self.variants:
                if variant.text == input_field.text() and variant.is_checked == type_button.isChecked():
                    unique_id = variant.id
                    break
            # Удаление варианта из списка self.variants
            if unique_id:
                self.variants = [v for v in self.variants if v.id != unique_id]
            # Удаление виджета варианта из макета
            variant_frame.deleteLater()
            self.print_variants()

    def set_variant_button_callbacks(self, variant_frame, copy_button, remove_button):
        remove_button.clicked.connect(lambda: self.remove_variant(variant_frame))
        copy_button.clicked.connect(self.copy_button_action)

    def new_variant_buttons_frame(self, name, variant_frame):
        button_frame = QFrame()
        button_frame.setObjectName(name)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(6)
        copy_button = self.new_button(FIF.COPY)
        remove_button = self.new_button(FIF.REMOVE)
        button_layout.addWidget(copy_button)
        button_layout.addWidget(remove_button)
        self.set_variant_button_callbacks(variant_frame, copy_button, remove_button)
        return button_frame

    def get_variant_type(self, str_type):
        if str_type == "Один из списка":
            return RadioButton()
        elif str_type == "Несколько из списка":
            return CheckBox()
        elif str_type == "Текст":
            return LineEdit()

    def new_variant_frame(self, name, str_type):
        variant_frame = QFrame()
        variant_frame.setObjectName(name)
        variant_frame_layout = QHBoxLayout(variant_frame)

        if str_type == "Текст":
            variant_input = LineEdit()
            variant_input.setPlaceholderText(f'Введите правильный ответ...')
            variant_input.setMaximumHeight(33)
            variant_frame_layout.addWidget(variant_input)

            unique_id = str(uuid.uuid4())
            new_variant = Variant(unique_id, "", False)  # По умолчанию is_checked = False для текстового варианта
            self.variants.append(new_variant)

            variant_input.textChanged.connect(
                lambda text: self.variant_updated(unique_id, text, True))  # Для текста не нужно is_checked
        else:
            variant_type = self.get_variant_type(str_type)
            variant_frame_layout.addWidget(variant_type)

            variant_input = LineEdit()
            variant_input.setPlaceholderText(f'Вариант {len(self.variants)+1}')
            variant_input.setMaximumHeight(33)
            variant_frame_layout.addWidget(variant_input)

            button_frame = self.new_variant_buttons_frame(name='Variant_Buttons', variant_frame=variant_frame)
            variant_frame_layout.addWidget(button_frame)

            input_field = variant_frame.findChild(LineEdit)
            type_button = variant_frame.findChild(RadioButton) or variant_frame.findChild(CheckBox)

            unique_id = str(uuid.uuid4())
            new_variant = Variant(unique_id, "", type_button.isChecked())
            self.variants.append(new_variant)

            input_field.textChanged.connect(lambda text: self.variant_updated(unique_id, text, type_button.isChecked()))
            type_button.clicked.connect(lambda checked: self.variant_updated(unique_id, input_field.text(), checked))

        return variant_frame

    def variant_updated(self, unique_id, text, is_checked):
        for variant in self.variants:
            if variant.id == unique_id:
                variant.text = text
                variant.is_checked = is_checked
                break

        self.print_variants()

    def print_variants(self):
        print("--------------/")
        for variant in self.variants:
            print(f"[{variant.id}] - [{variant.is_checked}] - [{variant.text}]")
        print("--------------/")

    def add_variant_frame(self, str_type):
        variant_frame = self.new_variant_frame(name='Variant_Frame', str_type=str_type)
        return variant_frame

    def remove_button_action(self, frame):
        frame.deleteLater()

    def delete_button_action(self):
        self.handler.remove_question(self)
        self.soft_frame_layout.deleteLater()

    def copy_button_action(self):
        variant = self.add_variant_frame(self.current_type)
        if variant:
            self.footer_layout.insertWidget(0, variant)


    def combo_box_onchange_action(self, text):
        self.variants = []
        self.correct_answer = []
        for i in reversed(range(self.footer_layout.count())):
            self.footer_layout.itemAt(i).widget().deleteLater()

        variant = self.add_variant_frame(text)
        self.current_type = text
        if variant:
            self.footer_layout.addWidget(variant)

    def toggle_footer_visibility(self):
        self.is_footer_visible = not self.is_footer_visible

        if not self.is_footer_visible:
            self.footer_scroll_area.setFixedHeight(0)
            self.collapse_button.setIcon(FIF.VIEW)
            self.footer_frame.setVisible(False)
        else:
            self.footer_scroll_area.setFixedHeight(self.defaults.FOOTER_SCROLL_AREA_HEIGHT)
            self.collapse_button.setIcon(FIF.HIDE)
            self.footer_frame.setVisible(True)

class Variant:
    def __init__(self, unique_id, text, is_checked=False):
        self.id = unique_id
        self.text = text
        self.is_checked = is_checked

class NoWheelComboBox(ComboBox):
    def wheelEvent(self, event):
        # Игнорируем событие колеса мыши
        event.ignore()

class EditorInterface(Ui_EditorInterface, QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent=parent)
        self.setObjectName('editorInterface')
        self.setupUi(self)
        self._initInterface()

    def _initInterface(self):
        self.renameWindow = CustomMessageBox(self.window())
        self.headerLabel.setText('Редактор')

        self.saveButtonIcon.setIcon(FluentIcon.SAVE)
        self.saveButton.clicked.connect(self.saveQuiz)

        self.backButtonIcon.setIcon(FluentIcon.LEFT_ARROW)
        self.backButton.clicked.connect(self.goHome)
        self.backButton.setHidden(True)

        self.stackedWidget.setCurrentWidget(self.homePage)
        self.question_handler = EQuestionHandler(self)

        self.addNewButton.clicked.connect(self.rysyProtifYasherov)
        self.addNewButton.setText('Добавить')
        self.addNewButton.setIcon(FIF.ADD)

        self.hideAllButton.clicked.connect(self.jaYstal)
        self.hideAllButton.setText('Скрыть всё')
        self.hideAllButton.setIcon(FIF.REMOVE)

        self.fillHomePage()
        self.fillSettingsQuestionWidget()

    def fillSettingsQuestionWidget(self):
        self.settingsTime.clicked.connect(self.showChangeTimeDialog)
        self.settingsTimeChangeButton.clicked.connect(self.showChangeTimeDialog)
        self.settingsTimeIcon.setIcon(FluentIcon.STOP_WATCH)

        self.settingsPrivacy.clicked.connect(self.privacyChanged)
        self.settingsPrivacyIcon.setIcon(FluentIcon.VIEW)
        self.privacyChanged()

        self.settingsGrade.clicked.connect(self.showChangeTimeDialog)
        self.settingsGradeIcon.setIcon(FluentIcon.UNIT)
        self.settingsGradeGoIcon.setIcon(FluentIcon.CHEVRON_RIGHT)

    def privacyChanged(self):
        if self.question_handler.hideAnswers:
            self.question_handler.hideAnswers = False
            self.settingsPrivacyGoIcon.setIcon(FluentIcon.CLOSE)
        else:
            self.question_handler.hideAnswers = True
            self.settingsPrivacyGoIcon.setIcon(FluentIcon.ACCEPT)

    def showChangeTimeDialog(self):
        w = CustomTimeMessageBox(self.window())
        if w.exec():
            self.settingsTimeChangeButton.setText(w.TimePicker.time.toString("hh:mm:ss"))

    def jaYstal(self):
        for question in self.question_handler.question_list:
            question.is_footer_visible = True
            question.toggle_footer_visibility()

    def rysyProtifYasherov(self):
        self.question_handler.add_question()

    def saveQuiz(self):
        self.question_handler.save_quiz('test.json')

    # ВРЕМЕННЫЙ КЛАСС
    def goHome(self):
        self.backButton.setHidden(True)
        self.stackedWidget.setCurrentWidget(self.homePage)

    def showRenameDialog(self):
        w = CustomMessageBox(self.window(), oldName=self.testNameLabel.text())
        if w.exec(): self.testNameLabel.setText(w.newName)

    def fillHomePage(self):
        self.testNameLabel.setText('Новый тест')
        self.testNameChangeButton.setText('Переименовать')
        self.testNameChangeButton.clicked.connect(self.showRenameDialog)

        self.helpIcon.setIcon(FIF.HELP)
        self.helpLabel.setText('Руководство')
        self.helpButton.setText('Открыть')
        self.helpButton.clicked.connect(self.echo)

        self.moreIcon.setIcon(FIF.CALORIES)
        self.moreLabel.setText('Новые функции')
        self.moreButton.setText('Посмотреть')
        self.moreButton.clicked.connect(self.echo)

        self.editQuestionsIcon.setIcon(FIF.MENU)
        self.editQuestionsLabel.setText('Вопросы')
        self.editQuestionsSubLabel.setText('Добавить/Редактировать вопросы')
        self.editQuestionsGoIcon.setIcon(FIF.CHEVRON_RIGHT)
        self.editQuestions.clicked.connect(lambda _=None, widget=self.editQuestions.objectName(): self.switchToWidget(_, widget))

        self.settingsQuestionIcon.setIcon(FIF.SETTING)
        self.settingsQuestionLabel.setText('Настройки')
        self.settingsQuestionSubLabel.setText('Оценка, доступ, и др.')
        self.settingsQuestionGoIcon.setIcon(FIF.CHEVRON_RIGHT)
        self.settingsQuestion.clicked.connect(lambda _=None, widget=self.settingsQuestion.objectName(): self.switchToWidget(_, widget))
        self.settingsQuestion.setEnabled(True)


    def echo(self):
        print('click')

    def switchToWidget(self, _=None, widget=None):
        self.backButton.setHidden(False)
        widget = self.findChild(QWidget, f'{widget}Widget')
        self.stackedWidget.setCurrentWidget(widget)


    def debug(self):
        self.stackedWidget.setCurrentWidget('widget')

class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None, oldName='Новый тест'):
        super().__init__(parent)
        self.oldName = oldName
        self.newName = self.oldName
        self.titleLabel = SubtitleLabel(self.tr('Переименовать тест'), self)
        self.viewLayout.addWidget(self.titleLabel)

        self.LineEdit = LineEdit(self)
        self.LineEdit.setText(oldName)
        self.LineEdit.setPlaceholderText(self.tr('Название'))
        self.LineEdit.setClearButtonEnabled(True)
        self.LineEdit.setMaxLength(120)
        self.viewLayout.addWidget(self.LineEdit)

        self.yesButton.setText(self.tr('Применить'))
        self.yesButton.setShortcut("Return")
        self.cancelButton.setText(self.tr('Назад'))
        self.cancelButton.setShortcut("Esc")

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)
        self.LineEdit.textChanged.connect(self.ifTextInput)

    def ifTextInput(self, text):
        self.yesButton.setEnabled(bool(text))
        self.newName = text
        if self.newName == self.oldName:
            self.yesButton.setEnabled(False)

class CustomTimeMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent):
        super().__init__(parent)
        self.oldTime = '0'
        self.newTime = self.oldTime
        self.titleLabel = SubtitleLabel(self.tr('Изменить время'), self)
        self.viewLayout.addWidget(self.titleLabel)

        self.TimePicker = TimePicker(self)
        self.TimePicker.setTime(QTime(0, 0, 0))
        self.TimePicker.setSecondVisible(True)
        self.viewLayout.addWidget(self.TimePicker)

        self.yesButton.setText(self.tr('Применить'))
        self.yesButton.setShortcut("Return")
        self.cancelButton.setText(self.tr('Назад'))
        self.cancelButton.setShortcut("Esc")