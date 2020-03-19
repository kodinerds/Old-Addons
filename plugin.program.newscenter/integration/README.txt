###########################################################################
#
#          FILE:  plugin.program.newscenter
#
#        AUTHOR:  Tobias D. Oestreicher
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.0.1
#       CREATED:  14.02.2016
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
#     CHANGELOG:  (14.02.2016) TDOe - First Publishing
#                 (02.04.2016) TDOe - Rework
###########################################################################


Beschreibung:
=============

Das Plugin plugin.program.newscenter gibt Skinnern die Möglichkeit einen Nachrichten-Feed als Widget in den Skin zu integrieren.
Zudem können folgende Direktlinks per Pluginaufruf erfolgen:
- Tagesschau
- Tagesschau in 100s
- Kinder Nachrichten (logo)
- Wettervideos


Das Widget kann in den Settings konfiguriert werden, welcher Feed angezeigt werden soll. Hierzu stehen folgende NachrichtenQuellen zur Verfügung:
- Spiegel Online
- n-tv
- tagesschau.de
- n24
- Heise
- Google News
- FOCUS-Online
- Die Welt
- Sport 1
- ...

Desweiteren verfügt das Plugin über ein JSON File, in welchem Aenderungen an den Feeds als auch Neue Feeds hinzugefügt werden können. 
(NewsFeeds.json)

Im Bereich Sport stellt das NewsCenter Plugin die aktuelle Tabelle der 1. und 2. Bundesliga dar.

Ein weiteres JSON File (Buli.json) dient der Zuordnung der Ligaid zu Mannschaft (Benötigt für Vereinslogo)




Skintegration:
==============

Um das News-Widget in Confluence zu aktivieren, sind mehrere Schritte notwendig.

Anmerkung:
----------

In der folgenden Anleitung sind die Beispielcodes so aufgebaut, dass Zuerst ein Stück Orginal Confluence Code kommt. 
Im Anschluss wird der hinzuzufügenden Code eingeleitet von der Präambel '<!-- Start NewsCenter -->', und endet mit '<!-- Ende NewsCenter -->', nun kommt noch ein Stück orginal Confluence Code. 


1. Dateien kopieren:
-------------------- 

Die Dateien "script-news.xml" und "script-news-wetter.xml" in den Confluence Skin-Ordner kopiert werden:

  # cp integration/script-news.xml integration/script-news-wetter.xml /usr/share/kodi/addon/skin.confluence/720p/


Die Datei "Custom_NewsCenter.xml" in den Confluence Skin-Ordner kopieren. (Juggers Custom Window)

  # cp integration/Custom_NewsCenter.xml /usr/share/kodi/addon/skin.confluence/720p/


Die Bilddateien aus dem integration Ordner in den Confluence Media Ordner kopieren:

  # cp integration/*.png /usr/share/kodi/addon/skin.confluence/media/


2. Änderungen an der Datei Home.xml:
------------------------------------

-------------------- 8< ----------[ Wetter-Submenü hinzufügen ]-------------
                <control type="group">
                        <depth>DepthMenu</depth>
                        <top>400</top>
                        <animation type="WindowOpen" reversible="false">
                                <effect type="zoom" start="80" end="100" center="640,360" easing="out" tween="back" time="225" />
                                <effect type="fade" start="0" end="100" time="225" />
                        </animation>
                        <animation type="WindowClose" reversible="false">
                                <effect type="zoom" start="100" end="80" center="640,360" easing="in" tween="back" time="225" />
                                <effect type="fade" start="100" end="0" time="225" />
                        </animation>

                        <control type="group" id="9001">
                                <depth>DepthMenu-</depth>
                                <left>0</left>
                                <top>70</top>
                                <onup>9000</onup>
                                <ondown>9002</ondown>
<!-- Start NewsCenter -->
                                <control type="grouplist" id="50506">
                                        <include>HomeSubMenuCommonValues</include>
                                        <onleft>9014</onleft>
                                        <onright>9014</onright>
                                        <visible>Container(9000).HasFocus(7)</visible>
                                        <!-- Buttons for the grouplist -->
                                        <include>HomeSubMenuNewsWetter</include>
                                </control>
