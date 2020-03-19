###########################################################################
#
#          FILE:  plugin.program.tvhighlights
#
#        AUTHOR:  Tobias D. Oestreicher
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.1.2
#       CREATED:  22.01.2016
#
###########################################################################
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.
#
###########################################################################
#     CHANGELOG:  (22.01.2016) TDOe - First Publishing
###########################################################################


Beschreibung:
=============

Das Plugin 'plugin.program.tvhighlights' holt von tvdigital.de die TV-Highlights des Tages und stellt diese dann als
RecentlyAdded Widget im Menüpunkt TV bereit (nach Skintegration).
Hierbei richtet sich das Plugin anhand der im PVR befindlichen Sender, und zeigt nur TV Highlights für diese an.
Desweiteren besteht eine Integration des Dienstes service.kn.switchtimer in der Sendungs-Detailansicht mit
welchem die Highlights zum Umschalten vorgemerkt werden können.

Im Settingsmenü kann eingestellt werden welche Kategorie für Anzeige und Aktualisierung verwendet werden soll.
Zur Auswahl stehen hier folgende Kategorien:

  * Spielfilm
  * Serie
  * Sport
  * Kinder
  * Doku und Info
  * Unterhaltung

Pro Highlights kann ein Popup geöffnet werden, in welchem Detailinformationen zur Sendung angezeigt werden. Über den
Dienst "service.kn.switchtimer" (Danke BJ1) kann ein Umschalten vorgemerkt werden.

Das Plugin wird bei jedem Kodi Start ausgefüht und aktualisiert die Daten in Abhängigkeit vom eingestellten Intervall
(0 - kein erneuter Datenabruf). Es erfolgt jedoch trotzdem eine Aktualisierung des Widgets, um z.B. abgelaufene
Sendungen aus der Anzeige zu entfernen (in den Einstellungen wählbar).

Hinweise:

Die Einstellungen für die Aktualisierung der Inhalte (werden von der Webseite von TV Digital abgerufen) sollten moderat
ausgewählt werden. Ein Intervall von 120 Minuten sollte vollkommen ausreichend sein. Die Aktualisierung des Widgets
richtet sich nach den Sehgewohnheiten des Benutzers, ein Wert von 30 Minuten ist auch hier ausreichend.



=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
=*=                                             Für Skinner                                        =*=
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*


Skintegration:
==============

Um die TVHighlights des Tages in Confluence zu integrieren sind folgende Schritte erforderlich (als Beispiel dient hier
die Integration unter einer Linux-Distribution). Die zum Kopieren erforderlichen Dateien befinden sich im Ordner
'integration/Confluence' bzw. 'integration/Destiny' des Plugins (plugin.program.tvhighlights):

cd $HOME/.kodi/addons/plugin.program.tvhighlights/integration/Confluence

1. Kopieren des XML Files in den Confluence Skin Ordner

  sudo cp script-tvhighlights.xml /usr/share/kodi/addons/skin.confluence/720p/

2. Script als include am Skin "anmelden"
Hierzu die Datei "/usr/share/kodi/addons/skin.confluence/720p/includes.xml" editieren, und unterhalb der Zeile:

  <include file="IncludesHomeRecentlyAdded.xml" />

folgendes einfügen:

  <include file="script-tvhighlights.xml" />

3. Das include in "/usr/share/kodi/addons/skin.confluence/720p/IncludesHomeRecentlyAdded.xml" ergänzen:
folgendes include Tag muss innerhalb der ControlGroup mit der ID 9003 ergänzt werden.
  
  <include>HomeRecentlyAddedTVHighlightsTodayInfo</include>

Beispiel:
---------------8<---------------
  1 <?xml version="1.0" encoding="UTF-8"?>
  2 <includes>
  3         <include name="HomeRecentlyAddedInfo">
  4                 <control type="group" id="9003">
  5                         <onup>20</onup>
  6                         <ondown condition="System.HasAddon(script.globalsearch)">608</ondown>
  7                         <ondown condition="!System.HasAddon(script.globalsearch)">603</ondown>
  8                         <visible>!Window.IsVisible(Favourites)</visible>
  9                         <include>VisibleFadeEffect</include>
 10                         <animation effect="fade" time="225" delay="750">WindowOpen</animation>
 11                         <animation effect="fade" time="150">WindowClose</animation>
 12                         <include>HomeRecentlyAddedTVHighlightsTodayInfo</include>

--------------->8---------------


4. Kategorie Wahl für TV Highlights im Master Mode hinzufügen (optional)

