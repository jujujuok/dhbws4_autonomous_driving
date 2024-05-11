# Abschlussprojekt: Autonomer Rennwagen

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

## 3. Ausführung
1. In dern Ordner ../src navigieren 
2. Venv umgebung starten 
2. In Der Konsole  `python main.py` ausführen 

Die Simulation wird sich öffnen und das Fahrzeug wird sich entsprechend 
der Pipeline bewegen. 

