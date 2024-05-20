# coding:utf-8
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon

from ..common.config import REPO_URL
from ..common.style_sheet import StyleSheet
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('Testify', self)
        self.linkCardView = LinkCardView(self)
        self.galleryLabel.setObjectName('galleryLabel')
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('GitHub'),
            self.tr(
                'Исходный код программы на странице проекта github.'),
            REPO_URL
        )
        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            self.tr('Telegram'),
            self.tr(
                'Вы можете написать разработчику в Telegram.'),
            REPO_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()
        gradient = QLinearGradient(0, 0, 0, h)
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 70))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 70))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
        painter.fillPath(path, QBrush(gradient))


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(4)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        basicInputView = SampleCardView(self.tr("Новости обновления 1.1"), self.view)
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Border.png",
            title="Улучшение редактора",
            content="Оцените новые интересные функции \nредактора.",
            routeKey="editorInterface",
            index=1
        )
        self.vBoxLayout.addWidget(basicInputView)

        basicInputView = SampleCardView(self.tr("Новости обновления 1.0"), self.view)
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/InfoBadge.png",
            title="Новый интерфейс",
            content=self.tr(
                "Переход с пакета pydracula к pyfluentwidgets. Теперь интерфейс имеет стиль Windows 11."),
            routeKey="basicInputInterface",
            index=0
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/RichEditBox.png",
            title="Редактор тестов",
            content=self.tr("Удобный и красивый интерфейс редактора уже доступен!"),
            routeKey="basicInputInterface",
            index=8
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Flyout.png",
            title="Пройти тест",
            content=self.tr(
                "Вы уже можете пройти тест, созданный в Testify."),
            routeKey="developInterface",
            index=10
        )
        self.vBoxLayout.addWidget(basicInputView)