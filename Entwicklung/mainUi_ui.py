# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUi.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(481, 620)
        MainWindow.setMinimumSize(QSize(420, 620))
        MainWindow.setWindowTitle(u"Videoerfassung f\u00fcr OTC")
        icon = QIcon()
        icon.addFile(u"bueffee_mailfuss.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowFilePath(u"")
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_1 = QFrame(self.centralwidget)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_1)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.addButton = QPushButton(self.frame_2)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setText(u"Video hinzuf\u00fcgen")

        self.horizontalLayout_2.addWidget(self.addButton)

        self.addCSVButton = QPushButton(self.frame_2)
        self.addCSVButton.setObjectName(u"addCSVButton")
        self.addCSVButton.setText(u"CSV hinzuf\u00fcgen")

        self.horizontalLayout_2.addWidget(self.addCSVButton)

        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.renameBox = QCheckBox(self.frame_2)
        self.renameBox.setObjectName(u"renameBox")
        self.renameBox.setText(u"Videos umbenennen")
        self.renameBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.renameBox)

        self.reloadButton = QPushButton(self.frame_2)
        self.reloadButton.setObjectName(u"reloadButton")
        self.reloadButton.setText(u"\u00dcbernehmen")

        self.horizontalLayout_2.addWidget(self.reloadButton)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.tableWidget = QTableWidget(self.frame_1)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setText(u"Zeit");
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setText(u"Dateiname");
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setText(u"Pfad");
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.frame_3 = QFrame(self.frame_1)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.vidoezeitBox = QCheckBox(self.frame_4)
        self.vidoezeitBox.setObjectName(u"vidoezeitBox")
        self.vidoezeitBox.setText(u"einzel Videos mit Zeitsempel versehen")
        self.vidoezeitBox.setCheckable(False)

        self.horizontalLayout_3.addWidget(self.vidoezeitBox)

        self.oneVideoBox = QCheckBox(self.frame_4)
        self.oneVideoBox.setObjectName(u"oneVideoBox")
        self.oneVideoBox.setText(u"Ein-Zeitstempel-Video erstellen")
        self.oneVideoBox.setCheckable(False)
        self.oneVideoBox.setChecked(False)

        self.horizontalLayout_3.addWidget(self.oneVideoBox)


        self.verticalLayout_3.addWidget(self.frame_4)

        self.line_1 = QFrame(self.frame_3)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_1)

        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.detectBox = QCheckBox(self.frame_5)
        self.detectBox.setObjectName(u"detectBox")
        self.detectBox.setText(u"DETECT durchlaufen")
        self.detectBox.setCheckable(False)

        self.horizontalLayout_6.addWidget(self.detectBox)

        self.trackBox = QCheckBox(self.frame_5)
        self.trackBox.setObjectName(u"trackBox")
        self.trackBox.setText(u"TRACK durchlaufen")
        self.trackBox.setCheckable(False)

        self.horizontalLayout_6.addWidget(self.trackBox)


        self.verticalLayout_3.addWidget(self.frame_5)

        self.frame = QFrame(self.frame_3)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 0))
        self.label.setMaximumSize(QSize(50, 16777215))
        self.label.setText(u"Modell")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label)

        self.modellBox = QComboBox(self.frame)
        self.modellBox.setObjectName(u"modellBox")
        self.modellBox.setEnabled(False)
        self.modellBox.setMinimumSize(QSize(75, 0))
        self.modellBox.setMaximumSize(QSize(16777215, 16777215))
        self.modellBox.setEditable(False)

        self.horizontalLayout_4.addWidget(self.modellBox)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(5, 0))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 0))
        self.label_2.setMaximumSize(QSize(50, 16777215))
        self.label_2.setText(u"conf")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.confSpinBox = QDoubleSpinBox(self.frame)
        self.confSpinBox.setObjectName(u"confSpinBox")
        self.confSpinBox.setEnabled(True)
        self.confSpinBox.setMaximumSize(QSize(60, 16777215))
        self.confSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.confSpinBox.setReadOnly(True)
        self.confSpinBox.setMaximum(1.000000000000000)
        self.confSpinBox.setSingleStep(0.010000000000000)
        self.confSpinBox.setValue(0.250000000000000)

        self.horizontalLayout_4.addWidget(self.confSpinBox)

        self.line_3 = QFrame(self.frame)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_3)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))
        self.label_3.setMaximumSize(QSize(50, 16777215))
        self.label_3.setText(u"iou")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.iouSpinBox = QDoubleSpinBox(self.frame)
        self.iouSpinBox.setObjectName(u"iouSpinBox")
        self.iouSpinBox.setEnabled(True)
        self.iouSpinBox.setMaximumSize(QSize(60, 16777215))
        self.iouSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iouSpinBox.setReadOnly(True)
        self.iouSpinBox.setMaximum(1.000000000000000)
        self.iouSpinBox.setSingleStep(0.010000000000000)
        self.iouSpinBox.setValue(0.450000000000000)

        self.horizontalLayout_4.addWidget(self.iouSpinBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addWidget(self.frame)

        self.line_2 = QFrame(self.frame_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.rErgBox = QCheckBox(self.frame_6)
        self.rErgBox.setObjectName(u"rErgBox")
        self.rErgBox.setText(u"R Ergebnisdarstellung erzeugen")
        self.rErgBox.setCheckable(False)

        self.horizontalLayout_7.addWidget(self.rErgBox)

        self.excelBox = QCheckBox(self.frame_6)
        self.excelBox.setObjectName(u"excelBox")
        self.excelBox.setText(u"Excel Ergebnistabelle erstellen")
        self.excelBox.setCheckable(False)

        self.horizontalLayout_7.addWidget(self.excelBox)


        self.verticalLayout_3.addWidget(self.frame_6)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_7 = QFrame(self.frame_1)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_7)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.resetButton = QPushButton(self.frame_7)
        self.resetButton.setObjectName(u"resetButton")
        font = QFont()
        font.setItalic(True)
        self.resetButton.setFont(font)
        self.resetButton.setAutoFillBackground(False)
        self.resetButton.setText(u"Reset")

        self.horizontalLayout.addWidget(self.resetButton)

        self.horizontalSpacer_3 = QSpacerItem(306, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.startButton = QPushButton(self.frame_7)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setText(u"Start")
        self.startButton.setCheckable(False)

        self.horizontalLayout.addWidget(self.startButton)


        self.verticalLayout_2.addWidget(self.frame_7)

        self.progressBar = QProgressBar(self.frame_1)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setFormat(u"%p%")

        self.verticalLayout_2.addWidget(self.progressBar)


        self.verticalLayout.addWidget(self.frame_1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        pass
    # retranslateUi

