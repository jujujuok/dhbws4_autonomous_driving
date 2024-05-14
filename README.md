# Abschlussprojekt: Autonomer Rennwagen

Dieses "Framework" enthält eine grundlegende Struktur für die Umsetzung einer modularen Pipeline für die Gymnasium Car Racing Simulation ([link](https://gymnasium.farama.org/environments/box2d/car_racing/)).

## 0. Requirements

- Python 3.x
- Ubuntu 22.04 (Empfohlen)

## 1. Installation

1. Erstellen einer virtuellen Umgebung im Projektordner:

    ```bash
    cd <working-dir>
    python -m venv .venv
    ```

2. Dependencies installieren

    _Achtung: die virtuelle Umgebung muss aktiviert sein._

    ``` bash
    sudo apt-get install swig build-essential python3-dev

    pip install -r src/requirements.txt
    ```

3. Testen der Installation: [`test_installation.py`](src/test_installation.py). Danach sollte sich die Simulation öffnen und das Fahrzeug zufällig bewegen.

## 2. Ausführung

1. In dern Ordner ../src navigieren
2. Venv umgebung starten
3. [`main.py`](src/main.py) ausführen

Die Simulation wird sich öffnen und das Fahrzeug sich entsprechend
der Pipeline bewegen.

## 3. Parallele Ausführung mit Multiprocessing

[Multiprocessing](../src/main_multiprocessing.py) mit dem flag `--parallel` ausführen für parallele Auswertung.

Credits an [Fabian @hfxbse](https://github.com/hfxbse), der dieses Feature hinzugefügt hat, weil das [Repo](https://github.com/jujujuok/dhbws4_autonomous_driving) öffentlich einsehbar ist.
