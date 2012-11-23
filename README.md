# Worum geht es?

Photoblog ist eine Software zum Erstellen von Foto-Weblogs, gestützt durch Google Appengine und den Picasa Fotoalben. Für den Betrieb wird also nichts weiter benötigt als ein Konto bei Google. Photoblog wird unter der GPL v3 lizensiert.

# Wie funktioniert es?

Um ein Foto im Photoblog zu veröffentlichen, muss es lediglich in ein vorher bestimmtes Album des PicasaWeb-Kontos hochgeladen werden. Dazu kann entweder ein geeignetes Programm, wie etwa Picasa, F-Spot oder Lightroom verwendet werden, oder das gewöhnliche Web-Formular. PicasaWeb wird sich dabei um die Skalierung, die Kompression, das Erstellen von Vorschaubildern und um die Aufbereitung von EXIF-Informationen kümmern. Die Photoblog-Software wird regelmäßig überprüfen, ob neue Fotos hochgeladen wurden und pro neuem Foto einen neuen Eintrag im Weblog erstellen. Bei Bedarf kann die Überprüfung natürlich auch manuell durchgeführt werden, ein manuelles Eingreifen sollte jedoch zu keiner Zeit notwendig sein.

## Beispiel

[Mein eigenes Foto-Weblog wird mit dieser Software betrieben.](http://fotos.florianheinle.de)

## Features

* Kein kostenpflichtiger Webspace notwendig. Ein kostenloses Google-Konto reicht aus
* Die robuste Infrastruktur von Google stellt zuverlässigen und schnellen Betrieb quasi sicher
* Nach der Installation sind keine Wartungsarbeiten mehr notwendig, bis auf das Hochladen neuer Bilder
* Die gewohnte Software zur Bilderverwaltung (Picasa, F-Spot, Lightroom, etc) kann zum Upload verwendet werden, bei Bedarf auch stapelweise
* Besucher können sich für ein Abo per E-Mail oder RSS eintragen
* Design mittels Django templates (0.96)
* Vorhandene EXIF-Informationen können angezeigt werden
* Freie Software (gratis & GPLv3)

# Download

[Aktuelle Entwicklungsversion](https://github.com/fheinle/Photoblog/archive/master.zip)

oder

    $ git clone git://github.com/fheinle/Photoblog.git

# Installation

Siehe dazu die eigene Seite der Installationsanleitung
