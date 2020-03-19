#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import json


def debug(content):
    log(content, xbmc.LOGDEBUG)
    
def notice(content):
    log(content, xbmc.LOGNOTICE)

def log(msg, level=xbmc.LOGNOTICE):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level) 



fileid = xbmc.getInfoLabel('ListItem.DBID')
debug("+++++")
debug(fileid)
result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"VideoLibrary.GetEpisodeDetails","params":{"episodeid":'+fileid+',"properties":["tvshowid"]},"id":20}') 
struktur=json.loads(result)
erg=struktur["result"]["episodedetails"]["tvshowid"]
debug("ERG: "+str(erg))
url="ActivateWindow(Videos,videodb://tvshows/titles/%s/?tvshowid=%s)"%(erg,erg)
debug(url)
debug("+++++++++++++++++++")
xbmc.executebuiltin(url)