<!-- Ende NewsCenter -->
                                <control type="grouplist" id="9010">
                                        <include>HomeSubMenuCommonValues</include>
                                        <onleft>9010</onleft>
                                        <onright>9010</onright>
                                        <visible>Container(9000).HasFocus(2)</visible>
                                        <!-- Buttons for the grouplist -->
                                        <include>HomeSubMenuVideos</include>
                                </control>
-------------------- >8 -----------------------
.
.
.
.
.
-------------------- 8< ----------[ News Submenü hinzufügen ]-------------
                                <control type="grouplist" id="9016">
                                        <include>HomeSubMenuCommonValues</include>
                                        <onleft>9014</onleft>
                                        <onright>9014</onright>
                                        <visible>Container(9000).HasFocus(13)</visible>
                                        <!-- Buttons for the grouplist -->
                                        <include>HomeSubMenuRadio</include>
                                </control>
<!-- NewsCenter Start -->
                                <control type="grouplist" id="50506">
                                        <include>HomeSubMenuCommonValues</include>
                                        <onleft>9014</onleft>
                                        <onright>9014</onright>
                                        <visible>Container(9000).HasFocus(50505)</visible>
                                        <!-- Buttons for the grouplist -->
                                        <include>HomeSubMenuNews</include>
                                </control>
<!-- NewsCenter Ende -->
                        </control>
                        <control type="image">
                                <left>-100</left>
                                <top>0</top>
                                <width>1480</width>
                                <height>75</height>
                                <texture border="0,6,0,6">HomeBack.png</texture>
                        </control>

-------------------- >8 -----------------------
.
.
.
.
.
-------------------- 8< ----------[ News Button einfügen ]-------------
                                <content>
<!-- NewsCenter Start -->
                                        <item id="50505">
                                                <label>NEWS</label>
                                                <onclick>ActivateWindow(4117)</onclick>
                                                <icon>-</icon>
                                                <thumb>-</thumb>
                                                <visible>System.HasAddon(plugin.program.newscenter)</visible>
                                        </item>
<!-- NewsCenter Ende -->
                                        <item id="7">
                                                <label>31950</label>
                                                <onclick>ActivateWindow(Weather)</onclick>
                                                <icon>-</icon>
                                                <thumb>-</thumb>
                                                <visible>!Skin.HasSetting(HomeMenuNoWeatherButton) + !IsEmpty(Weather.Plugin)</visible>
                                        </item>
-------------------- >8 -----------------------
.
.
.
.
.
-------------------- 8< -----------------------
                <control type="group" id="9002">
                        <depth>DepthMenu</depth>
                        <onup>9001</onup>
                        <ondown>20</ondown>
                        <control type="fixedlist" id="700">
                                <animation effect="slide" start="0,0" end="-91,0" time="0" condition="StringCompare(Container(700).NumItems,2) | StringCompare(Container(700).NumItems,4)">conditional</animation>
                                <visible>Container(9000).HasFocus(2) | Container(9000).HasFocus(10) | Container(9000).HasFocus(11)</visible>
                                <onleft>700</onleft>
                                <onright>700</onright>
                                <onup>9001</onup>
                                <ondown>20</ondown>
                                <include>HomeAddonsCommonLayout</include>
                                <content>
                                        <include>HomeAddonItemsVideos</include>
                                </content>
                        </control>
<!-- NewsCenter Start -->
                        <control type="fixedlist" id="50509">
                                <animation effect="slide" start="0,0" end="-91,0" time="0" condition="StringCompare(Container(703).NumItems,2) | StringCompare(Container(703).NumItems,4)">conditional</animation>
                                <visible>Container(9000).HasFocus(50505)</visible>
                                <onleft>703</onleft>
                                <onright>703</onright>
                                <onup>9001</onup>
                                <ondown>20</ondown>
                                <include>HomeAddonsCommonLayout</include>
                                <content>
                                        <include>HomeAddonItemsNews</include>
                                </content>
                        </control>
