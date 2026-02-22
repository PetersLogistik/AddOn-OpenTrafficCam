import sys
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QFileDialog, QTableView, QApplication, QFrame, QDateTimeEdit, QHBoxLayout, QHeaderView, QMainWindow, QMenuBar, QProgressBar, QPushButton, QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMainWindow)

class Ui_Erfassung(QWidget):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 271, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # Button - Add
        self.pushButton1 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton1.setObjectName(u"Add")
        self.pushButton1.clicked.connect(self.onOpen)
        self.horizontalLayout.addWidget(self.pushButton1)
        # Button - Time
        self.pushButton2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton2.setObjectName(u"time")
        self.pushButton2.setDisabled(True)
        self.horizontalLayout.addWidget(self.pushButton2)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 30, 250, 200))
        
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 230, 801, 31))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 300, 256, 192))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # def __init__(self):
    #     super().__init__()
    #     self.initUI()

    # def initUI(self):
    #     layout = QVBoxLayout()
    #     layout_Serien = QHBoxLayout(self.layout)
    #     self.openButton = QPushButton("Ordner hinzufügen")
    #     layout_Serien.addWidget(self.openButton)
    #     self.openButton.clicked.connect(self.onOpen)

    #     self.openButton2 = QPushButton("Uhrzeit und Datum ändern")
    #     layout_Serien.addWidget(self.openButton2)
    #     # self.openButton2.clicked.connect(self.onOpen)

    #     self.listWidget = QListWidget()
    #     layout.addWidget(self.listWidget)
        
        

    #     self.setLayout(layout)
    #     self.setWindowTitle("Dateipfade anzeigen")
    #     self.resize(400, 300)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton1.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.pushButton2.setText(QCoreApplication.translate("MainWindow", u"Zeit", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Zeit", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Zeiten", None));

    def onOpen(self):
        ordner = QFileDialog.getExistingDirectory(self)
        # self.listWidget.addItem(ordner)
        self.tableView.setItem(0,0, ordner)
        self.tableView.show()
        

if __name__ == '__main__':
    import main
    main()