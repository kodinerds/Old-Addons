#!/usr/bin/python
# -*- coding: utf-8 -*-


import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import json
import random
import sys
import urllib2
import re

class NewsCenterGeoHelper():
    def __init__(self):
        url=''

##########################################################################################################################
##
##########################################################################################################################
    def plz2bundesland(self,plz):
        addon      = xbmcaddon.Addon()
        addonID    = addon.getAddonInfo('id')

        BundFile = xbmc.translatePath('special://home/addons/'+addonID+'/BundeslandPLZ.json')
        with open(BundFile, 'r') as PLZTrans:
            content=PLZTrans.read().rstrip('\n').decode('utf-8')
        PLZJson = json.loads(content)
        #debug('plz2bundesland')
    
        for i in PLZJson:
            if (plz >= i['start']) and (plz <= i['ende']):
                return i['bundesland']
        return 0    

    def plz2ort(self,plz):
        url = "http://www1.dasoertliche.de/Controller?zvo_ok=&book=&plz=&quarter=&district=&ciid=&pc=%s&image=Finden&buc=&kgs=&searchType=plz&buab=&zbuab=&page=210&context=5&action=43&form_name=search_pc" % (plz)
        req = urllib2.urlopen(url)
        content = req.read()
        ort = re.compile('<input type="hidden" name="ci" value="(.+?)"/>', re.DOTALL).findall(content)[0]
        ort = unicode(ort, "ISO-8859-15")
        return ort
    
    



class NewsWetterKarten():

    def __init__(self):
        # do variable init
        url=''


##########################################################################################################################
##
##########################################################################################################################
    def dwdshorter(self,Bundesland):
        short = {
            "Bayern": "bay",
            "Baden-Württemberg": "baw",
            "Brandenburg": "bbb",
            "Berlin": "bbb",
            "Hessen": "hes",
            "Mecklenburg-Vorpommern": "mvp",
            "Niedersachsen": "nib",
            "Bremen": "nib",
            "Nordrhein-Westfalen": "nrw",
            "Rheinland-Pfalz": "rps",
            "Saarland": "rps",
            "Sachsen": "sac",
            "Sachsen-Anhalt": "saa",
            "Schleswig-Holstein": "shh",
            "Thüringen": "thu",
            "Hamburg": "shh"
        }
        return short.get(Bundesland, "brd")
    
    def plz2uwzmap(self,plz):
        gh = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        #debug("Bundesland=%s" % (Bundesland) )
        if Bundesland == "Bayern":
            pic="http://www.unwetterzentrale.de/images/map/bayern_index.png"
        elif "Baden-W" in Bundesland:
            pic="http://www.unwetterzentrale.de/images/map/badenwuerttemberg_index.png"
        elif (Bundesland == "Brandenburg") or (Bundesland == "Berlin"):
            pic="http://www.unwetterzentrale.de/images/map/brandenburg_index.png"
        elif Bundesland == "Hessen":
            pic="http://www.unwetterzentrale.de/images/map/hessen_index.png"
        elif Bundesland == "Mecklenburg-Vorpommern":
            pic="http://www.unwetterzentrale.de/images/map/meckpom_index.png"
        elif (Bundesland == "Niedersachsen") or (Bundesland == "Bremen"):
            pic="http://www.unwetterzentrale.de/images/map/niedersachsen_index.png"
        elif Bundesland == "Nordrhein-Westfalen":
            pic="http://www.unwetterzentrale.de/images/map/nrw_index.png"
        elif (Bundesland == "Rheinland-Pfalz") or (Bundesland == "Saarland"):
            pic="http://www.unwetterzentrale.de/images/map/rlp_index.png"
        elif Bundesland == "Sachsen":
            pic="http://www.unwetterzentrale.de/images/map/sachsen_index.png"
        elif Bundesland == "Sachsen-Anhalt":
            pic="http://www.unwetterzentrale.de/images/map/sachsenanhalt_index.png"
        elif (Bundesland == "Schleswig-Holstein") or (Bundesland == "Hamburg"):
            pic="http://www.unwetterzentrale.de/images/map/schleswig_index.png"
        elif "ringen" in Bundesland:
            pic="http://www.unwetterzentrale.de/images/map/thueringen_index.png"
        else:
            pic="http://www.unwetterzentrale.de/images/map/deutschland_index.png"
        pic = "%s?%04.0f" % (pic,random.uniform(10000, 99999))
        return pic
    












