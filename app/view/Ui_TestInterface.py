# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\app\view\ui\TestInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TestInterface(object):
    def setupUi(self, TestInterface):
        TestInterface.setObjectName("TestInterface")
        TestInterface.resize(1008, 677)
        self.verticalLayout = QtWidgets.QVBoxLayout(TestInterface)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll = SmoothScrollArea(TestInterface)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll.sizePolicy().hasHeightForWidth())
        self.scroll.setSizePolicy(sizePolicy)
        self.scroll.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.scroll.setAcceptDrops(True)
        self.scroll.setStyleSheet("background-color: transparent;\n"
"border: 0;")
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.bodyCard = QtWidgets.QWidget()
        self.bodyCard.setGeometry(QtCore.QRect(0, 0, 1008, 677))
        self.bodyCard.setAutoFillBackground(False)
        self.bodyCard.setObjectName("bodyCard")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.bodyCard)
        self.verticalLayout_6.setContentsMargins(36, 36, 36, 36)
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.header = QtWidgets.QHBoxLayout()
        self.header.setSpacing(4)
        self.header.setObjectName("header")
        self.testIcon = IconWidget(self.bodyCard)
        self.testIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.testIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.testIcon.setObjectName("testIcon")
        self.header.addWidget(self.testIcon)
        self.testNameLabel = CaptionLabel(self.bodyCard)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.testNameLabel.setFont(font)
        self.testNameLabel.setObjectName("testNameLabel")
        self.header.addWidget(self.testNameLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header.addItem(spacerItem)
        self.ss_2 = CardWidget(self.bodyCard)
        self.ss_2.setObjectName("ss_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.ss_2)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.userNameIcon = IconWidget(self.ss_2)
        self.userNameIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.userNameIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.userNameIcon.setObjectName("userNameIcon")
        self.horizontalLayout_4.addWidget(self.userNameIcon)
        self.userNameLabel = BodyLabel(self.ss_2)
        self.userNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.userNameLabel.setObjectName("userNameLabel")
        self.horizontalLayout_4.addWidget(self.userNameLabel)
        self.header.addWidget(self.ss_2)
        self.ss = CardWidget(self.bodyCard)
        self.ss.setObjectName("ss")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ss)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timeIcon = IconWidget(self.ss)
        self.timeIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.timeIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.timeIcon.setObjectName("timeIcon")
        self.horizontalLayout_3.addWidget(self.timeIcon)
        self.timeLabel = BodyLabel(self.ss)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setMinimumSize(QtCore.QSize(65, 0))
        self.timeLabel.setMaximumSize(QtCore.QSize(65, 16777215))
        self.timeLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout_3.addWidget(self.timeLabel)
        self.header.addWidget(self.ss)
        self.verticalLayout_6.addLayout(self.header)
        self.stackedWidget = QtWidgets.QStackedWidget(self.bodyCard)
        self.stackedWidget.setObjectName("stackedWidget")
        self.quizPage = QtWidgets.QWidget()
        self.quizPage.setObjectName("quizPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.quizPage)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.questionTitleLabel = TextEdit(self.quizPage)
        self.questionTitleLabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.questionTitleLabel.sizePolicy().hasHeightForWidth())
        self.questionTitleLabel.setSizePolicy(sizePolicy)
        self.questionTitleLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.questionTitleLabel.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.questionTitleLabel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.questionTitleLabel.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.questionTitleLabel.setDocumentTitle("")
        self.questionTitleLabel.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.questionTitleLabel.setReadOnly(True)
        self.questionTitleLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.questionTitleLabel.setObjectName("questionTitleLabel")
        self.verticalLayout_2.addWidget(self.questionTitleLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.answerBox = QtWidgets.QVBoxLayout()
        self.answerBox.setSpacing(4)
        self.answerBox.setObjectName("answerBox")
        self.LineEdit = LineEdit(self.quizPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit.sizePolicy().hasHeightForWidth())
        self.LineEdit.setSizePolicy(sizePolicy)
        self.LineEdit.setDragEnabled(False)
        self.LineEdit.setObjectName("LineEdit")
        self.answerBox.addWidget(self.LineEdit)
        self.RadioButton = RadioButton(self.quizPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RadioButton.sizePolicy().hasHeightForWidth())
        self.RadioButton.setSizePolicy(sizePolicy)
        self.RadioButton.setObjectName("RadioButton")
        self.answerBox.addWidget(self.RadioButton)
        self.CheckBox = CheckBox(self.quizPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CheckBox.sizePolicy().hasHeightForWidth())
        self.CheckBox.setSizePolicy(sizePolicy)
        self.CheckBox.setObjectName("CheckBox")
        self.answerBox.addWidget(self.CheckBox)
        self.verticalLayout_2.addLayout(self.answerBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.saveButton = PushButton(self.quizPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setMinimumSize(QtCore.QSize(0, 0))
        self.saveButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.saveButton.setObjectName("saveButton")
        self.gridLayout_2.addWidget(self.saveButton, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(51, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.prevButton = ToolButton(self.quizPage)
        self.prevButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.prevButton.setAutoRaise(False)
        self.prevButton.setObjectName("prevButton")
        self.horizontalLayout_2.addWidget(self.prevButton)
        self.nextButton = ToolButton(self.quizPage)
        self.nextButton.setText("")
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout_2.addWidget(self.nextButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 4, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.endButton = PushButton(self.quizPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endButton.sizePolicy().hasHeightForWidth())
        self.endButton.setSizePolicy(sizePolicy)
        self.endButton.setMinimumSize(QtCore.QSize(0, 0))
        self.endButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.endButton.setObjectName("endButton")
        self.horizontalLayout_5.addWidget(self.endButton)
        spacerItem4 = QtWidgets.QSpacerItem(51, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.ProgressBar = ProgressBar(self.quizPage)
        self.ProgressBar.setMinimumSize(QtCore.QSize(0, 4))
        self.ProgressBar.setMaximumSize(QtCore.QSize(16777215, 4))
        self.ProgressBar.setObjectName("ProgressBar")
        self.verticalLayout_2.addWidget(self.ProgressBar)
        self.stackedWidget.addWidget(self.quizPage)
        self.resultPage = QtWidgets.QWidget()
        self.resultPage.setObjectName("resultPage")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.resultPage)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(4)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.HeaderCard = SimpleCardWidget(self.resultPage)
        self.HeaderCard.setObjectName("HeaderCard")
        self.gridLayout = QtWidgets.QGridLayout(self.HeaderCard)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 0, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.headerTitleIcon = IconWidget(self.HeaderCard)
        self.headerTitleIcon.setMinimumSize(QtCore.QSize(40, 40))
        self.headerTitleIcon.setMaximumSize(QtCore.QSize(40, 40))
        self.headerTitleIcon.setObjectName("headerTitleIcon")
        self.horizontalLayout.addWidget(self.headerTitleIcon)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.headerTitleLabel = TitleLabel(self.HeaderCard)
        self.headerTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerTitleLabel.setObjectName("headerTitleLabel")
        self.verticalLayout_3.addWidget(self.headerTitleLabel)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_15.addWidget(self.HeaderCard)
        self.gradeCard = QtWidgets.QHBoxLayout()
        self.gradeCard.setContentsMargins(-1, -1, 0, -1)
        self.gradeCard.setSpacing(4)
        self.gradeCard.setObjectName("gradeCard")
        self.totalCard = SimpleCardWidget(self.resultPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.totalCard.sizePolicy().hasHeightForWidth())
        self.totalCard.setSizePolicy(sizePolicy)
        self.totalCard.setObjectName("totalCard")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.totalCard)
        self.verticalLayout_19.setSpacing(4)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.layout_2 = QtWidgets.QHBoxLayout()
        self.layout_2.setSpacing(4)
        self.layout_2.setObjectName("layout_2")
        self.totalIcon = IconWidget(self.totalCard)
        self.totalIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.totalIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.totalIcon.setObjectName("totalIcon")
        self.layout_2.addWidget(self.totalIcon)
        self.verticalLayout_19.addLayout(self.layout_2)
        self.totalLabel = StrongBodyLabel(self.totalCard)
        self.totalLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.totalLabel.setObjectName("totalLabel")
        self.verticalLayout_19.addWidget(self.totalLabel)
        self.totalSubLabel = BodyLabel(self.totalCard)
        self.totalSubLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.totalSubLabel.setProperty("darkColor", QtGui.QColor(255, 255, 255, 150))
        self.totalSubLabel.setObjectName("totalSubLabel")
        self.verticalLayout_19.addWidget(self.totalSubLabel)
        self.gradeCard.addWidget(self.totalCard)
        self.correctCard = SimpleCardWidget(self.resultPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.correctCard.sizePolicy().hasHeightForWidth())
        self.correctCard.setSizePolicy(sizePolicy)
        self.correctCard.setObjectName("correctCard")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.correctCard)
        self.verticalLayout_18.setSpacing(4)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.layout_3 = QtWidgets.QHBoxLayout()
        self.layout_3.setSpacing(4)
        self.layout_3.setObjectName("layout_3")
        self.correctIcon = IconWidget(self.correctCard)
        self.correctIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.correctIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.correctIcon.setObjectName("correctIcon")
        self.layout_3.addWidget(self.correctIcon)
        self.verticalLayout_18.addLayout(self.layout_3)
        self.correctLabel = StrongBodyLabel(self.correctCard)
        self.correctLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.correctLabel.setObjectName("correctLabel")
        self.verticalLayout_18.addWidget(self.correctLabel)
        self.correctSubSabel = BodyLabel(self.correctCard)
        self.correctSubSabel.setAlignment(QtCore.Qt.AlignCenter)
        self.correctSubSabel.setProperty("darkColor", QtGui.QColor(255, 255, 255, 150))
        self.correctSubSabel.setObjectName("correctSubSabel")
        self.verticalLayout_18.addWidget(self.correctSubSabel)
        self.gradeCard.addWidget(self.correctCard)
        self.misstakeCard = SimpleCardWidget(self.resultPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.misstakeCard.sizePolicy().hasHeightForWidth())
        self.misstakeCard.setSizePolicy(sizePolicy)
        self.misstakeCard.setObjectName("misstakeCard")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.misstakeCard)
        self.verticalLayout_14.setSpacing(4)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setSpacing(4)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.misstakeIcon = IconWidget(self.misstakeCard)
        self.misstakeIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.misstakeIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.misstakeIcon.setObjectName("misstakeIcon")
        self.horizontalLayout_16.addWidget(self.misstakeIcon)
        self.verticalLayout_14.addLayout(self.horizontalLayout_16)
        self.misstakeLabel = StrongBodyLabel(self.misstakeCard)
        self.misstakeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.misstakeLabel.setObjectName("misstakeLabel")
        self.verticalLayout_14.addWidget(self.misstakeLabel)
        self.misstakeSubLabel = BodyLabel(self.misstakeCard)
        self.misstakeSubLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.misstakeSubLabel.setProperty("darkColor", QtGui.QColor(255, 255, 255, 150))
        self.misstakeSubLabel.setObjectName("misstakeSubLabel")
        self.verticalLayout_14.addWidget(self.misstakeSubLabel)
        self.gradeCard.addWidget(self.misstakeCard)
        self.SimpleCardWidget = SimpleCardWidget(self.resultPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SimpleCardWidget.sizePolicy().hasHeightForWidth())
        self.SimpleCardWidget.setSizePolicy(sizePolicy)
        self.SimpleCardWidget.setObjectName("SimpleCardWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.SimpleCardWidget)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.layout_4 = QtWidgets.QHBoxLayout()
        self.layout_4.setSpacing(4)
        self.layout_4.setObjectName("layout_4")
        self.gradeIcon = IconWidget(self.SimpleCardWidget)
        self.gradeIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.gradeIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.gradeIcon.setObjectName("gradeIcon")
        self.layout_4.addWidget(self.gradeIcon)
        self.verticalLayout_4.addLayout(self.layout_4)
        self.gradeLabel = StrongBodyLabel(self.SimpleCardWidget)
        self.gradeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gradeLabel.setObjectName("gradeLabel")
        self.verticalLayout_4.addWidget(self.gradeLabel)
        self.gradeSubLabel = BodyLabel(self.SimpleCardWidget)
        self.gradeSubLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gradeSubLabel.setProperty("darkColor", QtGui.QColor(255, 255, 255, 150))
        self.gradeSubLabel.setObjectName("gradeSubLabel")
        self.verticalLayout_4.addWidget(self.gradeSubLabel)
        self.gradeCard.addWidget(self.SimpleCardWidget)
        self.verticalLayout_15.addLayout(self.gradeCard)
        self.openTable = CardWidget(self.resultPage)
        self.openTable.setObjectName("openTable")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.openTable)
        self.horizontalLayout_19.setContentsMargins(14, 14, 14, 14)
        self.horizontalLayout_19.setSpacing(4)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(6, -1, 6, -1)
        self.layout.setObjectName("layout")
        self.openTableIcon = IconWidget(self.openTable)
        self.openTableIcon.setMinimumSize(QtCore.QSize(20, 20))
        self.openTableIcon.setMaximumSize(QtCore.QSize(20, 20))
        self.openTableIcon.setAcceptDrops(False)
        self.openTableIcon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.openTableIcon.setObjectName("openTableIcon")
        self.layout.addWidget(self.openTableIcon)
        self.horizontalLayout_19.addLayout(self.layout)
        self.layout_5 = QtWidgets.QVBoxLayout()
        self.layout_5.setSpacing(0)
        self.layout_5.setObjectName("layout_5")
        self.openTableLabel = StrongBodyLabel(self.openTable)
        self.openTableLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.openTableLabel.setObjectName("openTableLabel")
        self.layout_5.addWidget(self.openTableLabel)
        self.openTableSubLabel = BodyLabel(self.openTable)
        self.openTableSubLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.openTableSubLabel.setProperty("lightColor", QtGui.QColor(0, 0, 0, 150))
        self.openTableSubLabel.setProperty("darkColor", QtGui.QColor(255, 255, 255, 150))
        self.openTableSubLabel.setObjectName("openTableSubLabel")
        self.layout_5.addWidget(self.openTableSubLabel)
        self.horizontalLayout_19.addLayout(self.layout_5)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem7)
        self.layout_6 = QtWidgets.QHBoxLayout()
        self.layout_6.setContentsMargins(6, -1, 6, -1)
        self.layout_6.setSpacing(4)
        self.layout_6.setObjectName("layout_6")
        self.openTableLaterLabel = HyperlinkLabel(self.openTable)
        self.openTableLaterLabel.setObjectName("openTableLaterLabel")
        self.layout_6.addWidget(self.openTableLaterLabel)
        self.openTableGoIcon = IconWidget(self.openTable)
        self.openTableGoIcon.setMinimumSize(QtCore.QSize(16, 16))
        self.openTableGoIcon.setMaximumSize(QtCore.QSize(16, 16))
        self.openTableGoIcon.setAcceptDrops(False)
        self.openTableGoIcon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.openTableGoIcon.setObjectName("openTableGoIcon")
        self.layout_6.addWidget(self.openTableGoIcon)
        self.horizontalLayout_19.addLayout(self.layout_6)
        self.verticalLayout_15.addWidget(self.openTable)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_15.addItem(spacerItem8)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setSpacing(4)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.SaveToFileButton = PrimaryPushButton(self.resultPage)
        self.SaveToFileButton.setObjectName("SaveToFileButton")
        self.horizontalLayout_21.addWidget(self.SaveToFileButton)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem9)
        self.verticalLayout_15.addLayout(self.horizontalLayout_21)
        self.stackedWidget.addWidget(self.resultPage)
        self.tablePage = QtWidgets.QWidget()
        self.tablePage.setObjectName("tablePage")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tablePage)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.TableWidget = TableWidget(self.tablePage)
        self.TableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TableWidget.setTabKeyNavigation(False)
        self.TableWidget.setProperty("showDropIndicator", False)
        self.TableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.TableWidget.setCornerButtonEnabled(False)
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setColumnCount(0)
        self.TableWidget.setRowCount(0)
        self.TableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.TableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_5.addWidget(self.TableWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem10)
        self.backButton = PushButton(self.tablePage)
        self.backButton.setObjectName("backButton")
        self.horizontalLayout_6.addWidget(self.backButton)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.stackedWidget.addWidget(self.tablePage)
        self.verticalLayout_6.addWidget(self.stackedWidget)
        self.scroll.setWidget(self.bodyCard)
        self.verticalLayout.addWidget(self.scroll)

        self.retranslateUi(TestInterface)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(TestInterface)

    def retranslateUi(self, TestInterface):
        _translate = QtCore.QCoreApplication.translate
        TestInterface.setWindowTitle(_translate("TestInterface", "Form"))
        self.testNameLabel.setText(_translate("TestInterface", "testNameLabel"))
        self.userNameLabel.setText(_translate("TestInterface", "NAME"))
        self.timeLabel.setText(_translate("TestInterface", "44:44:44"))
        self.questionTitleLabel.setHtml(_translate("TestInterface", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\',\'Microsoft YaHei\',\'PingFang SC\',\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">123</span></p></body></html>"))
        self.LineEdit.setText(_translate("TestInterface", "test"))
        self.LineEdit.setPlaceholderText(_translate("TestInterface", "OTVER"))
        self.RadioButton.setText(_translate("TestInterface", "Radio button"))
        self.CheckBox.setText(_translate("TestInterface", "Check box"))
        self.saveButton.setText(_translate("TestInterface", "save"))
        self.endButton.setText(_translate("TestInterface", "END TEST"))
        self.headerTitleLabel.setText(_translate("TestInterface", "PLACEHOLDER"))
        self.totalLabel.setText(_translate("TestInterface", "..."))
        self.totalSubLabel.setText(_translate("TestInterface", "..."))
        self.correctLabel.setText(_translate("TestInterface", "..."))
        self.correctSubSabel.setText(_translate("TestInterface", "..."))
        self.misstakeLabel.setText(_translate("TestInterface", "..."))
        self.misstakeSubLabel.setText(_translate("TestInterface", "..."))
        self.gradeLabel.setText(_translate("TestInterface", "..."))
        self.gradeSubLabel.setText(_translate("TestInterface", "..."))
        self.openTableLabel.setText(_translate("TestInterface", "Посмотреть ответы"))
        self.openTableSubLabel.setText(_translate("TestInterface", "Таблица с вашими и правильными ответами"))
        self.openTableLaterLabel.setText(_translate("TestInterface", "00:00:00"))
        self.SaveToFileButton.setText(_translate("TestInterface", "Сохранить результат"))
        self.backButton.setText(_translate("TestInterface", "Назад"))
from qfluentwidgets import BodyLabel, CaptionLabel, CardWidget, CheckBox, HyperlinkLabel, IconWidget, LineEdit, PrimaryPushButton, ProgressBar, PushButton, RadioButton, SimpleCardWidget, SmoothScrollArea, StrongBodyLabel, TableWidget, TextEdit, TitleLabel, ToolButton


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TestInterface = QtWidgets.CardWidget()
    ui = Ui_TestInterface()
    ui.setupUi(TestInterface)
    TestInterface.show()
    sys.exit(app.exec_())
