#!/usr/bin/python

import xbmc
import xbmcaddon
import xbmcgui
import json
import re


import xbmcplugin
import datetime
import urllib2
import sys
import os

class PluginHelpers():
    def __init__(self):
        url=''

##########################################################################################################################
##
##########################################################################################################################
    def getUnicodePage(self,url):
        req = urllib2.urlopen(url)
        content = ""
        if "content-type" in req.headers and "charset=" in req.headers['content-type']:
            encoding=req.headers['content-type'].split('charset=')[-1]
            content = unicode(req.read(), encoding)
        else:
            content = unicode(req.read(), "utf-8")
        return content
    
##########################################################################################################################
##
##########################################################################################################################
    def parameters_string_to_dict(self,parameters):
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict
        
##########################################################################################################################
##
##########################################################################################################################
    def writeLog(self, message, level=xbmc.LOGNOTICE):
        try:
            xbmc.log('[plugin.program.newscenter] %s' % ( message), level)
        except Exception:
            xbmc.log('[plugin.program.newscenter] %s' % ('Fatal: Message could not displayed'), xbmc.LOGERROR)

##########################################################################################################################
##
##########################################################################################################################
    def debug(self, message):
        try:
            xbmc.log('[plugin.program.newscenter] %s' % (message), xbmc.LOGDEBUG)
        except Exception:
            xbmc.log('[plugin.program.newscenter] %s' % ('Fatal: Message could not displayed'), xbmc.LOGERROR)


##########################################################################################################################
##
##########################################################################################################################
    def notifyOSD(self,header, message, icon=xbmcgui.NOTIFICATION_INFO, disp=4000, enabled=True):
        if enabled:
            OSD = xbmcgui.Dialog()
            OSD.notification(header.encode('utf-8'), message.encode('utf-8'), icon, disp)





##################################################################################################################################################################

class NewsBuli():
    def __init__(self):
        url=''



##########################################################################################################################
##
##########################################################################################################################
    def get_buli_naechsterspieltag_items(self,liga):
        listitems = []
        addon      = xbmcaddon.Addon()
        addonID    = addon.getAddonInfo('id')
        mediaPath  = xbmc.translatePath('special://home/addons/'+addonID+'/resources/skins/Default/media/')

        BuliFile = xbmc.translatePath('special://home/addons/'+addonID+'/Buli.json')
        with open(BuliFile, 'r') as Mannschaften:
            BuliMannschaften=Mannschaften.read().rstrip('\n').decode('utf-8')
        MannschaftsID = json.loads(BuliMannschaften)
        ph = PluginHelpers() 
        url="http://bulibox.de/"
        content = ph.getUnicodePage(url)
        content = content.replace("\\","")
        spl = content.split('<div id="inhalt">')
        spl2 = spl[1]
        spl2 = spl2.split('</table>')
    
        if liga != "" and int(liga) == 1:
            bulitable = spl2[0]
        elif int(liga) == int(2):
            bulitable = spl2[1]
    
        bulitable = bulitable.split('<table')
        bulitable = bulitable[1]
        bulitable_rows = bulitable.split('</tr>')
    
        for i in bulitable_rows:
            out = re.compile('<td.+?>(.+?)</td>', re.DOTALL).findall(i)
    
            try:
                spieldatum = out[0].replace('&nbsp;',' ').strip()
                mannschaft1 = out[1].replace('&nbsp;',' ').strip()
                mannschaft2 = out[2].replace('&nbsp;',' ').strip()
    
                for smid in MannschaftsID:
                    if mannschaft1 == smid['name']:
                        mannschaft1pic = "%sBuliLogos/%s.png" % ( mediaPath,smid['id'] )
                    if mannschaft2 == smid['name']:
                        mannschaft2pic = "%sBuliLogos/%s.png" % ( mediaPath,smid['id'] )
                json_str = { "Label": spieldatum.replace('&nbsp;',' ').strip(), "Logo1": mannschaft1pic.strip(), "Mannschaft1": mannschaft1.replace('&nbsp;',' ').strip(), "Logo2": mannschaft2pic.strip(), "Mannschaft2": mannschaft2.replace('&nbsp;',' ').strip() }
                listitems.append( json_str )
    
            except:
                pass
    
        return listitems
    
    


