# -*- coding: utf-8 -*- 
import sys
from verarbeitung import opentracffic as ot
from verarbeitung import analyse_erfassung as ae
from mainUi_ui import Ui_MainWindow
from PyQt6.QtGui import QAction, QKeyEvent
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMainWindow, QMessageBox, QPushButton, QMenu

class Ui_Erfassung(QMainWindow, Ui_MainWindow):
    # https://doc.qt.io/
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.addButton.clicked.connect(self.ordnerEingabe)
        self.addCSVButton.clicked.connect(self.csvEingabe)
        self.reloadButton.clicked.connect(self.bestaetigen)
        self.otanalyticsButton.clicked.connect(self.start_ota)
        self.resetButton.clicked.connect(self.resetGui)
        self.startButton.clicked.connect(self.get_input)

        self.reset_aktiv = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_button)
        
        # Spalten automatisch anpassen
        self.tableWidget.resizeColumnsToContents()
        
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

        # Standart-Werte laden
        self.tableStatus = None
        self.load_standard()

        # Staus anzeigen
        self.statusBar().showMessage("Bereit")
        
        # Alle Pfade sichern 
        self.mainpfad = []
    
    """
        Button - Definiton
    """
    def ordnerEingabe(self) -> None:
        """
            Durch den Nutzer gestartet und läd einen ordner, anschließend wird der Pfad an ordnerAuswahl übergeben.
        """
        directory = QFileDialog.getExistingDirectory(self, "Ordner wählen", "")
        if directory:
            self.mainpfad.append({"pfad":directory})
            self.aktivVideo()
            self.videoTabelle(directory)

    def csvEingabe(self) -> None:
        """
            Durch den Nutzer gestartet und läd eine Datei.
        """
        self.aktivCSV()
        # dateien, _ = QFileDialog.getOpenFileNames(self, "Dateien öffnen", "", "Alle Dateien (*);;Python-Dateien (*.py)")

    def bestaetigen(self) -> None:
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

    def get_input(self):
        """
            Hierin wird der Ablauf bestimmt, der stattfindet, wenn auf Start gedrückt wird.
        """
        self.statusBar().showMessage("Bitte Beachte die neu geöffneten Fenster.")
        # self.disableAll()
        
        if self.tableStatus == "Video":
            df_video = self.get_table_data(True)
        
        if self.oneVideoBox.isChecked():
            ae.make_onevideo(df_video)
            self.infobox("Es wurde ein durchgehendes Video mit Zeitstempel erstellt.")
            # QMessageBox.information(self, "Hinweis", f"Es wurde ein durchgehendes Video mit Zeitstempel erstellt.", QMessageBox.Ok, QMessageBox.Ok)
        if self.vidoezeitBox.isChecked():
            ae.videozeit_in_video(df_video)
            self.infobox("Alle Viedeos wurden mit einem Zeitstempel versehen.")
            # QMessageBox.information(self, "Hinweis", f"Alle Viedeos wurden mit einem Zeitstempel versehen.", QMessageBox.Ok, QMessageBox.Ok)
        if self.detectBox.isChecked() or self.trackBox.isChecked():
            for mpfad in self.mainpfad:
                directory = mpfad["pfad"]
                detect = self.detectBox.isChecked()
                track = self.trackBox.isChecked()
                durination = ae.get_durination(directory)
                modell = self.modellBox.currentText()
                conf_value = self.confSpinBox.value()
                iou_value = self.iouSpinBox.value()
                ot.start_otc(detect, directory, durination, modell, conf_value, iou_value, track)

        # if self.rErgBox.isChecked():
        #     pass
        # if self.excelBox.isChecked():
        #     pass
        self.aktivVideo()
        self.bereit()

    def start_ota(self):
        ot.start_otanalytics()

    """
        Ausführungen 
    """
    def videoTabelle(self, directory:str) -> None:
        """
            Diese Funktion liest alle Videos in einem Ordner, der vom Nutzer bestimmt wurde, aus und gibt die Videos in der Tabelle an.
        """
        self.statusBar().showMessage("Dateien laden")
        error, df_videos, errortyp = ae.dateien_laden(directory)

        if error:
            if errortyp == "Inhalt":
                QMessageBox.information(self, "Hinweis", f"Es sind keine Videos im Ordner \n{directory} \nvorhanden.", QMessageBox.Ok, QMessageBox.Ok)
            elif errortyp == "Pfad":
                QMessageBox.warning(self, "Warnung", f"Es wurde kein Pfad ausgewählt oder eingegeben. \nBitte Wiederholen Sie die Eingabe.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.tabelle_fuellen(df_videos)
        self.bereit()

    def tabelle_fuellen(self, df:dict) -> None:
        """
            Füllt die Tabelle mit allen Elementen, die im df liegen. Beachte, dass sie nur die Spalten füllt, die vorhandne sind. Sie achtet dabei nicht auf die Überschriften.
        """
        for _, row in df.iterrows():
            # Neue Zeile am Ende hinzufügen
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for idx, value in enumerate(row):
                # In GUI-Tabelle einfügen
                self.tableWidget.setItem(rowPosition, idx, QTableWidgetItem(value))

    def reload_Time(self) -> None:
        """
            Wenn keine Uhrzeit angegeben ist, dann soll eine Zeit eingegeben werden. Diese Funktion führt errechnet die folgezeiten für alle leeren Zeitkästen & bennet die Dateien um.
        """
        # Typ = True: mit Umbennung; Typ = False: ohne Umbennenung
        self.disableAll()
        df_video = self.get_table_data(True)

        error, idx, datum_uhrzeit = ae.test_zeiteingabe(df_video, self.mainpfad)
        if error:
            QMessageBox.critical(self, "Hinweis", f"Das eingegebene Format für das {idx}. Videopaket ist ungültig. \nBitte verwende das Format 'YYYY-MM-DD HH-MM-SS' und geben sie einen Zeitpunkt ein.\n{datum_uhrzeit}", QMessageBox.Ok, QMessageBox.Ok)
        else:

            if self.renameBox.isChecked():
                ae.dateiname_anpassen(df_video)
                self.loeche_Zeileneintaege()
                for mpfad in self.mainpfad:
                    self.videoTabelle(mpfad["pfad"])
            else:
                self.loeche_Zeileneintaege()
                self.tabelle_fuellen(df_video)

        self.bereit()
        self.aktivVideo()
            
    def makeCSV(self):
        """
            Diese Funktion erzeuget eine CSV-Datei, die der Detect und Track-Funktion übergeben wird. Anhand dieser kann OTC ausgefürht werden.
        """
        daten = self.get_table_data()

    def delete_selected_row(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            self.tableWidget.removeRow(current_row)

    """
        Gui - Anpassungen
    """
    def load_standard(self):
        """
            # Setzt alle Elemente auf die Ausgangslage
        """
        # Werte laden
        value = ae.get_standard_values()
        # Standartwerte
        self.tableStatus = None
        self.mainpfad = [] 
        # setzte & füllen
        self.addButton.setDisabled(False)
        self.addCSVButton.setDisabled(False)
        self.renameBox.setDisabled(False)
        self.renameBox.setChecked(True)
        self.reloadButton.setDisabled(True)
        self.tableWidget.setDisabled(False)
        self.loeche_Zeileneintaege()
        self.tableWidget.setColumnCount(0)
        self.vidoezeitBox.setDisabled(False)
        self.vidoezeitBox.setCheckable(False)
        self.vidoezeitBox.setChecked(False)
        self.oneVideoBox.setDisabled(False)
        self.oneVideoBox.setCheckable(False)
        self.oneVideoBox.setChecked(False)
        self.trackBox.setDisabled(False)
        self.trackBox.setCheckable(False)
        self.trackBox.setChecked(False)
        self.detectBox.setDisabled(False)
        self.detectBox.setCheckable(False)
        self.detectBox.setChecked(False)
        self.otanalyticsButton.setDisabled(True)
        self.modellBox.setDisabled(True)
        self.modellBox.clear()
        self.modellBox.addItems(value["modells"])
        self.modellBox.setCurrentIndex(value["modell_standard"])
        self.confSpinBox.setDisabled(False)
        self.confSpinBox.setReadOnly(True)
        self.confSpinBox.setValue(value["conf_value"])
        self.iouSpinBox.setDisabled(False)
        self.iouSpinBox.setReadOnly(True)
        self.iouSpinBox.setValue(value["iou_value"])
        self.rErgBox.setDisabled(False)
        self.rErgBox.setCheckable(False)
        self.rErgBox.setChecked(False)
        self.excelBox.setDisabled(False)
        self.excelBox.setCheckable(False)
        self.excelBox.setChecked(False)
        self.startButton.setDisabled(False)

    def reset_button(self) -> None:
        # Button zurücksetzen
        self.reset_aktiv = False
        self.resetButton.setStyleSheet("") 
        self.bereit()

    def disableAll(self) -> None:
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
        self.otanalyticsButton.setDisabled(True)
        self.modellBox.setDisabled(True)
        self.confSpinBox.setDisabled(True)
        self.iouSpinBox.setDisabled(True)
        self.rErgBox.setDisabled(True)
        self.excelBox.setDisabled(True)
        self.startButton.setDisabled(True)

    def resetGui(self) -> None:
        if self.reset_aktiv:
            self.reset_button()
            self.load_standard()

        else:
            self.reset_aktiv = True
            self.resetButton.setStyleSheet("background-color: red;")
            self.timer.start(10000)
            self.statusBar().showMessage("Rest bitte bestätigen.", 10000)

    def aktivVideo(self) -> None:
        """
            Reduzeirt die Auswahl, wenn Videos barbeitet werden.
        """
        # Enable
        self.reloadButton.setEnabled(True)
        self.vidoezeitBox.setCheckable(True)
        self.oneVideoBox.setCheckable(True)
        self.trackBox.setCheckable(True)
        self.detectBox.setCheckable(True)
        self.otanalyticsButton.setDisabled(False)
        self.modellBox.setEnabled(True)
        self.confSpinBox.setReadOnly(False)
        self.iouSpinBox.setReadOnly(False)
        # Check
        self.trackBox.setChecked(True)
        self.detectBox.setChecked(True)
        # Disable
        self.addCSVButton.setDisabled(True)
        self.rErgBox.setDisabled(True)
        self.excelBox.setDisabled(True) 
        # Tabelle-Anpassen
        if self.tableStatus != "Video":
            self.prepareTable("videotabelle")
            self.tableStatus = "Video"

    def aktivCSV(self) -> None:
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
        self.modellBox.setDisabled(True)
        self.confSpinBox.setDisabled(True)
        self.iouSpinBox.setDisabled(True)
        # Tabelle-Anpassen
        if self.tableStatus != "CSV":
            self.prepareTable("csvtabelle")
            self.tableStatus = "CSV"
    
    def prepareTable(self, typ:str) -> None:
        werte = ae.get_standard_values(f"{typ}")
        self.tableWidget.setColumnCount(len(werte))
        self.tableWidget.setHorizontalHeaderLabels(werte)

    def loeche_Zeileneintaege(self) -> None:
        """
            löscht alle Zeilen
        """
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        QApplication.processEvents()
        self.bereit()

    def bereit(self) -> None:
        self.tableWidget.resizeColumnsToContents()
        self.statusBar().showMessage("Bereit")
        self.progressBar.setValue(0)

    def get_column_name(self):
        """
            Holt sich alle Spaltennamen
        """
        names = []
        for i in range(self.tableWidget.columnCount()):
            names.append(self.tableWidget.horizontalHeaderItem(i).text())
        return names   

    def get_table_data(self, video:bool=False) -> object:
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

        names = self.get_column_name()
        df = ae.convert_to_pandas(daten, names)

        if video:
            return ae.zeiten_anpassen(df, self.mainpfad)
        return df

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            self.delete_selected_row()
        else:
            super().keyPressEvent(event)

    def show_context_menu(self, position):
        menu = QMenu(self.tableWidget)

        menu.addAction("Zeile löschen", self.delete_selected_row)
        
        menu.exec(self.tableWidget.viewport().mapToGlobal(position))
    
    """
    Weitere Abfragen/Anzeigen
    """
    def infobox(self, text:str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(text)
        msg.setWindowTitle("Auto-Closing Info")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    
        # Close after 5 seconds
        QTimer.singleShot(10000, lambda: msg.done(0))
        msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_Erfassung()
    window.show()

    sys.exit(app.exec())