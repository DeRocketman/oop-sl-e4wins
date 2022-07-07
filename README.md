# OOP SL SoSe 22 "e4Wins" 

## Autoren:
- Maximilian Rupprecht
- Dirk Stricker

## Struktur

    |-src               Beinhaltet sämtlichen Code
    | |-controller      Ordner für Controller-Klassen
    | |-model           Ordner für Model-Klassen
    | |-services        Ordner für Service-Klassen
    | |-view            Ordner für View-Klassen
    |
    |-README.md         Informationen über das Projekt
    |-requirements.txt  Informationen über genutzte Packages

## Anforderungen/Beschreibungen

### Benutztes Framework:
    PyGame

### Projektidee:
    Wir möchten das Gesellschaftsspiel „4 Gewinnt“ als Hausarbeit entwickeln. 
    Dieses Spiel sollte in einem Netzwerk gespielt werden können.

### Grobes Spielprinzip

    Die Spieler müssen im Startbildschirm ein Nick-Name wählen und entscheiden, ob sie einem Spiel beitreten 
    oder selbst eins hosten möchten. Wenn die Spieler selbst ein Spiel hosten wollen, soll die IP-Adresse angezeigt 
    werden, die sie dann ihrem Spielpartner mitteilen müssen, damit eine Verbindung hergestellt werden kann.
    Wenn ein User einem Spiel beitreten möchte, muss er die IP-Adresse eines Hosts in einem Textfeld eingeben.
    Dem Host soll der Name des teilnehmenden Spielers angezeigt werden.
    Das Spiel darf erst gestartet werden können, wenn beide Spieler bereit sind.

    Anschließend wird das Spiel gespielt. Dabei wird abwechselnd ein Spielstein in das Spielfeld fallen gelassen. 
    Das Spiel prüft eigenständig, ob ein Sieger feststeht.

