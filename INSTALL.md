# Vorbereitung

Das Photoblog basiert auf Diensten von Google, es ist dort folglich zwingend ein kostenfreies Benutzerkonto notwendig. Sollte noch keines vorhanden sein, lässt sich eines in wenigen Minuten registrieren. Anschließend muss man sich noch für zwei Dienste bei Google eintragen:

* [AppEngine](http://appengine.google.com/) - hier wird die Photoblog-Software installiert. Sobald man sich eingetragen hat, sollte man sich noch einen benutzerdefinierten und eindeutigen Namen ausdenken.
* [PicasaWeb](http://picasaweb.google.com) - hier werden die Fotos selbst abgespeichert. Es empfiehlt sich, direkt ein oder zwei Fotos für die noch folgende initiale Einrichtung hochzuladen.

# Konfiguration der Software

Nachdem das heruntergeladene Archiv entpackt worden ist, müssen noch einige Einstellungen vorgenommen werden. Dazu wird die Datei ``conf.py.EXAMPLE`` nach ``conf.py`` kopiert und bearbeitet.  PicasaWeb verwendet eindeutige Nummern zur Identifikation von Fotoalben. Die eindeutige Nummer des zuvor erstellten Albums muss noch ermittelt werden. Das mitgelieferte Script ``get_picasa_id.py`` kann dabei behilflich sein. Als mail_from_address sollte unbedingt die Adresse des eigenen Google-Kontos verwendet werden (oder die eines anderen, bei AppEngine eingetragenen, Administrators), da die Infrastruktur von Google sonst keinen Versand von E-Mails zulässt.

Als host kann man entweder http://_DERZUVORAUSGEWHÄLTENAMEFÜRDASWEBLOG_.appspot.com verwendet werden oder eine bei Google Apps betriebene Domain ([Anleitung dazu](http://code.google.com/appengine/articles/domains.html))

Templates können nach belieben bearbeitet werden. Dabei ist die [offizielle Dokumentation der verwendeten Django Template Engine](http://www.djangoproject.com/documentation/0.96/templates/) nützlich. Dies ist auch ein ausgezeichneter Zeitpunkt, die Anwendung gegebenenfalls in eine andere Sprache zu übersetzen.

# Inbetriebnahme

Zum Hochladen des Photoblogs wird das [Google Appengine SDK](http://code.google.com/intl/de/appengine/downloads.html) benötigt. Google stellt eine [Anleitung zum eigentlichen Hochladen der Software über dieses SDK](http://code.google.com/intl/de/appengine/docs/python/tools/uploadinganapp.html) bereit. Nachdem das Photoblog hochgeladen ist, genügt ein Aufruf von http://_DERZUVORAUSGEWHÄLTENAMEFÜRDASWEBLOG_.appspot.com/update (wo  man sich mit seinen Zugangsdaten von Google anmelden muss), um die Fotos aus dem Album bei PicasaWeb zu übertragen. Nach dieser initialen Einrichtung sollte kein weiterer manueller Aufruf mehr notwendig sein.
