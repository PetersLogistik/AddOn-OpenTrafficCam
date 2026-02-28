# -*- coding: utf-8 -*- 
import sys, os, time
import verarbeitung.video_verarbeitung as vid
from mainUi_ui import Ui_MainWindow
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMainWindow, QMessageBox, QPushButton

class Ui_Erfassung(QMainWindow, Ui_MainWindow):
    # https://doc.qt.io/
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.addButton.clicked.connect(self.ordnerEingabe)
        self.addCSVButton.clicked.connect(self.aktivCSV)
        self.reloadButton.clicked.connect(self.bestaetigen)
        self.resetButton.clicked.connect(self.reset)
        self.startButton.clicked.connect(self.get_input)

        self.reset_aktiv = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_button)
        
        # Spalten automatisch anpassen
        self.tableWidget.resizeColumnsToContents()
        
        # Standart-Werte laden
        self.modellBox.addItems(["yolo11m", "yolov8m"])
        self.confSpinBox.setValue(0.25)
        self.iouSpinBox.setValue(0.45)
        # Staus anzeigen
        self.statusBar().showMessage("Bereit")
        
        # Alle Pfade sichern 
        self.mainpfad = []

    def bestaetigen(self):
        """
            Fragt nach, ob auch die Videos umbenannt werden sollen oder nur die Zeit in der Tabelle angezeigt werden soll.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Frage")
        msg.setIcon(QMessageBox.Question)

        if self.renameBox.isChecked():
            msg.setText("Beachte alle Zeiten werden in der Tabelle überschrieben.\n\nMöchten Sie die Titel der Videos umbenenen? \nDabei wird der Zeitstempel dem Videotitel hinzugefügt.")
        else:
            msg.setText("Beachte alle Zeiten werden in der Tabelle überschrieben.")

        # Deutsche Buttons erstellen
        bt_ja = QPushButton("Ja")
        bt_clt = QPushButton("Abbrechen")

        # Buttons hinzufügen
        msg.addButton(bt_ja, QMessageBox.ActionRole)
        msg.addButton(bt_clt, QMessageBox.RejectRole)
        msg.setDefaultButton(bt_ja)

        # Dialog anzeigen
        msg.exec()

        if msg.clickedButton() == bt_ja and self.renameBox.isChecked:
            self.reload_Time()
        elif msg.clickedButton() == bt_ja and self.renameBox.isChecked is False:
            self.reload_Time(False)

    def disableAll(self):
        """
            Sperrt alle Klick-Elemente
        """
        self.addButton.setDisabled(True)
        self.addCSVButton.setDisabled(True)
        self.renameBox.setDisabled(True)
        self.reloadButton.setDisabled(True)
        self.tableWidget.setDisabled(True)
        self.vidoezeitBox.setDisabled(True)
        self.oneVideoBox.setDisabled(True)
        self.trackBox.setDisabled(True)
        self.detectBox.setDisabled(True)
        self.modellBox.setDisabled(True)
        self.confSpinBox.setDisabled(True)
        self.iouSpinBox.setDisabled(True)
        self.rErgBox.setDisabled(True)
        self.excelBox.setDisabled(True)
        self.startButton.setDisabled(True)

    def enableAll(self):
        """
            Entsperrt alle Klick-Elemente 
        """
        self.addButton.setDisabled(False)
        self.addCSVButton.setDisabled(False)
        self.renameBox.setDisabled(False)
        self.reloadButton.setDisabled(False)
        self.tableWidget.setDisabled(False)
        self.vidoezeitBox.setDisabled(False)
        self.oneVideoBox.setDisabled(False)
        self.trackBox.setDisabled(False)
        self.detectBox.setDisabled(False)
        self.modellBox.setDisabled(False)
        self.confSpinBox.setDisabled(False)
        self.iouSpinBox.setDisabled(False)
        self.rErgBox.setDisabled(False)
        self.excelBox.setDisabled(False)
        self.startButton.setDisabled(False)

    def aktivVideo(self):
        """
            Reduzeirt die Auswahl, wenn Videos barbeitet werden.
        """
        # Enable
        self.vidoezeitBox.setCheckable(True)
        self.oneVideoBox.setCheckable(True)
        self.trackBox.setCheckable(True)
        self.detectBox.setCheckable(True)
        self.modellBox.setEnabled(False)
        self.confSpinBox.setReadOnly(False)
        self.iouSpinBox.setReadOnly(False)
        # Check
        self.trackBox.setChecked(True)
        self.detectBox.setChecked(True)
        # Disable
        self.addCSVButton.setDisabled(True)
        self.rErgBox.setDisabled(True)
        self.excelBox.setDisabled(True) 

    def aktivCSV(self):
        """
            Reduziet die Auswahl, wenn CSV bearbeitet werden.
        """
        # Enable
        self.rErgBox.setCheckable(True)
        self.excelBox.setCheckable(True)
        # Disable
        self.addButton.setDisabled(True)
        self.renameBox.setDisabled(True)
        self.reloadButton.setDisabled(True)
        self.vidoezeitBox.setDisabled(True)
        self.oneVideoBox.setDisabled(True)
        self.trackBox.setDisabled(True)
        self.detectBox.setDisabled(True)
    
    def bereit(self) -> None:
        self.tableWidget.resizeColumnsToContents()
        self.statusBar().showMessage("Bereit")
        self.progressBar.setValue(0)
        
    def reset(self):
        if self.reset_aktiv:
            self.reset_button()
            self.enableAll()
            # Checked
            self.renameBox.setChecked(True)
            # Non-Checked
            self.trackBox.setChecked(False)
            self.detectBox.setChecked(False)
            # Disable
            self.rErgBox.setCheckable(False)
            self.excelBox.setCheckable(False)
            self.vidoezeitBox.setCheckable(False)
            self.oneVideoBox.setCheckable(False)
            self.trackBox.setCheckable(False)
            self.detectBox.setCheckable(False)
            self.loeche_Zeileneintaege()
            self.modellBox.setEnabled(False)
            self.modellBox.setCurrentIndex(0)
            self.confSpinBox.setReadOnly(True)
            self.confSpinBox.setValue(0.25)
            self.iouSpinBox.setReadOnly(True)
            self.iouSpinBox.setValue(0.45)
        else:
            self.reset_aktiv = True
            self.resetButton.setStyleSheet("background-color: red;")
            self.timer.start(10000)
            self.statusBar().showMessage("Rest bitte bestätigen.", 10000)
    
    def reset_button(self):
        # Button zurücksetzen
        self.reset_aktiv = False
        self.resetButton.setStyleSheet("") 
        self.bereit()

    def start_timer(self):
        time.sleep(30)
        self.reset_count=0

    def loeche_Zeileneintaege(self):
        """
            löscht alle Zeilen
        """
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        QApplication.processEvents()
        self.bereit()

    def ordnerEingabe(self) -> None:
        """
            Durch den Nutzer gestartet und läd einen ordner, anschließend wird der Pfad an ordnerAuswahl übergeben.
        """
        directory = QFileDialog.getExistingDirectory(self, "Ordner wählen", "")
        self.mainpfad.append(directory)
        self.ordnerAuswahl(directory)

    def ordnerAuswahl(self, directory) -> None:
        """
            Diese Funktion liest alle Videos in einem Ordner, der vom Nutzer bestimmt wurde, aus und gibt die Videos in der Tabelle an.
        """
        self.aktivVideo()
        self.statusBar().showMessage("Dateien laden")
        extensions = [".mp4", ".MP4", ".avi",".mkv",".mov"]

        if directory:
            # dateien, _ = QFileDialog.getOpenFileNames(self, "Dateien öffnen", "", "Alle Dateien (*);;Python-Dateien (*.py)")
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            files.sort()
            count = False
            
            for file in files: # für jede Datei im Ordner
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions: # Prüfe auf Video Datei -> True
                    count = True
                    file_path = os.path.abspath(os.path.join(directory, file))

                    # Uhrzeit des Vidoes
                    date = str(vid.extrahiere_datum(file))

                    # Neue Zeile am Ende hinzufügen
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowPosition)

                    # Item erstellen und einfügen
                    self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(date))
                    self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(file))
                    self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(file_path))
            
            if count is False:
                QMessageBox.information(self, "Hinweis", f"Es sind keine Videos im Ordner \n{directory} \nvorhanden.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Warnung", f"Es wurde kein Pfad ausgewählt oder eingegeben. \nBitte Wiederholen Sie die Eingabe.", QMessageBox.Ok, QMessageBox.Ok)
        self.bereit()

    def make_onevideo(self):
        self.statusBar().showMessage("Es wird ein Video zusammengeschnitten")
        
        for mpfad in self.mainpfad:
            zeit = self.tableWidget.item(0, 0).text()
            pfad, zeit = vid.one_video(mpfad, zeit)
            
            self.statusBar().showMessage("Das Video wird mit einem Zeitstempel versehen")
            vid.make_video_overlay(pfad, zeit)
        
        self.bereit()

    def videozeit_in_video(self):
        videos = self.get_table_data()
        self.statusBar().showMessage("In die Vidos wird die Zeit geschrieben")
        
        for round, video in enumerate(videos,start=1):
            self.progressBar.setValue((len(videos))/(round))
            
            path = video[2]
            zeit = video[0]
            vid.make_video_overlay(path, zeit)
            
            self.bereit()


    def get_input(self):
        """
            Hierin wird der Ablauf bestimmt, der stattfindet, wenn auf Start gedrückt wird.
        """
        self.disableAll()
        if self.oneVideoBox.isChecked():
            self.make_onevideo()
        if self.vidoezeitBox.isChecked():
            self.videozeit_in_video()

        # self.makeCSV()
        # # self.detectBox.isChecked()
        # # self.trackBox.isChecked()
        # if self.rErgBox.isChecked():
        #     pass
        # if self.excelBox.isChecked():
        #     pass
        self.enableAll()

    def reload_Time(self, type=True) -> None:
        """
            Wenn keine Uhrzeit angegeben ist, dann soll eine Zeit eingegeben werden. Diese Funktion führt errechnet die folgezeiten für alle leeren Zeitkästen & bennet die Dateien um.
        """
        # Typ = True: mit Umbennung; Type = False: ohne Umbennenung
        # Tabellenspalten: 0:Zeit, 1:Dateiname, 2: Pfad
        self.disableAll()
        table = self.tableWidget
        try:
            item = table.item(0, 0).text()
        except:
            QMessageBox.critical(self, "Hinweis", f"Bitte Lade zunächst eine Datei.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.statusBar().showMessage("Eingabenprüfung")
            item, date = vid.timeparser(item, test=True)

            if item: # wenn ein Wert vorhanden ist
                rows = self.tableWidget.rowCount()
                # Die erste Zeitangebe ins Format übertragen
                self.tableWidget.setItem(0, 0, QTableWidgetItem(date))
                for row in range(0, rows):

                    self.statusBar().showMessage("Berechnung der Startzeiten")
                    self.progressBar.setValue((rows+1)/(row+1))

                    startzeit = table.item(row,0).text()
                    video_pfad = table.item(row,2).text()

                    if row < rows: # Errechnet die nächste Startzeit
                        date = vid.get_next_starttime(startzeit, video_pfad)
                        self.tableWidget.setItem(row+1, 0, QTableWidgetItem(date))

                    if type: # Umbenennen des Aktuellen Videos
                        self.statusBar().showMessage("Datei wird umbenannt")
                        vid.rename_Datei(video_pfad,startzeit)
                self.progressBar.setValue(100)
                if type: # Neuladen der Tabelle mit aktuellen Werten
                    self.loeche_Zeileneintaege()
                    for mPfad in self.mainpfad:
                        self.ordnerAuswahl(mPfad)
            else:
                QMessageBox.critical(self, "Hinweis", f"Das eingegebene Format ist ungültig. \nBitte verwende das Format 'YYYY-MM-DD HH-MM-SS'.", QMessageBox.Ok, QMessageBox.Ok)
        self.bereit()
        
        self.enableAll()

    def get_table_data(self) -> object:
        """
            Diese Funktion liest alle items aus der Tabelle in der GUI aus.
        """
        daten = []
        for row in range(self.tableWidget.rowCount()):
            zeile = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                zeile.append(item.text() if item else "")
            daten.append(zeile)
        return daten

    def makeCSV(self):
        """
            Diese Funktion erzeuget eine CSV-Datei, die der Detect und Track-Funktion übergeben wird. Anhand dieser kann OTC ausgefürht werden.
        """
        daten = self.get_table_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_Erfassung()
    window.show()

    sys.exit(app.exec())