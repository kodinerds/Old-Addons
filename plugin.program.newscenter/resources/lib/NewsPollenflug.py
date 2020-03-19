#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
import os
import datetime
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from xml.dom.minidom import parseString

class NewsPollenflug():
    def __init__(self):
        url=''


##########################################################################################################################
##
##########################################################################################################################
    def numbers_to_weekdaystring(self,argument):
        num2string = {
            0: "Montag",
            1: "Dienstag",
            2: "Mittwoch",
            3: "Donnerstag",
            4: "Freitag",
            5: "Samstag",
            6: "Sonntag"
        }
        return num2string.get(argument, "nothing")
 
##########################################################################################################################
##
##########################################################################################################################
    def pollenpics(self,polle):
        addon     = xbmcaddon.Addon()
        addonID   = addon.getAddonInfo('id')
        mediaPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/skins/Default/media/')
        mediapath = "%sPollenpics/" % (mediaPath)
        polle2pic = {
            "Ambrosia": "%sambrosia.jpg" % (mediapath),
            "Ampfer": "%sampfer.jpg" % (mediapath),
            "Beifuss": "%sbeifuss.jpg" % (mediapath),
            "Birke": "%sbirke.jpg" % (mediapath),
            "Buche": "%sbuche.jpg" % (mediapath),
            "Eiche": "%seiche.jpg" % (mediapath),
            "Erle": "%serle.jpg" % (mediapath),
            "Esche": "%sesche.jpg" % (mediapath),
            "Graeser": "%sgraeser.jpg" % (mediapath),
            "Hasel": "%shasel.jpg" % (mediapath),
            "Pappel": "%spappel.jpg" % (mediapath),
            "Roggen": "%sroggen.jpg" % (mediapath),
            "Ulme": "%sulme.jpg" % (mediapath),
            "Wegerich": "%swegerich.jpg" % (mediapath),
            "Weide": "%sweidenkaetzchen.jpg" % (mediapath)
        }
        return polle2pic.get(polle, "nothing")
    
    
   

##########################################################################################################################
##
##########################################################################################################################
    def get_pollen_items(self):
        addon        = xbmcaddon.Addon()
        addonID      = addon.getAddonInfo('id')
        addonFolder  = xbmc.translatePath('special://home/addons/'+addonID).decode('utf-8')
        icon         = os.path.join(addonFolder, "icon.png")
        plz          = addon.getSetting('plz')
        url          = "http://www.allergie.hexal.de/pollenflug/xml-interface-neu/pollen_de_7tage.php?plz=%s" % (plz)
        response     = urllib.urlopen(url)
        dom          = parseString(response.read())
        url          = '-'
        addon_handle = int(sys.argv[1]) 
        for node in dom.getElementsByTagName('pollenbelastungen'):
            Tag = node.getAttribute("tag").strip()
            if int(Tag) == int(0):
                tagname="Heute"
            elif int(Tag) == int(1):
                tagname="Morgen"
            elif int(Tag) == int(2):
                tagname="Übermorgen"
            else:
                tagname=self.numbers_to_weekdaystring((datetime.date.today() + datetime.timedelta(int(Tag))).weekday())
            datum=datetime.date.today() + datetime.timedelta(int(Tag))
            li = xbmcgui.ListItem(tagname.decode('utf-8'), iconImage=icon)
            li.setLabel2(datum.strftime('%d.%m.%Y'))
            i=0
            for snode in node.getElementsByTagName('pollen'):
                Name = snode.getAttribute("name").encode('utf-8').replace('ß','ss').replace('ä','ae')
                Belastung = snode.getAttribute("belastung")
                li.setProperty("%s_Name" % (i), Name)
                li.setProperty("%s_Belastung" % (i), Belastung)
                li.setProperty("%s_Pic" % (i), self.pollenpics(Name))
                i+=1
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
        return addon_handle
    

