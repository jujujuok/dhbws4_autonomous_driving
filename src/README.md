# Abschlussprojekt: Autonomer Rennwagen

```
Matrikelnumme: 3222108
Matrikelnumme: 

```

Dieses "Framework" enthält eine grundlegende Struktur für die Umsetzung einer modularen Pipeline für die Gymnasium Car Racing Simulation ([link](https://gymnasium.farama.org/environments/box2d/car_racing/)).

## 0. Requirements

- Python 3.8
- Ubuntu 20.04 (Empfohlen, kann aber auch abweichen)

## 1. Installation

Wir empfehlen die Pakete global zu installieren. Optional kann aber auch eine Virtuelle Umgebung angelegt werden.

### 1.1 Globale Installation (Empfohlen)

1. Installieren aller python Pakete: `pip install "gymnasium[box2d]" numpy matplotlib scipy opencv-python`
2. In den Source Ordner wechseln `cd <working-dir>`
3. Testen der Installation: `python test_installation.py`. Danach sollte sich die Simulation öffnen und das Fahrzeug zufällig bewegen.

### 1.2 Installation in virtueller Umgebung (Optional)

1. Erstellen einer virtuellen Umgebung im Projektordner:

    ```bash
    cd <working-dir>
    python -m venv .venv
    ```

2. Aktivieren der virtuellen Umgebung: `source .venv/bin/activate`
3. Nun werden alle Python Befehle in dieser Umgebung ausgeführt und Pakete installiert.
   **Wichtig: Die Umgebung muss für jedes Terminal neu aktiviert werden.**
4. In vscode über `strg+shift+P` nach `Python: Select Interpreter` suchen und `.venv` als Interpreter auswählen.
5. Installieren aller python Pakete: `pip install "gymnasium[box2d]" numpy matplotlib scipy opencv-python`
6. Testen der Installation: `python test_installation.py`. Danach sollte sich die Simulation öffnen und das Fahrzeug zufällig bewegen.

## 2. Dateistruktur

Das Projekt ist wie folgt zu strukturieren:

```python
working-dir/
| - .gitignore # Definition von Dateien, die nicht von git getrackt werden sollen
| - car.py # Beschreibt das Fahrzeug und enthält die gesamte Pipeline
| - env_wrapper.py # Wrapper für die Gymnasium Car Racing Simulation
| - input_controller.py # Manuelle Steuerung des Fahrzeugs
| - lane_detection.py # Modul zur Spurerkennung
| - lateral_control.py # Modul zur Querregelung
| - longitudinal_control.py # Modul zur Längsregelung
| - main.py # Hauptdatei, die die Pipeline über 5 Iterationen ausführt
| - path_planning.py # Modul zur Pfadplanung
| - README.md # Diese Datei
```
### 2.1 Datei car.py
```python
In der Datei car.py ist die Car Klasse definirt, welche die Entscheidungsfindung eines autonomen 
Fahrzeugs, indem sie Sensorbeobachtungen (Mittels Vektroren)verarbeitet und Fahrentscheidungen trifft. 
Dabei sind unteranderen die Spurerkennung, Pfadplanung sowie Lateral- und 
Längsregelung, um Lenkwinkel, Beschleunigung und Bremsung zu berechnen.
```

### 2.2 Datei lane_detection.py
```python

Die Klasse LaneDetection ist für die Erkennung der  Fahrspuren in Bildern
eines autonomen Fahrzeugs zuständig. 

Diese Methode 'detect_lanes' nimmt ein Bild als Eingabe und führt eine Vorverarbeitung durch, indem sie das Bild 
beschneidet, um Teile der Anzeige zu entfernen. Anschließend wird die Kantenerkennung auf das Bild angewendet. 
Hierbei wird zwischen einer Standardkantendetektion und einer umfassenderen Evaluationsdetektion unterschieden, 
basierend auf dem evaluate-Flag. Es wird eine Binärisierung durchgeführt, um die Kanten hervorzuheben (image > 70).
Abschließend wird ein Bereich des Bildes maskiert, um das eigene Fahrzeug auszublenden und so die Verarbeitung 
zu vereinfachen (CarConst).

Diese Methode 'lane_clustering' segmentiert die erkannten Linien weiter in Cluster, basierend auf ihrer räumlichen 
Nähe und einer Mindestanzahl von Punkten (min_points). Es wird ein rekursiver Ansatz verwendet, um benachbarte Punkte 
zu finden und diesen Clustern zuzuordnen. Die Cluster werden nummeriert, um unterschiedliche Spurlinien zu 
identifizieren und von einander zu unterscheiden.
```

### 2.2 Datei path_planning.py
```python

Die Klasse PathPlanning ist für die Pfadplanung/ -bestimmung für ein autonomes Fahrzeugsystem zuständig. 

Diese Methode 'sensor_application' verwendet ein Bild um die Abstände und Richtungen zu potenziellen 
Hindernissen oder Fahrspurlinien in verschiedenen Richtungen relativ zur aktuellen Position des 
Fahrzeugs zu bestimmen. Dabei werden Unterschiedliche Vektroen definiert, um die Umgebung des 
gesamten fahrzeug zu erkennen. 

In der Methode 'plan' wird der längste Vektor berehcnte, welche im späteren Verlauf eine 
entscheidenen Rolle für die Querregelung ist. 
```

### 2.3 Datei lateral_control.py
```python
In dieser Klasse wid mittles dem lägsten Vektor der Winkel zwischen der 
Fahrtrichtung und dem Richtungsvektor des Farhzeuges berechnet. Dabei Zeigt der längste Vektro, wo 
das Fahrzeug hinfahren soll.
```


### 2.3 Datei longitudinal_control.py
```python
In dieser Klasse wid mittles einem PID-Regeler die Längsregelung des Fahrzeuges gesteuert. Dabei wird 
die Zeilgeschwindigkeit mit unterscheidlicher Mathematik berechnet. 
```


## 3. Ausführung
1. In dern Ordner ../src navigieren 
2. Venv umgebung starten 
2. In Der Konsole  `python main.py` ausführen 

Die Simulation wird sich öffnen und das Fahrzeug wird sich entsprechend 
der Pipeline bewegen. 

