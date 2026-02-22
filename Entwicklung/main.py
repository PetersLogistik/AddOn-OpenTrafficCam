import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from analyse_erfassung import Ui_Erfassung


app = QApplication(sys.argv)

window = QMainWindow()
ui = Ui_Erfassung()
ui.setupUi(window)
window.show()

# window = Ui_Erfassung()
# window.show()

sys.exit(app.exec())
