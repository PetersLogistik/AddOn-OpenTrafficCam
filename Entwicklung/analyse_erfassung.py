import sys, os
import re
from datetime import datetime
from mainUi_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QMainWindow

class Ui_Erfassung(QMainWindow, Ui_MainWindow):
    # https://doc.qt.io/
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.addButton.clicked.connect(self.ordnerAuswahl)
        self.reloadButton.clicked.connect(self.resetTime)
        self.startButton.clicked.connect(self.makeCSV)

        # Staus anzeigen.
        self.statusBar().showMessage("Bereit")

    def disableAll(self):
        self.addButton.setDisabled(True)
        self.renameBox.setDisabled(True)
        self.reloadButton.setDisabled(True)
        self.tableWidget.setDisabled(True)
        self.vidoezeitBox.setDisabled(True)
        self.oneVideoBox.setDisabled(True)
        self.trackBox.setDisabled(True)
        self.detectBox.setDisabled(True)
        self.rErgBox.setDisabled(True)
        self.excelBox.setDisabled(True)
        self.startButton.setDisabled(True)

    def enableAll(self):
        self.addButton.setDisabled(False)
        self.renameBox.setDisabled(False)
        self.reloadButton.setDisabled(False)
        self.tableWidget.setDisabled(False)
        self.vidoezeitBox.setDisabled(False)
        self.oneVideoBox.setDisabled(False)
        self.trackBox.setDisabled(False)
        self.detectBox.setDisabled(False)
        self.rErgBox.setDisabled(False)
        self.excelBox.setDisabled(False)
        self.startButton.setDisabled(False)

    def ordnerAuswahl(self):
        """
            Diese Funktion liest alle Videos in einem Ordner, der vom Nutzer bestimmt wurde, aus und gibt die Videos in der Tabelle an.
        """
        extensions = [".mp4", ".MP4", ".avi",".mkv",".mov"]
        try: # Null-Fehler abfangen.
            directory = QFileDialog.getExistingDirectory(self, "Ordner wählen", "")
        except FileNotFoundError as e:
            print(f"Fehler: Pfad nicht gefunden - {e}")
        except Exception as e:
            print(f"Anderer Fehler: {e}")
        else:
            # dateien, _ = QFileDialog.getOpenFileNames(self, "Dateien öffnen", "", "Alle Dateien (*);;Python-Dateien (*.py)")
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            files.sort()

            for file in files: # für jede Datei im Ordner
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions: # Prüfe auf mp4 Video Datei -> True
                    file_path = os.path.join(directory, file)
                    # Uhrzeit des Vidoes
                    date = str(self.extrahiere_datum(file))

                    # Neue Zeile am Ende hinzufügen
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowPosition)

                    # Item erstellen und einfügen
                    self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(date))
                    self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(file))
                    self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(file_path))
    
    def extrahiere_datum(self, dateiname):
        """
            Diese Funktion ermittelt bei den Videos eine Uhrzeit und gibt diese zurück.
        """
        # Muster für "video_2026-02-24_07-00-27.mp4"
        muster = r"video_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})"
        
        treffer = re.search(muster, dateiname)
        if treffer:
            jahr, monat, tag, stunde, minute, sekunde = treffer.groups()
            datum = datetime(int(jahr), int(monat), int(tag), int(stunde), int(minute), int(sekunde))
            return datum
        try:
            timestamp = os.path.getmtime(dateiname)
            return datetime.fromtimestamp(timestamp)
        except:
            return None
        
    def get_input(self):
        """
            Hierin wird der Ablauf bestimmt, der stattfindet, wenn auf Start gedrückt wird.
        """
        self.disableAll
        if self.oneVideoBox.isChecked() is True:
            pass
        self.makeCSV()
        # self.detectBox.isChecked()
        # self.trackBox.isChecked()
        if self.rErgBox.isChecked() is True:
            pass
        if self.excelBox.isChecked() is True:
            pass
        self.enableAll
    
    def resetTime(self):
        """
            Wenn keine Uhrzeit angegeben ist, dann soll eine Zeit eingegeben werden. Diese Funktion führt errechnet die folgezeiten für alle leeren Zeitkästen & bennet die Dateien um.
        """
        self.disableAll
        table = self.tableWidget
        item = table.item(0, 0)
        # for row in range(1,table.rowCount()-1):
        #     self.tableWidget.setItem(row, 0, QTableWidgetItem(date))
        self.enableAll

    def get_table_data(self, table):
        """
            Diese Funktion liest alle items aus der Tabelle in der GUI aus.
        """
        daten = []
        for row in range(table.rowCount()):
            zeile = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                zeile.append(item.text() if item else "")
            daten.append(zeile)
        return daten

    def makeCSV(self):
        """
            Diese Funktion erzeuget eine CSV-Datei, die der Detect und Track-Funktion übergeben wird. Anhand dieser kann OTC ausgefürht werden.
        """
        daten = self.get_table_data(self.tableWidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_Erfassung()
    window.show()

    sys.exit(app.exec())