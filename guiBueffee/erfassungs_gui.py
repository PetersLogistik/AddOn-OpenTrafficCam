import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QFileDialog, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        # MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(393, 600)
        MainWindow.setWindowTitle("Erfassung OTC-Videoanalyse")
        MainWindow.setWindowIcon(QIcon(r".\AddOn-OpenTrafficCam\Entwicklung\bueffee_mailfuss.png"))

        self.centralwidget = QWidget(MainWindow)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(10, 14, 371, 561))

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QHBoxLayout()
    # Add Button
        self.addButton = QPushButton(self.verticalLayoutWidget)
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Hinzuf\u00fcgen", None))
        self.horizontalLayout_3.addWidget(self.addButton)
        self.addButton.clicked.connect(self.ordnerAuswahl)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout_3)
    # Table
        self.tableWidget = QTableWidget(self.verticalLayoutWidget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)
    # Check-Box
        self.oneVideoBox = QCheckBox(self.verticalLayoutWidget)
        self.oneVideoBox.setText(u"Video mit Zeitstempel versehen")
        self.verticalLayout.addWidget(self.oneVideoBox)
    # Linie
        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
    # Check-Box
        self.detectBox = QCheckBox(self.verticalLayoutWidget)
        self.detectBox.setText(QCoreApplication.translate("MainWindow", u"DETECT durchlaufen", None))
        self.horizontalLayout_2.addWidget(self.detectBox)

        self.trackBox = QCheckBox(self.verticalLayoutWidget)
        self.trackBox.setText(QCoreApplication.translate("MainWindow", u"TRACK durchlaufen", None))
        self.horizontalLayout_2.addWidget(self.trackBox)
        
        self.verticalLayout.addLayout(self.horizontalLayout_2)
    # Linie
        self.line2 = QFrame(self.verticalLayoutWidget)
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout.addWidget(self.line2)
    # Check-Box
        self.horizontalLayout = QHBoxLayout()
        self.rErgBox = QCheckBox(self.verticalLayoutWidget)
        self.rErgBox.setText(u"R Ergebnisdarstellung")
        self.horizontalLayout.addWidget(self.rErgBox)

        self.excelBox = QCheckBox(self.verticalLayoutWidget)
        self.excelBox.setText(u"Excel Ergebnistabelle")
        self.horizontalLayout.addWidget(self.excelBox)

        self.verticalLayout.addLayout(self.horizontalLayout)
    # Linie
        self.line3 = QFrame(self.verticalLayoutWidget)
        self.line3.setFrameShape(QFrame.Shape.HLine)
        self.line3.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout.addWidget(self.line3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)
    # start Button
        self.startButton = QPushButton(self.verticalLayoutWidget)
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.horizontalLayout_4.addWidget(self.startButton)
        # self.startButton.clicked.connect()

        self.verticalLayout.addLayout(self.horizontalLayout_4)
    # Bar
        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.verticalLayout.addWidget(self.progressBar)
    # Statusbar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Zeit", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Pfad", None));
    # retranslateUi

    @QtCore.Slot()
    def ordnerAuswahl(self):
        ordner = QFileDialog.getExistingDirectory(self, "Ordner wählen")
        if ordner:
            self.listWidget.addItem(ordner)
        # self.tableWidget.setItem(0,0, ordner)
        # self.tableWidget.show()
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())