##########################################################################################################################
##
##########################################################################################################################
    def get_buli_table_items(self,liga):
        listitems = []
        print("Hallo Test")
        addon      = xbmcaddon.Addon()
        addonID    = addon.getAddonInfo('id')
        mediaPath  = xbmc.translatePath('special://home/addons/'+addonID+'/resources/skins/Default/media/')
        ph = PluginHelpers()
        url="http://bulibox.de/abschlusstabellen/%s-Bundesliga.html" % (liga)
        content = ph.getUnicodePage(url)
        content = content.replace("\\","")
        BuliFile = xbmc.translatePath('special://home/addons/'+addonID+'/Buli.json')
        with open(BuliFile, 'r') as Mannschaften:
            BuliMannschaften=Mannschaften.read().rstrip('\n').decode('utf-8')
        MannschaftsID = json.loads(BuliMannschaften)
        m=0
        spl = content.split('<div id="inhalt">')
        spl2 = spl[1]
        spl2 = spl2.split('</table>')
        spl2 = spl2[1]
        spl2 = spl2.split('</tr>')
        for i in spl2:
            out = re.compile('<td>(.+?)</td>', re.DOTALL).findall(i)
            rang = ''
            name= ''
            sun = ''
            tore = ''
            punkte = ''
            spiele = ''
            pic = ''
            statpic = ''
            try:
                rang = out[0]
                name = out[1]
                spiele = out[2]
                sun = out[3]
                tore = out[4]
                punkte = out[5]
                statpic = "http://bulibox.de/%s" % (re.compile("src='../(.+?)'", re.DOTALL).findall(out[6])[0])
                for smid in MannschaftsID:
                    if name.replace('&nbsp;',' ').strip() == smid['name']:
                        m+=1
    
                        #pic = "http://sportbilder.t-online.de/fussball/logos/teams/145x145/%s.png" % ( smid['id'] )
                        pic = "%sBuliLogos/%s.png" % ( mediaPath,smid['id'] )
                        json_str = { "Logo": pic.strip(), "Label": name.replace('&nbsp;',' ').strip(), "Spiele": spiele.replace('&nbsp;',' ').strip(), "SUN": sun.replace('&nbsp;',' ').strip(), "Platz": rang.replace('&nbsp;',' ').strip(), "Tore": tore.replace('&nbsp;',' ').strip(), "Punkte": punkte.replace('&nbsp;',' ').strip(), "StatPic": statpic.strip()}
                        listitems.append( json_str )
            except:
                pass
    
        return listitems
    



##########################################################################################################################
##
##########################################################################################################################
    def get_buli_spielplan_items(self,liga):
        listitems = []
        addon      = xbmcaddon.Addon()
        addonID    = addon.getAddonInfo('id')
        addonFolder         = downloadScript = xbmc.translatePath('special://home/addons/'+addonID).decode('utf-8')

        mediaPath  = xbmc.translatePath('special://home/addons/'+addonID+'/resources/skins/Default/media/')
        icon                = os.path.join(addonFolder, "icon.png")#.encode('utf-8')
        ph = PluginHelpers()
        url="http://bulibox.de/abschlusstabellen/%s-Bundesliga.html" % (liga)
        content = ph.getUnicodePage(url)
        content = content.replace("\\","")
        BuliFile = xbmc.translatePath('special://home/addons/'+addonID+'/Buli.json')
        with open(BuliFile, 'r') as Mannschaften:
            BuliMannschaften=Mannschaften.read().rstrip('\n').decode('utf-8')
        MannschaftsID = json.loads(BuliMannschaften)
        print("In Class of Buli: ")
        m=0
        spl = content.split('<div id="inhalt">')
        spl2 = spl[1]
        spl2 = spl2.split('</table>')
        spl2 = spl2[0]
        spl2 = spl2.split("<table border=1 align=center style='width:400; text-align: left' cellpadding='4px'>")
        spl2 = spl2[1]
        spl2 = spl2.split('</tr>')
    
        for i in spl2:
            out = re.compile('<td>(.+?)</td>', re.DOTALL).findall(i)
            spieldatum = ''
            mannschaft1 = ''
            mannschaft2 = ''
            ergebniss = ''
            mannschaft1logo =''
            mannschaft2logo =''
            try:
                spieldatum = out[0]
                mannschaft1 = out[1]
                mannschaft2 = out[2]
                ergebniss = out[3]
                for smid in MannschaftsID:
                    if mannschaft1.replace('&nbsp;',' ').strip() == smid['name']:
                        mannschaft1logo = "%sBuliLogos/%s.png" % ( mediaPath,smid['id'] )
                    if mannschaft2.replace('&nbsp;',' ').strip() == smid['name']:
                        mannschaft2logo = "%sBuliLogos/%s.png" % ( mediaPath,smid['id'] )
    
                spieldatum = spieldatum.replace('&nbsp;',' ').strip()
                mannschaft1 = mannschaft1.replace('&nbsp;',' ').strip()
                mannschaft2 = mannschaft2.replace('&nbsp;',' ').strip()
                ergebniss = ergebniss.replace('&nbsp;',' ').strip()
                json_str = { "Logo": icon, "Label": "Buli Spielplan", "Spieldatum": spieldatum, "Mannschaft1": mannschaft1, "Mannschaft2": mannschaft2, "Ergebniss": ergebniss, "Mannschaft1Logo": mannschaft1logo, "Mannschaft2Logo": mannschaft2logo}
                listitems.append( json_str )
            except:
                pass
    
        return listitems
    


  
