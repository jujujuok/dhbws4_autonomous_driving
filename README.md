# Abschlussprojekt: Autonomer Rennwagen

``` txt
Matrikelnummer: 3222108
Matrikelnummer: 9994799
```

Dieses "Framework" enthält eine grundlegende Struktur für die Umsetzung einer modularen Pipeline für die Gymnasium Car Racing Simulation ([link](https://gymnasium.farama.org/environments/box2d/car_racing/)).

## 0. Requirements

- Python 3.8
- Ubuntu 20.04 (Empfohlen, kann aber auch abweichen)

## 1. Installation

1. Erstellen einer virtuellen Umgebung im Projektordner:

    ```bash
    cd <working-dir>
    python -m venv .venv
    ```

2. Aktivieren der virtuellen Umgebung: `source .venv/bin/activate`
3. Nun werden alle Python Befehle in dieser Umgebung ausgeführt und Pakete installiert.
   **Wichtig: Die Umgebung muss für jedes Terminal neu aktiviert werden.**
4. In vscode über `strg+shift+P` nach `Python: Select Interpreter` suchen und `.venv` als Interpreter auswählen.

5. Dependencies installieren

    ``` bash
    sudo apt-get install swig build-essential python3-dev

    pip install -r src/requirements.txt
    ```

6. Testen der Installation: `python src/test_installation.py`. Danach sollte sich die Simulation öffnen und das Fahrzeug zufällig bewegen.

## 2. Ausführung

1. In dern Ordner ../src navigieren
2. Venv umgebung starten
3. In Der Konsole  `python main.py` ausführen

Die Simulation wird sich öffnen und das Fahrzeug wird sich entsprechend
der Pipeline bewegen.
