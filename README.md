# AddOn-OpenTrafficCam #
Ein kleiner Zusatz, um die Umbenennungen der Videos und Aktivierung des OTVision-Programms zu automatisieren.
Unter [>> grafik_cuda.md <<](grafik_cuda.md) sind Hinweise und Hilfestellungen für die Nutzbarmachung der grafischen Schnittstelle angeführt.

## Installation ##
Mit der Version 3 wird lediglich die GoOn.cmd sowie die rename.py benötigt. Die rename.py muss in der gleichen Ordner wie die GoOn.cmd liegen. Zusätzlich muss unter den Umgebungsvariablen vom System die Vaiable = OT_PATH mit Wert = %Pfad_zum_'Ober'ordner_von_OpenTrafficCam% hinterlegt werden. So das der Ordner OTVision in dem Verzeichnis gefunden werden kann.<br>
Unter der folgenden Hierachie muss der Ordner 'OTraffic' als Ziel im Path angegeben werden:
    
    GitHub > OTraffic > OTVision 

## Hinweis ##
Die Dateien mit rename_v?.py sind ältere Versionen von der Datei ohne rename_v?.py

Um einen Durchlauf der Programme ohne manuelle Eingaben ist anstelle der OTVision.cmd die GoOn.cmd zu nutzen.
---
## Installation Alt ##
- die beiden Dateien oben herunterladen.
- die .bat-Datei in dem Ordner vor dem OTVision-Programm ablegen, den Ordner mit dem OTVision-Programm in 'OTVision' umbenennen, falls dieser anders heißt.
- die 'rename.py' in den Ordner 'OTVision' ablegen. <br>
---
  Die Dateien sollten wie folgt aufzufinden sein:<br>
    ...\OTVision.cmd<br>
    ...\OTVision\rename.py

## Anwenden ##
Zum Starten des Programms nur ein Doppelklick auf die OTVision.bat-Datei. Anschließend wird man in der Konsole geführt.

## Disclaimer ##
Durch kleine Veränderungen kann das Program nicht wie geplant laufen. <br>
Benutzung auf eigene Gefahr. Der/die Ersteller kommen nicht für etwaig Schäden an Hard- und Software auf. 