<!-- NewsCenter Ende -->



                        <control type="fixedlist" id="703">
-------------------- >8 -----------------------
.
.
.
.
.
-------------------- 8< ----------[ Warnsymbol bei Unwetter ]-------------
                        <control type="image">
                                <description>Power Icon</description>
                                <left>60</left>
                                <top>5</top>
                                <width>35</width>
                                <height>35</height>
                                <aspectratio>keep</aspectratio>
                                <texture>icon_power.png</texture>
                        </control>

<!-- NewsCenter Start -->
                        <control type="image">
                                <description>Unwetter Icon</description>
                                <left>1200</left>
                                <top>5</top>
                                <width>35</width>
                                <height>35</height>
                                <aspectratio>keep</aspectratio>
                                <texture>wetterwarnung.png</texture>
                                <visible>!StringCompare(Window(Home).Property(NewsCenter.Unwetter.Anzahl),0) + SubString(Window(Home).Property(NewsCenter.Visible.UnwetterWarnIcon),true)</visible>
                        </control>
<!-- NewsCenter Ende -->

                        <control type="button" id="21">
                                <description>Favourites push button</description>
                                <left>0</left>
                                <top>0</top>
                                <width>45</width>
                                <height>45</height>
                                <label>1036</label>
                                <font>-</font>
                                <onclick>ActivateWindow(Favourites)</onclick>
-------------------- >8 -----------------------




3. Änderungen an der Datei IncludesHomeMenuItems.xml:
-----------------------------------------------------

-------------------- 8< ----------[ Submenü Content ]-------------
<?xml version="1.0" encoding="UTF-8"?>
<includes>

<!-- Start NewsCenter -->
        <include name="HomeSubMenuNews">


                <control type="image" id="50100">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3" flipx="true">HomeSubEnd.png</texture>
                </control>

                <control type="button" id="50115">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Tagesschau in 100s</label>
                        <visible>SubString(Window(Home).Property(NewsCenter.Visible.Tagesschau100), true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_tagesschau_100")</onclick>
                </control>
                <control type="button" id="50101">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Tagesschau</label>
                        <visible>SubString(Window(Home).Property(NewsCenter.Visible.Tagesschau), true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_tagesschau")</onclick>
                </control>
                <control type="button" id="50118">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>MDR Aktuell 130s</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.NDRKompakt),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_mdr_aktuell_130")</onclick>
                </control>
                <control type="button" id="50119">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Kinder News</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.KinderNachrichten),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_kinder_nachrichten")</onclick>
                </control>
                <control type="button" id="50120">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>BR Rundschau 100s</label>
                        <visible>SubString(Window(Home).Property(NewsCenter.Visible.BRRundschau100),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_rundschau100")</onclick>
                </control>
                <control type="button" id="50121">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>NDR Aktuell kompakt</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.NDRKompakt),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_ndraktuellkompakt")</onclick>
                </control>


                <control type="button" id="50116">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Feed Auswahl</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_select_dialog")</onclick>
                </control>

                <control type="button" id="50122">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Live</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_livestream_select_dialog")</onclick>
                </control>

                <control type="button" id="50117">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Sport</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_buli_select")</onclick>
                </control>

                <control type="image" id="90126">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3">HomeSubEnd.png</texture>
                </control>
        </include>


        <include name="HomeSubMenuNewsWetter">


                <control type="image" id="561001">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3" flipx="true">HomeSubEnd.png</texture>
                </control>
                <control type="button" id="561021">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Wetter in 60s</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.Wetter60),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_wetteronline")</onclick>
                </control>
                <control type="button" id="561031">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Wetter.info</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.WetterInfo),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_wetterinfo")</onclick>
                </control>
                <control type="button" id="561032">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Wetter.net</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.WetterNet),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_wetternet")</onclick>
                </control>
                <control type="button" id="561033">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Tagesschau Wetter</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.TagesschauWetter),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_tagesschauwetter")</onclick>
                </control>
                <control type="button" id="561034">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Unwetter Karten</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_wetter_karte")</onclick>
                </control>
                <control type="button" id="561035">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Unwetter Warnungen</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_unwetter_warnungen")</onclick>
                        <visible>!StringCompare(Window(Home).Property(NewsCenter.Unwetter.Anzahl),0)</visible>
                </control>


                <control type="image" id="90126">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3">HomeSubEnd.png</texture>
                </control>
        </include>
