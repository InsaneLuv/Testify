from PyQt5.QtCore import QTime, Qt
from PyQt5.QtWidgets import QCompleter, QHBoxLayout
from qfluentwidgets import (SubtitleLabel, BodyLabel, MessageBoxBase, SearchLineEdit, TimePicker, FluentIcon, LineEdit,
                            Slider)
from app.common.config import cfg
from .tools import TimerManager, time_to_seconds



class NotifyBox(MessageBoxBase):
    def __init__(self, parent, title=None, message=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.viewLayout.addWidget(self.titleLabel)
        self.subLabel = BodyLabel(message, self)
        self.viewLayout.addWidget(self.subLabel)

        self.yesButton.setText(self.tr('Я понял'))
        self.yesButton.setShortcut("Return")

        self.cancelButton.setHidden(True)


class TestChangeTimeBox(MessageBoxBase):
    def __init__(self, parent, label=None):
        super().__init__(parent)
        self.oldTime = '0'
        self.newTime = self.oldTime
        self.titleLabel = SubtitleLabel('Изменить время', self)
        self.viewLayout.addWidget(self.titleLabel)

        self.TimePicker = TimePicker(self)
        self.TimePicker.setTime(QTime(0, 0, 0))
        self.TimePicker.setSecondVisible(True)
        if label:
            total_seconds = time_to_seconds(label.text())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            self.TimePicker.setTime(QTime(hours, minutes, seconds))
        self.viewLayout.addWidget(self.TimePicker)

        self.subLabel = BodyLabel('Выберите время в формате: hh:mm:ss', self)
        self.viewLayout.addWidget(self.subLabel)

        self.yesButton.setText(self.tr('Применить'))
        self.yesButton.setShortcut("Return")
        self.cancelButton.setText(self.tr('Назад'))
        self.cancelButton.setShortcut("Esc")


class UserNameBox(MessageBoxBase):
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
        self.yesButton.setIcon(FluentIcon.PLAY)
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


class TestRenameTestBox(MessageBoxBase):
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


class TestGradeSettingsBox(MessageBoxBase):
    def __init__(self, parent=None, gradePolicy=None):
        super().__init__(parent)
        self.viewLayout.addWidget(SubtitleLabel('Настроить баллы', self))
        self.gradePolicy = []
        if gradePolicy:
            for i in gradePolicy:
                self.gradeLayout = QHBoxLayout()
                self.subLabel = BodyLabel(str(i[0]), self)
                self.subLabel.setFixedWidth(15)
                self.subLabel.setAlignment(Qt.AlignVCenter)

                self.slider = Slider(self)
                self.subLabelPercentage = LineEdit(self)
                self.slider.valueChanged.connect(
                    lambda value, lineEdit=self.subLabelPercentage: self.updateLineEditFromSlider(value, lineEdit)
                )
                self.slider.setOrientation(Qt.Horizontal)
                self.slider.setFixedWidth(200)
                self.slider.setMaximum(100)
                self.slider.setValue(int(i[1]))

                self.subLabelPercentage.textChanged.connect(
                    lambda text, slider=self.slider: self.updateSliderFromLineEdit(text, slider)
                )
                self.subLabelPercentage.setFixedWidth(50)
                self.subLabelPercentage.setMaxLength(3)
                self.subLabelPercentage.setAlignment(Qt.AlignHCenter)
                self.subLabelPercentage.setText(str(int(i[1])))

                self.gradeLayout.addWidget(self.subLabel)
                self.gradeLayout.addWidget(self.slider)
                self.gradeLayout.addWidget(self.subLabelPercentage)
                self.viewLayout.addLayout(self.gradeLayout)
                self.gradePolicy.append((self.subLabel, self.subLabelPercentage))

        self.subLabel = BodyLabel('Какой процент правильных ответов для получения оценки', self)
        self.viewLayout.addWidget(self.subLabel)

    @staticmethod
    def updateLineEditFromSlider(value, lineEdit):
        lineEdit.blockSignals(True)
        lineEdit.setText(f'{value}')
        lineEdit.blockSignals(False)

    @staticmethod
    def updateSliderFromLineEdit(text, slider):
        try:
            value = int(text)
            if 0 <= value <= 100:
                slider.setValue(value)
        except ValueError:
            pass


class ExitConfirmMessageBox(MessageBoxBase):
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
