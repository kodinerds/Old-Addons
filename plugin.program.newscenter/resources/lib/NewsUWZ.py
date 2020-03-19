#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import datetime
import urllib2
import json
import sys



class NewsUWZ():
    def __init__(self):
        url=''

##########################################################################################################################
##
##########################################################################################################################
    def WarnAnzahl(self,cc,plz):
        WINDOW = xbmcgui.Window( 10000 )
        Country=cc
        PLZ=plz
        baseurl="http://feed.alertspro.meteogroup.com/AlertsPro/AlertsProPollService.php?method=getWarning&language=de&areaID=UWZ%s%s" % (Country,PLZ)
        req = urllib2.urlopen(baseurl)
        content = req.read().decode('cp1252').encode('utf-8')
        UWZWarnings = json.loads(content)
        #debug("Anzahl Warnungen: %s" % (len(UWZWarnings['results'])))
        WINDOW.setProperty( "NewsCenter.Unwetter.Anzahl", str(len(UWZWarnings['results'])) )
    

##########################################################################################################################
##
##########################################################################################################################
    def Warnungen(self,cc,plz):

        addon        = xbmcaddon.Addon()
        addonID      = addon.getAddonInfo('id')
        addonFolder  = xbmc.translatePath('special://home/addons/'+addonID).decode('utf-8')
        addon_handle = int(sys.argv[1])



        WINDOW = xbmcgui.Window( 10000 )
        Country=cc
        PLZ=plz
        baseurl="http://feed.alertspro.meteogroup.com/AlertsPro/AlertsProPollService.php?method=getWarning&language=de&areaID=UWZ%s%s" % (Country,PLZ)
        req = urllib2.urlopen(baseurl)
        content = req.read().decode('cp1252').encode('utf-8')
        UWZWarnings = json.loads(content)
    
        typenames = [{ "type":"1", "name":"unknown"},     # <===== FIX HERE
                     { "type":"2", "name":"sturm"},
                     { "type":"3", "name":"schnee"},
                     { "type":"4", "name":"regen"},
                     { "type":"5", "name":"temperatur"},
                     { "type":"6", "name":"waldbrand"},
                     { "type":"7", "name":"gewitter"},
                     { "type":"8", "name":"strassenglaette"},
                     { "type":"9", "name":"temperatur"},    # 9 = hitzewarnung
                     { "type":"10", "name":"glatteisregen"},
                     { "type":"11", "name":"temperatur"}] #bodenfrost
        severitycolor = [{ "severity":"0", "name":"green"},
                         { "severity":"1", "name":"green"}, # <===== FIX HERE
                         { "severity":"2", "name":"unknown"}, # <===== FIX HERE
                         { "severity":"3", "name":"unknown"}, # <===== FIX HERE
                         { "severity":"4", "name":"orange"},
                         { "severity":"5", "name":"unknown"}, # <===== FIX HERE
                         { "severity":"6", "name":"unknown"}, # <===== FIX HERE
                         { "severity":"7", "name":"orange"},
                         { "severity":"8",  "name":"gelb"},
                         { "severity":"9",  "name":"gelb"}, # <===== FIX HERE
                         { "severity":"10",  "name":"orange"},
                         { "severity":"11",  "name":"rot"},
                         { "severity":"12",  "name":"violet"}]
        df = xbmc.getRegion('dateshort')
        tf = xbmc.getRegion('time').split(':')
        DATEFORMAT = df + '  -  ' + tf[0][0:2] + ':' + tf[1] + ' Uhr'
        WINDOW.setProperty( "NewsCenter.Unwetter.Anzahl", str(len(UWZWarnings['results'])) )
    
        for UWZWarning in UWZWarnings['results']:
            for tn in typenames:
                if int(tn['type']) == int(UWZWarning['type']):
                    typename = tn['name']
                    break
            for sc in severitycolor:
                if int(sc['severity']) == int(UWZWarning['severity']):
                    severitycol = sc['name']
                    break
            picurl="http://www.unwetterzentrale.de/images/icons/%s-%s.gif" % (typename,severitycol)
            url   = "-"
            start = datetime.datetime.fromtimestamp( int(UWZWarning['dtgStart']) ).strftime(DATEFORMAT)
            ende  = datetime.datetime.fromtimestamp( int(UWZWarning['dtgEnd']) ).strftime(DATEFORMAT)
            li    = xbmcgui.ListItem(UWZWarning['payload']['translationsShortText']['DE'].encode('utf-8'), iconImage=picurl)
            li.setProperty("Start", str(start))
            li.setProperty("Ende", str(ende))
            li.setProperty("Severity", str(UWZWarning['severity']))
            li.setProperty("UWZLevel", str(UWZWarning['payload']['uwzLevel']))
            li.setProperty("Type", typename.capitalize())
            li.setProperty("LongText", UWZWarning['payload']['translationsLongText']['DE'].encode('utf-8'))
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
        return addon_handle
    