##########################################################################################################################
##
##########################################################################################################################
    def DWD_Base(self,clickable=1):
        addon      = xbmcaddon.Addon()
        plz        = addon.getSetting('plz')
        gh         = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        rand       = "?%04.0f" % (random.uniform(10000, 99999))
        url        = ''
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_deutschland.jpg%s' % (rand)
        li = xbmcgui.ListItem('Deutschland aktuell', iconImage='http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_deutschland.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(self, url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/vhs_deutschland.jpg%s' % (rand)
        li = xbmcgui.ListItem('Deutschland morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/vhs_deutschland.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/trendpic.jpg%s' % (rand)
        li = xbmcgui.ListItem('Deutschland 2.-4. Tag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/trendpic.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/europa/film/europavhs.jpg%s' % (rand)
        li = xbmcgui.ListItem('Europa morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/europavhs.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/welt/film/vhs_welt.jpg%s' % (rand)
        li = xbmcgui.ListItem('Welt morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/welt/film/vhs_welt.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
    

##########################################################################################################################
##
##########################################################################################################################
    def DWD_Base_UWZ(self,clickable=1):
        addon      = xbmcaddon.Addon()
        plz        = addon.getSetting('plz')
        gh         = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        rand       = "?%04.0f" % (random.uniform(10000, 99999))
        url        = ''
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_deutschland.jpg%s' % (rand)
        li = xbmcgui.ListItem('Deutschland aktuell', iconImage='http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_deutschland.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/vhs_deutschland.jpg%s' % (rand)
        li = xbmcgui.ListItem('Deutschland morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/vhs_deutschland.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)

        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/trendpic.jpg%s' % (rand)    
        li = xbmcgui.ListItem('Deutschland 2.-4. Tag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/trendpic.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/europa/film/europavhs.jpg%s' % (rand)
        li = xbmcgui.ListItem('Europa morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/europavhs.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/welt/film/vhs_welt.jpg%s' % (rand)
        li = xbmcgui.ListItem('Welt morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/welt/film/vhs_welt.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url="http://www.unwetterzentrale.de/images/map/deutschland_index.png"
        li = xbmcgui.ListItem("Unwetterkarte von Deutschland", iconImage=url)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
    
    

##########################################################################################################################
##
##########################################################################################################################
    def DWD_Bundesland(self,clickable=1):
        addon      = xbmcaddon.Addon()
        plz        = addon.getSetting('plz')
        gh         = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        bl         = self.dwdshorter(Bundesland)
        rand       = "?%04.0f" % (random.uniform(10000, 99999))
        url        = ''
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_%s_akt.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('%s aktuell' % (Bundesland), iconImage='http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_%s_akt.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/radar/rad_%s_akt.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Niederschlagsradar', iconImage='http://www.dwd.de/DWD/wetter/radar/rad_%s_akt.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/radar/radfilm_%s_akt.gif%s' % (bl,rand)
        li = xbmcgui.ListItem('Niederschlagsradar Film', iconImage='http://www.dwd.de/DWD/wetter/radar/radfilm_%s_akt.gif%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_start.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_start.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutefrueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutefrueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutemittag.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Mittag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutemittag.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutespaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutespaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutenacht.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Nacht', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutenacht.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenfrueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Morgen Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenfrueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenspaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Morgen Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenspaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenfrueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Übermorgen Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenfrueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenspaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Übermorgen Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenspaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4frueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage 4. Tag Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4frueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4spaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage 4. Tag Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4spaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/trendpic_%s.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Wettertrend', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/trendpic_%s.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
    
        
##########################################################################################################################
##
##########################################################################################################################
    def DWD_Bundesland_UWZ(self,clickable=1):
        addon      = xbmcaddon.Addon()
        plz        = addon.getSetting('plz')
        gh         = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        bl         = self.dwdshorter(Bundesland)
        rand       = "?%04.0f" % (random.uniform(10000, 99999))
        url        = ''
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_%s_akt.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('%s aktuell' % (Bundesland), iconImage='http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_%s_akt.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/radar/rad_%s_akt.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Niederschlagsradar', iconImage='http://www.dwd.de/DWD/wetter/radar/rad_%s_akt.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/radar/radfilm_%s_akt.gif%s' % (bl,rand)
        li = xbmcgui.ListItem('Niederschlagsradar Film', iconImage='http://www.dwd.de/DWD/wetter/radar/radfilm_%s_akt.gif%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_start.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_start.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutefrueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutefrueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutemittag.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Mittag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutemittag.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutespaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutespaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutenacht.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Heute Nacht', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_heutenacht.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenfrueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Morgen Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenfrueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenspaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Morgen Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_morgenspaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenfrueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Übermorgen Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenfrueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenspaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage Übermorgen Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_uebermorgenspaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4frueh.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage 4. Tag Früh', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4frueh.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4spaet.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Vorhersage 4. Tag Spät', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/vhs_%s_tag4spaet.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/trendpic_%s.jpg%s' % (bl,rand)
        li = xbmcgui.ListItem('Wettertrend', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/bilder/trendpic_%s.jpg%s' % (bl,rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url = self.plz2uwzmap(plz)
        li = xbmcgui.ListItem("Unwetterkarte von %s" % (Bundesland), iconImage=self.plz2uwzmap(plz))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
    

##########################################################################################################################
##
##########################################################################################################################
    def DWD_Extended(self,clickable=1):
        rand = "?%04.0f" % (random.uniform(10000, 99999))
        url  = ''
    
        if clickable == 1:
            url='http://www.dwd.de/DWD/wetter/radar/radarfilm_dl_720.mp4'
        li = xbmcgui.ListItem('Deutschland Radarfilm', iconImage='http://www.dwd.de/DWD/wetter/radar/vorschau_radarfilm_dl.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vhs_EU_Wo_Nieder_720.mp4'
        li = xbmcgui.ListItem('Europa Wolken und Niederschlag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vorschau_vhs_EU_Wo_Nieder.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vhs_Europa_Wind_720.mp4'
        li = xbmcgui.ListItem('Europa Wind', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vorschau_vhs_Europa_Wind.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
    

##########################################################################################################################
##
##########################################################################################################################
    def DWD_Base_Extended(self,clickable=1):
        addon      = xbmcaddon.Addon()
        plz        = addon.getSetting('plz')
        gh         = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        rand       = "?%04.0f" % (random.uniform(10000, 99999))
        url        = ''
   
        if clickable == 1:
            url = 'http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_deutschland.jpg%s' % (rand) 
        li = xbmcgui.ListItem('Deutschland aktuell', iconImage='http://www.dwd.de/DWD/wetter/aktuell/deutschland/bilder/wx_deutschland.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url ='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/vhs_deutschland.jpg%s' % (rand)
        li = xbmcgui.ListItem('Deutschland morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/vhs_deutschland.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)

        if clickable == 1:
            url ='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/trendpic.jpg%s' % (rand)    
        li = xbmcgui.ListItem('Deutschland 2.-4. Tag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/deutschland/film/trendpic.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url ='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/europavhs.jpg%s' % (rand)
        li = xbmcgui.ListItem('Europa morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/europavhs.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url ='http://www.dwd.de/DWD/wetter/wv_allg/welt/film/vhs_welt.jpg%s' % (rand)
        li = xbmcgui.ListItem('Welt morgen', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/welt/film/vhs_welt.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url='http://www.dwd.de/DWD/wetter/radar/radarfilm_dl_720.mp4'
        li = xbmcgui.ListItem('Deutschland Radarfilm', iconImage='http://www.dwd.de/DWD/wetter/radar/vorschau_radarfilm_dl.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vhs_EU_Wo_Nieder_720.mp4'
        li = xbmcgui.ListItem('Europa Wolken und Niederschlag', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vorschau_vhs_EU_Wo_Nieder.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vhs_Europa_Wind_720.mp4'
        li = xbmcgui.ListItem('Europa Wind', iconImage='http://www.dwd.de/DWD/wetter/wv_allg/europa/film/vorschau_vhs_Europa_Wind.jpg%s' % (rand))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
    
    
    

##########################################################################################################################
##
##########################################################################################################################
    def Euronews(self,clickable=1):
        url        = ''
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_summary_today.gif'
        li = xbmcgui.ListItem('Wettervorhersage Heute', iconImage='http://de.euronews.com/import/reg05_summary_today.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_summary_tonight.gif'
        li = xbmcgui.ListItem('Wettervorhersage Heute Nacht', iconImage='http://de.euronews.com/import/reg05_summary_tonight.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_summary_tomorrow.gif'
        li = xbmcgui.ListItem('Wettervorhersage Morgen', iconImage='http://de.euronews.com/import/reg05_summary_tomorrow.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_winds_today.gif'
        li = xbmcgui.ListItem('Wind Heute', iconImage='http://de.euronews.com/import/reg05_winds_today.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_winds_tonight.gif'
        li = xbmcgui.ListItem('Wind Heute Nacht', iconImage='http://de.euronews.com/import/reg05_winds_tonight.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_winds_tomorrow.gif'
        li = xbmcgui.ListItem('Wind Morgen', iconImage='http://de.euronews.com/import/reg05_winds_tomorrow.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_temp_today.gif'
        li = xbmcgui.ListItem('Temperaturen Heute', iconImage='http://de.euronews.com/import/reg05_temp_today.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_temp_tonight.gif'
        li = xbmcgui.ListItem('Temperaturen Heute Nacht', iconImage='http://de.euronews.com/import/reg05_temp_tonight.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_temp_tomorrow.gif'
        li = xbmcgui.ListItem('Temperaturen Morgen', iconImage='http://de.euronews.com/import/reg05_temp_tomorrow.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_precip_today.gif'
        li = xbmcgui.ListItem('Regen Heute', iconImage='http://de.euronews.com/import/reg05_precip_today.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        if clickable == 1:
            url= 'http://de.euronews.com/import/reg05_precip_tonight.gif'
        li = xbmcgui.ListItem('Regen Heute Nacht', iconImage='http://de.euronews.com/import/reg05_precip_tonight.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)

        if clickable == 1:
            url = 'http://de.euronews.com/import/reg05_precip_tomorrow.gif'    
        li = xbmcgui.ListItem('Regen Morgen', iconImage='http://de.euronews.com/import/reg05_precip_tomorrow.gif')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
        return int(sys.argv[1])
    
    
##########################################################################################################################
##
##########################################################################################################################
    def UWZ(self,clickable=1):
        addon      = xbmcaddon.Addon()
        plz        = addon.getSetting('plz')
        gh         = NewsCenterGeoHelper()
        Bundesland = gh.plz2bundesland(plz).encode('utf-8')
        url        = ''

        if clickable == 1:
            url = self.plz2uwzmap(plz)
        li = xbmcgui.ListItem("Unwetterkarte von %s" % (Bundesland), iconImage=self.plz2uwzmap(plz))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        karteDE = "http://www.unwetterzentrale.de/images/map/deutschland_index.png"
        if clickable == 1:
            url = karteDE
        li = xbmcgui.ListItem("Unwetterkarte von Deutschland", iconImage=karteDE)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url=url, listitem=li)
    
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return int(sys.argv[1])