in der Datei "/usr/share/kodi/addons/skin.confluence/720p/IncludesHomeMenuItems.xml"
folgende Stelle suchen:

---------------8<---------------
        <include name="HomeSubMenuTV">
                <control type="image" id="90141">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3" flipx="true">HomeSubEnd.png</texture>
                </control>
--------------->8---------------

direkt im Anschluss den zusätzlichen Button hinzufügen:

---------------8<---------------
<!-- Begin neu eingefuegter Button -->
                <control type="button" id="97149">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>$ADDON[plugin.program.tvhighlights 30011]</label>
                        <onclick>RunScript(plugin.program.tvhighlights,"?methode=show_select_dialog")</onclick>
                </control>
<!-- Ende neu eingefuegter Button -->

--------------->8---------------

Pluginaufrufe:
==============

Der Dienst für die Aktualisierung der Inhalte und des Widgets (starter.py) ruft das eigentliche Plugin
über den Parameter 'methode' auf. Dieser Parameter kann auch von anderen Plugins oder Scripten wie folgt verwendet
werden:

Führt ein erneutes Einlesen der Webseiten von TV Digital durch:

    XBMC.RunScript(plugin.program,tvhighlights,"?methode=scrape_highlights")

Aktualisiert das TV Highlight Widget. Ist die Option 'zeige zurückliegende Sendungen an' nicht gesetzt, werden
abgelaufene Sendungen entfernt.

    XBMC.RunScript(plugin.program.tvhighlights,"?methode=refresh_screen")

Öffnet ein Fenster mit zusätzlichen Informationen zur ausgewählten Sendung. Dazu muss ein zusätzlicher Parameter mit
der URL zur Sendung angegeben werden. Dieser wird in einem Property des Widgets gespeichert.

Beispiel 'onclick' für TV Highlights Element - Öffnet Popup generiert vom Plugin (script-TVHighlights-DialogWindow.xml):

    <onclick>
        RunScript(plugin.program.tvhighlights,"?methode=infopopup&detailurl=$INFO[Window.Property(TVHighlightsToday.1.Popup)]")
    </onclick>

Properties (<nr> im Bereich von 1...16)

  TVHighlightsToday.<nr>.ID
  TVHighlightsToday.<nr>.Title
  TVHighlightsToday.<nr>.Thumb
  TVHighlightsToday.<nr>.Time
  TVHighlightsToday.<nr>.Channel
  TVHighlightsToday.<nr>.PVRID
  TVHighlightsToday.<nr>.Logo
  TVHighlightsToday.<nr>.Genre
  TVHighlightsToday.<nr>.Comment
  TVHighlightsToday.<nr>.Extrainfos
  TVHighlightsToday.<nr>.Popup
  TVHighlightsToday.<nr>.Watchtype

Info-Window:

  TVHighlightsToday.Info.Title
  TVHighlightsToday.Info.Picture
  TVHighlightsToday.Info.Subtitle
  TVHighlightsToday.Info.Description
  TVHighlightsToday.Info.Broadcastdetails
  TVHighlightsToday.Info.Genre
  TVHighlightsToday.Info.Channel
  TVHighlightsToday.Info.Logo
  TVHighlightsToday.Info.PVRID
  TVHighlightsToday.Info.StartTime
  TVHighlightsToday.Info.EndTime
  TVHighlightsToday.Info.RatingType.1
  TVHighlightsToday.Info.Rating.1
  TVHighlightsToday.Info.RatingType.2
  TVHighlightsToday.Info.Rating.2
  TVHighlightsToday.Info.RatingType.3
  TVHighlightsToday.Info.Rating.3
  TVHighlightsToday.Info.RatingType.4
  TVHighlightsToday.Info.Rating.4
  TVHighlightsToday.Info.RatingType.5
  TVHighlightsToday.Info.Rating.5

Sonstiges:

  numCategories - Anzahl der im Setup ausgewählten Kategorien

Debugging:

Das Plugin wird gesprächig, wenn in den Einstellungen von Kodi unter System, Logging das Debug-Logging aktiviert
wird.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!                                                   ACHTUNG                                                     !!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


Es ist NICHT notwendig Aktualisierungen innerhalb irgendwelcher <onload>`s auszuführen! Das Plugin verfügt über einen
Dienst, welcher sich sowohl um die Content-Aktualisierung als auch um die Aktualisierung der angezeigten Daten kümmert.
Beide Werte sind im Setup einstellbar.


-- That's It , viel Spass damit, TDOe 2015-2016 --