<!-- Ende NewsCenter -->

	<include name="HomeSubMenuVideos">
		<control type="image" id="90101">
			<width>35</width>
			<height>35</height>
			<texture border="0,0,0,3" flipx="true">HomeSubEnd.png</texture>
		</control>
-------------------- >8 -----------------------



4. Änderungen an der Datei IncludesHomeRecentlyAdded.xml:
---------------------------------------------------------

-------------------- 8< -----------------------
<?xml version="1.0" encoding="UTF-8"?>
<includes>
        <include name="HomeRecentlyAddedInfo">
                <control type="group" id="9003">
                        <depth>DepthMenu</depth>
                        <onup>20</onup>
                        <ondown condition="System.HasAddon(script.globalsearch)">608</ondown>
                        <ondown condition="!System.HasAddon(script.globalsearch)">603</ondown>
                        <visible>!Window.IsVisible(Favourites)</visible>
                        <include>VisibleFadeEffect</include>
                        <animation effect="fade" time="225" delay="750">WindowOpen</animation>
                        <animation effect="fade" time="150">WindowClose</animation>
<!-- Start NewsCenter -->
                        <include>HomeRecentlyAddedNewsInfo</include>
                        <include>HomeRecentlyAddedNewsWetterInfo</include>
<!-- Ende NewsCenter -->

                        <control type="group">
                                <left>190</left>
                                <top>50</top>
                                <visible>Library.HasContent(Movies)</visible>
                                <visible>Container(9000).Hasfocus(10) + !Skin.HasSetting(HomepageHideRecentlyAddedVideo)</visible>
                                <include>VisibleFadeEffect</include>
                                <control type="label">
                                        <description>Title label</description>
                                        <left>180</left>
                                        <top>220</top>
                                        <height>20</height>
                                        <width>540</width>
                                        <label>20386</label>
                                        <align>center</align>
                                        <aligny>center</aligny>
                                        <font>font12_title</font>
                                        <textcolor>white</textcolor>
                                        <shadowcolor>black</shadowcolor>
                                </control>
                                <control type="list" id="8000">
-------------------- >8 -----------------------


5. Änderungen an der Datei includes.xml:
----------------------------------------

-------------------- 8< -----------------------
<?xml version="1.0" encoding="UTF-8"?>
<includes>
        <include file="defaults.xml" />
        <include file="ViewsVideoLibrary.xml" />
        <include file="ViewsMusicLibrary.xml" />
        <include file="ViewsFileMode.xml" />
        <include file="ViewsPictures.xml" />
        <include file="ViewsAddonBrowser.xml" />
        <include file="ViewsLiveTV.xml" />
        <include file="ViewsPVRGuide.xml" />
        <include file="ViewsWeather.xml" />
        <include file="IncludesCodecFlagging.xml" />
        <include file="IncludesHomeRecentlyAdded.xml" />
<!-- NewsCenter Start -->
        <include file="script-news.xml" />
        <include file="script-news-wetter.xml" />
<!-- NewsCenter Ende -->
        <include file="IncludesHomeMenuItems.xml" />
        <include file="IncludesPVR.xml" />
        <include file="IncludesBackgroundBuilding.xml" />

-------------------- >8 -----------------------







Parametrisierung bei Pluginaufrufes:
====================================
Wird das Plugin ohne Parameter gestartet, wird der Service auf "aktiv" gesetzt und die Daten passend zu den vorgenommenen Einstellungen werden in regelmäßigen Abständen aktualisiert.



XBMC.RunScript(plugin.program.newscenter,"?methode=start_service")
  Markiert den Service als aktiv, Daten werden geholt.

