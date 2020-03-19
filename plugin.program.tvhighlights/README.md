Beschreibung:
=============

Das Plugin plugin.program.tvhighlights holt von tvdigital.de die TV-Highlights des Tages und stellt diese dann als 
RecentlyAdded Widget beim Menüpunkt TV bereit (nach Skintegration).
Hierbei richtet sich das Plugin anhand der im PVR befindlichen Sender, und zeigt nur TV Highlights für diese an.
Desweiteren besteht eine integration des Dienstes service.kn.switchtimer in der Sendungs-Detailansicht mit 
welchem die Highlights zum umschalten vorgemerkt werden können.

Im Settingsmenü kann eingestellt werden welche Kategorie für die Anzeige und Aktualisierung verwendet werden soll.
Zur Auswahl stehen hier folgende Kategorien:
  * spielfilme
  * serien
  * sport
  * kinder
  * doku und info
  * unterhaltung

Ein Popup-Window kann für die Highlights geöffnet werden, in welchem Detailinformationen zur Sendung angezeigt werden, und mithilfe des Dienstes "service.kn.switchtimer" (Danke BJ1) kann ein Umschalten vorgemerkt werden.

Das Plugin wird bei jedem Kodi Start ausgefüht und aktualisiert die Daten. Je nachdem welches Interval man für Content Refresh eingestellt hat geht es in eine Loop 
und aktualisiert die TV-Highlights anhand der eingestellten Minuten. Ist hier die "0" ausgewählt, beendet sich der Dienst, ohne Daten abzurufen. Die Anzeige Aktualisierung kann hier seperat eingestellt werden.



Modi:
==============

Es gibt zwei Modi in denen das Plugin betrieben werden kann:
- Mastermode
- Splitmode


Mastermode:
--------------
Im Mastermode wird eine Kategorie ausgewählt welche vom Plugin automatisch aktualisiert wird.
Als Kategorie (watchtype) kann folgendes verwendet werden: 
- spielfilm
- serie
- unterhaltung
- sport
- kinder
- doku-und-info



Splitmode:
--------------
Hierbei können mehrere Kategorien ausgewählt werden welche vom Plugin aktualisiert werden sollen. 
Die zur Verfügung stehenden Kategorien sind die selben wie im Mastermode.


Einstellungen:
==============
Das Plugin kann so konfiguriert werden dass nur Sendungen angezeigt werden, welche beim letzten screen refresh nicht schon in der Vergangenheit lagen.
Weiterhin kann das Content Refresh Interval konfiguriert werden. (Bitte denkt an den Hoster, also nicht zu oft aktualisieren. Denke kleiner 120 Minuten ist unnötig)
Auch die Popup Nachricht beim Start von kodi und dem Content-Refresh kann aktiviert/deaktiviert werden.



Um das Plugin nutzen zu können erfordert es einer Skin Integration. Siehe hierzu die Readme.txt im Ordner "integration"
