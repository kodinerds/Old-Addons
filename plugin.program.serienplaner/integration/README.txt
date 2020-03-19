



=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
=*=                                                              Für Skinner                                                                        =*=
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=


Skintegration:
==============

Um die Serien des Tages in Confluence zu integrieren sind folgende Schritte erforderlich:


1. Kopieren des XML Files in den Confluence Skin Ordner script-serienplaner.xml

  cp script-tvhighlights.xml /usr/share/kodi/addons/skin.confluence/720p/script-serienplaner.xml


2. Script als include am Skin "anmelden"
Hierzu die Datei "/usr/share/kodi/addons/skin.confluence/720p/includes.xml" editieren, und unterhalb der Zeile:

  <include file="IncludesHomeRecentlyAdded.xml" />

folgendes einfügen:

  <include file="script-serienplaner.xml" />

3. Das include in "/usr/share/kodi/addons/skin.confluence/720p/IncludesHomeRecentlyAdded.xml" ergänzen:
folgendes include Tag muss innerhalb der ControlGroup mit der ID 9003 ergänzt werden.
  
  <include>HomeRecentlyAddedSerienplaner</include>

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
 12                         <include>HomeRecentlyAddedSerienplaner</include>

--------------->8---------------


4. Kategorie Wahl für SerienPlaner hinzufügen (optional)

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
                        <label>SerienPlaner Rubrik</label>
                        <onclick>RunScript(plugin.program.serienplaner,"?methode=show_select_dialog")</onclick>
                </control>
<!-- Ende neu eingefuegter Button -->

--------------->8---------------




Pluginaufrufe:
==============


Startet den Kategorie Dialog:

    RunScript(plugin.program.serienplaner,"?methode=show_select_dialog")

Startet den Scraper:

    RunScript(plugin.program.serienplaner,"?methode=scrape_serien")

Startet Screen-Refresh: 

    RunScript(plugin.program.serienplaner,"?methode=refresh_screen")


Prooperties:
============

"alte" Methode:
----------------
hierbei müssen die Item einzeln angelegt werden...
bisher stehen folgende Items zur Verfügung:

$INFO[Window.Property(SerienPlaner.1.TVShow)]
$INFO[Window.Property(SerienPlaner.1.Staffel)]
$INFO[Window.Property(SerienPlaner.1.Episode)]
$INFO[Window.Property(SerienPlaner.1.Title)]
$INFO[Window.Property(SerienPlaner.1.Starttime)]
$INFO[Window.Property(SerienPlaner.1.Datum)]
$INFO[Window.Property(SerienPlaner.1.neueEpisode)]
$INFO[Window.Property(SerienPlaner.1.Channel)]
$INFO[Window.Property(SerienPlaner.1.Logo)]
$INFO[Window.Property(SerienPlaner.1.PVRID)]
$INFO[Window.Property(SerienPlaner.1.Description)]
$INFO[Window.Property(SerienPlaner.1.Rating)]
$INFO[Window.Property(SerienPlaner.1.Alterfreigabe)]
$INFO[Window.Property(SerienPlaner.1.Genre)]
$INFO[Window.Property(SerienPlaner.1.Studio)]
$INFO[Window.Property(SerienPlaner.1.Status)]
$INFO[Window.Property(SerienPlaner.1.Jahr)]
$INFO[Window.Property(SerienPlaner.1.Thumb)]
$INFO[Window.Property(SerienPlaner.1.FirstAired)]
$INFO[Window.Property(SerienPlaner.1.RunningTime)]
$INFO[Window.Property(SerienPlaner.1.Poster)]
$INFO[Window.Property(SerienPlaner.1.Fanart)]
$INFO[Window.Property(SerienPlaner.1.Clearlogo)]
$INFO[Window.Property(SerienPlaner.1.WatchType)]



Dynamic Content:
----------------
hier stehen folgende Items zur Verfügung:
$INFO[ListItem.Label]
$INFO[ListItem.Label2]
$INFO[ListItem.Thumb]
$INFO[ListItem.Season]
$INFO[ListItem.Episode]
$INFO[ListItem.Title]
$INFO[ListItem.Genre]
$INFO[ListItem.mpaa]
$INFO[ListItem.Year]
$INFO[ListItem.Plot]
$INFO[ListItem.Rating]
$INFO[ListItem.Studio]
$INFO[ListItem.Tvshowtitle]
$INFO[ListItem.Art(Poster)]
$INFO[ListItem.Art(Fanart)]
$INFO[ListItem.Art(Clearlogo)]
$INFO[ListItem.Property(Senderlogo)]
$INFO[ListItem.Property(Starttime)]
$INFO[ListItem.Property(Date)]
$INFO[ListItem.Property(RunTime)]
$INFO[ListItem.Property(PVRID)]
$INFO[ListItem.Property(Status)]
$INFO[ListItem.Property(Datetime)]

Aufruf dynamic content: plugin://plugin.program.serienplaner/?methode=get_item_serienplaner&amp;reload=$INFO[Window(Home).Property(SerienPlaner.Countdown)]


Debugging:
==========
einfach den Debuglog in Kodi aktivieren....