XBMC.RunScript(plugin.program.newscenter,"?methode=stop_service")
  Markiert den Service als gestoppt, es werden keine Daten mehr geholt.

Start und Stop Service ist nur im Skinnermode aktiv. Wenn Skinnermode nicht aktiviert wurde, lÃ¤uft immer ein Update
solange Content Refresh nicht auf 0 gesetzt ist.




XBMC.RunScript(plugin.program.newscenter,"?methode=play_tagesschau")
  Startet letzte Folge der Tagesschau

XBMC.RunScript(plugin.program.newscenter,"?methode=play_tagesschau_100")
  Startet letzte Folge der Tagesschau in 100 Sekunden

XBMC.RunScript(plugin.program.newscenter,"?methode=play_wetteronline")
  Startet aktuellen Wetterbericht in 60 Sekunden

XBMC.RunScript(plugin.program.newscenter,"?methode=play_wetterinfo")
  Startet aktuellen Wetterbericht von Meteogroup

XBMC.RunScript(plugin.program.newscenter,"?methode=play_kinder_nachrichten")
  Startet letzte Folge der Kinder Nachrichtensendung logo

XBMC.RunScript(plugin.program.newscenter,"?methode=show_select_dialog")
  Oeffnet Auswahlfendster fuer angezeigten Skin (switch ist temporär)

XBMC.RunScript(plugin.program.newscenter,"?methode=set_default_feed")
  Oeffnet Auswahlfendster fuer Default Feed (permanent)  

- show_select_dialog
- show_buli_select
- show_bulilist (benötigt Parameter buliliga=[1|2] & bulipage=[1|2]
- show_livestream_select_dialog


Methoden Auflistung:
====================


Dienst:
=======
methode=start_service
methode=stop_service
methode=set_skinmode
methode=unset_skinmode
methode=set_default_feed
methode=get_uwz_count
methode=refresh

Videos:
=======
methode=play_tagesschau
methode=play_tagesschau_100
methode=play_wetteronline
methode=play_wetterinfo
methode=play_wetternet
methode=play_tagesschauwetter
methode=play_kinder_nachrichten
methode=play_mdr_aktuell_130
methode=play_rundschau100
methode=play_ndraktuellkompakt

Livestreams:
============
methode=play_livestream_euronews
methode=play_livestream_ntv
methode=play_livestream_n24
methode=play_livestream_tagesschau24
methode=play_livestream_phoenix
methode=play_livestream_dw


Dialoge:
========
methode=show_select_dialog
methode=show_livestream_select_dialog
methode=show_buli_select
methode=show_bulilist
methode=show_bulispielplan
methode=show_bulinaechsterspieltag
methode=show_unwetter_warnungen


Container:
==========
methode=get_buli_spielplan_items
methode=get_buli_table_items
methode=get_buli_naechsterspieltag_items
methode=get_feed_items
methode=get_pollen_items
methode=get_unwetter_warnungen


Wetterkarten-Container:
=======================
methode=get_dwd_pics_base
methode=get_dwd_pics_base_uwz
methode=get_dwd_pics_extended
methode=get_dwd_pics_bundesland
methode=get_dwd_pics_bundesland_uwz
methode=get_dwd_pics_base_extended
methode=get_euronews_wetter_pics
methode=get_uwz_maps



Properties:
===========

LatestNews.Service                    - (active/inactive) Schaltet im Skinnermodus den Datenrefresh ein/aus

LatestNews.<nr>.Title                 - RSS Titel
LatestNews.<nr>.Desc                  - RSS Beschreibung
LatestNews.<nr>.Logo                  - RSS Bild
LatestNews.<nr>.Date                  - RSS Artikel Veröffentlichung
LatestNews.<nr>.HeaderPic             - RSS Provider Bild

NewsCenter.PLZ                        - Postleitzahl aus den Settings
NewsCenter.Bundesland                 - Ermitteltes Bundesland (von PLZ)

NewsCenter.Unwetter.Anzahl            - Anzahl Unwetterwarnungen
