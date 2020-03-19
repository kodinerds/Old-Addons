#!/usr/bin/python
# -*- coding: utf-8 -*-

###########################################################################
#
#          FILE:  plugin.program.serienplaner/default.py
#
#        AUTHOR:  sveni_lee
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.0.1
#       CREATED:  17.3.2016
#
###########################################################################

import urllib
import urllib2
import os
import re
import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import time
import datetime
import json
import sqlite3
from datetime import timedelta
import _strptime
from xml.dom import minidom
from socket import *
from bs4 import BeautifulSoup

from resources.lib.serienplaner import WLScraper


## Kategorie = ''
__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__path__ = __addon__.getAddonInfo('path')
__LS__ = __addon__.getLocalizedString
__icon__ = xbmc.translatePath(os.path.join(__path__, 'icon.png'))

__showOutdated__ = True if __addon__.getSetting('showOutdated').upper() == 'TRUE' else False
__pvr_is_activ__ = True if __addon__.getSetting('pvractive').upper() == 'TRUE' else False 
__maxHLCat__ = int(re.match('\d+', __addon__.getSetting('max_hl_cat')).group())
__advancedDay__ = int(re.match('\d+', __addon__.getSetting('advanced')).group())
__prefer_hd__ = True if __addon__.getSetting('prefer_hd').upper() == 'TRUE' else False
__firstaired__ = True if __addon__.getSetting('first_aired').upper() == 'TRUE' else False
__series_in_db__ = True if __addon__.getSetting('serie_not_in_db').upper() == 'TRUE' else False
__episode_not_in_db__ = True if __addon__.getSetting('episode_not_in_db').upper() == 'TRUE' else False
__datapath__  = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/').decode('utf-8'), __addonID__)
SerienPlaner = __datapath__+'/serienplaner.db'

WINDOW = xbmcgui.Window(10000)
OSD = xbmcgui.Dialog()
WLURL = 'http://www.wunschliste.de/serienplaner/'


# Helpers

def notifyOSD(header, message, icon=xbmcgui.NOTIFICATION_INFO, disp=4000, enabled=True):
    if enabled:
        OSD.notification(header.encode('utf-8'), message.encode('utf-8'), icon, disp)

def writeLog(message, level=xbmc.LOGNOTICE):
        try:
            xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  message.encode('utf-8')), level)
        except Exception:
            xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  'Fatal: Message could not displayed'), xbmc.LOGERROR)

# End Helpers

ChannelTranslateFile = xbmc.translatePath(os.path.join(__path__, 'ChannelTranslate.json')) 
with open(ChannelTranslateFile, 'r') as transfile:
    ChannelTranslate=transfile.read().rstrip('\n')

TVShowTranslateFile = xbmc.translatePath(os.path.join(__path__, 'TVShowTranslate.json'))
with open(TVShowTranslateFile, 'r') as transfile:
    TVShowTranslate=transfile.read().rstrip('\n')

SPWatchtypes = {'international': 1, 'german': 5, 'classics': 3, 'soaps': 2}
SPTranslations = {'international': __LS__(30120), 'german': __LS__(30121), 'classics': __LS__(30122), 'soaps': __LS__(30123)}
SPTranslations1 = {__LS__(30120): 'international', __LS__(30121): 'german', __LS__(30122): 'classics', __LS__(30123): 'soaps'}
properties = ['TVShow', 'Staffel', 'Episode', 'Title', 'Starttime', '_Starttime', 'Datum', 'neueEpisode', 'Channel', 'Logo', 'PVRID', 'Description', 'Rating', 'Altersfreigabe', 'Genre', 'Studio', 'Status', 'Jahr', 'Thumb', 'FirstAired', 'RunningTime', 'Poster', 'Fanart', 'Clearlogo', 'WatchType']

# create category list from selection in settings

def categories():
    cats = []
    for category in SPWatchtypes:
        if __addon__.getSetting(category).upper() == 'TRUE': cats.append(category)
    return cats

# get remote URL, replace '\' and optional split into css containers

def getUnicodePage(url, container=None):
    try:
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = urllib2.Request(url, None, headers)
    except UnicodeDecodeError:
        req = urllib2.urlopen(url)

    encoding = 'utf-8'
    if "content-type" in req.headers and "charset=" in req.headers['content-type']:
        encoding=req.headers['content-type'].split('charset=')[-1]
    try:
        content = unicode(urllib2.urlopen(req).read(), encoding).replace("\\", "")
        if container is None: return content
        return content.split(container)
    except timeout:
        content = unicode(urllib2.urlopen(req).read(), encoding).replace("\\", "")
        if container is None: return content
        return content.split(container)


def getUnicodePage2(url):
    req = urllib2.Request(url)
    content = unicode(urllib2.urlopen(req).read(), "utf-8")
    content = content.replace("\\","")
    return content

def getUnicodePage3(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    content = unicode(urllib2.urlopen(req).read(), "utf-8")
    content = content.replace("\\","")
    return content

# get parameter hash, convert into parameter/value pairs, return dictionary

def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

# get used dateformat of kodi

def getDateFormat():
    df = xbmc.getRegion('dateshort')
    tf = xbmc.getRegion('time').split(':')

    try:
        # time format is 12h with am/pm
        return df + ' ' + tf[0][0:2] + ':' + tf[1] + ' ' + tf[2].split()[1]
    except IndexError:
        # time format is 24h with or w/o leading zero
        return df + ' ' + tf[0][0:2] + ':' + tf[1]

# convert datetime string to timestamp with workaround python bug (http://bugs.python.org/issue7980) - Thanks to BJ1

def date2timeStamp(date, format):
    try:
        dtime = datetime.datetime.strptime(date, format)
    except TypeError:
        try:
            dtime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, format)))
        except ValueError:
            return False
    except Exception:
        return False
    return int(time.mktime(dtime.timetuple()))

##########################################################################################################################
## get pvr channel-id
##########################################################################################################################
def channelName2channelId(channelname):
    query = {
            "jsonrpc": "2.0",
            "method": "PVR.GetChannels",
            "params": {"channelgroupid": "alltv"},
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))

    # translate via json if necessary
    trans = json.loads(str(ChannelTranslate))
    for tr in trans:
        if channelname == tr['name']:
            writeLog("Translating %s to %s" % (channelname,tr['pvrname']), level=xbmc.LOGDEBUG)
            channelname = tr['pvrname']
    
    if 'result' in res and 'channels' in res['result']:
        res = res['result'].get('channels')
        for channels in res:

            # prefer HD Channel if available
            if __prefer_hd__ and  (channelname + " HD").lower() in channels['label'].lower():
                writeLog("SerienPlaner found HD priorized channel %s" % (channels['label']), level=xbmc.LOGDEBUG)
                return channels['channelid']

            if channelname.lower() in channels['label'].lower():
                writeLog("TVHighlights found channel %s" % (channels['label']), level=xbmc.LOGDEBUG)
                return channels['channelid']
    return False

##########################################################################################################################
## get TVShow-DBID 
##########################################################################################################################
def TVShowName2TVShowDBID(tvshowname):

    trans = json.loads(str(TVShowTranslate))
    for tr in trans:
        if tvshowname == tr['name']:
            writeLog("Translating %s to %s" % (tvshowname,tr['tvshow']), level=xbmc.LOGDEBUG)
            tvshowname = tr['tvshow']

    query = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetTVShows",
            "params": {
                "properties": ["originaltitle", "imdbnumber"]
            },
            "id": "libTvShows"
            }
    
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    
    try:
        if 'result' in res and 'tvshows' in res['result']:
            res = res['result']['tvshows']
            for tvshow in res:
                if tvshow['label'] == tvshowname:
                    return tvshow['tvshowid']

        return False
    except Exception:
        writeLog("JSON query returns an error", level=xbmc.LOGDEBUG)
        return False

##########################################################################################################################
## get TVShow-ID 
##########################################################################################################################
def TVShowName2TVShowID(tvshowname):

    trans = json.loads(str(TVShowTranslate))
    for tr in trans:
        if tvshowname == tr['name']:
            writeLog("Translating %s to %s" % (tvshowname,tr['tvshow']), level=xbmc.LOGDEBUG)
            tvshowname = tr['tvshow']

    query = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetTVShows",
            "params": {
                "properties": ["originaltitle", "imdbnumber"]
            },
            "id": "libTvShows"
            }
    
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
#    writeLog("JSON returns: %s" % (res), level=xbmc.LOGDEBUG)
    try:
        if 'result' in res and 'tvshows' in res['result']:
            res = res['result']['tvshows']
            for tvshow in res:
                if tvshow['label'] == tvshowname:
##                    return tvshow['imdbnumber']
                    return True
        return False
    except Exception:
        writeLog("JSON query returns an error", level=xbmc.LOGDEBUG)
        return False




##########################################################################################################################
## get Season and Episode TVShow-ID 
##########################################################################################################################
def SeasonAndEpisodeInDB(tvshowid, season, episode):
    query = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetEpisodes",
            "params": {
                "tvshowid": tvshowid,
                "properties": ["season", "episode"]
            },
            "id": "libEpisodes"
            }
    
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
#    writeLog("JSON returns: %s" % (res), level=xbmc.LOGDEBUG)
    try:
        if 'result' in res and 'episodes' in res['result']:
            res = res['result']['episodes']
            for episo in res:
#                writeLog("JSON returns: Season %s Episode %s" % (episo['season'], episo['episode']), level=xbmc.LOGDEBUG)
#                writeLog("Season: %s  Episode: %s" % (season, episode), level=xbmc.LOGDEBUG)
                if episo['season'] == int(season) and episo['episode'] == int(episode):
                    writeLog("Ergebnis: TRUE", level=xbmc.LOGDEBUG)                
                    return True
        return False
    except Exception:
        writeLog("JSON query returns an error", level=xbmc.LOGDEBUG)
        return False



##########################################################################################################################
## get TVShow-ID 
##########################################################################################################################

def get_thetvdbID(tvshowname):

            # translate via json if necessary
    trans = json.loads(str(TVShowTranslate))
    for tr in trans:
        if tvshowname == tr['name']:
            writeLog("Translating %s to %s" % (tvshowname,tr['tvshow']), level=xbmc.LOGDEBUG)
            tvshowname = tr['tvshow']

    tvshowname = tvshowname.replace('&', '')
    tvshowname = tvshowname.replace('and', '')    

    tvshowname = tvshowname.encode("utf-8")
    url_str="http://thetvdb.com/api/GetSeries.php?seriesname="+tvshowname
    try:
        xml_str = urllib.urlopen(url_str).read()
        xmldoc = minidom.parseString(xml_str)
    except timeout:
        time.sleep(5)
        xml_str = urllib.urlopen(url_str).read()
        xmldoc = minidom.parseString(xml_str)

    series_detail = xmldoc.getElementsByTagName("Series")

    try:        
        for Series in series_detail:
            imdbid = Series.getElementsByTagName("id")[0].firstChild.nodeValue
            writeLog("Serie hat ID %s auf the TVDB" % (imdbid), level=xbmc.LOGDEBUG) 
            return imdbid
    except Exception:
        writeLog("Serie nicht auf the TVDB", level=xbmc.LOGDEBUG)
        return False

##########################################################################################################################
## get TVShow-Poster DB
##########################################################################################################################
def TVShowName2TVShow_Detais(tvshowname):
    query = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetTVShows",
            "params": {
                "properties": ["originaltitle", "thumbnail", "genre", "studio", "mpaa", "year"]
            },
            "id": "libTvShows"
            }
    
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    try:
        if 'result' in res and 'tvshows' in res['result']:
            res = res['result']['tvshows']
            for tvshow in res:
                if tvshow['label'] == tvshowname:
                    return {'_genre' : tvshow['genre'], '_posterUrl' : tvshow['thumbnail'], '_studio' : tvshow['studio'], '_mpaa' : tvshow['mpaa'], '_year' : tvshow['year']}
    except Exception:
        writeLog("JSON query returns an error", level=xbmc.LOGDEBUG)
        return False      

##########################################################################################################################
## get TVShow-Poster THE TVDB
##########################################################################################################################

def get_thetvdbPoster(imdbnumber):
    url_str="http://tvdb.cytec.us/api/9DAF49C96CBF8DAC/series/%s/de.xml" % (imdbnumber)
    xml_str = urllib.urlopen(url_str).read()
    xmldoc = minidom.parseString(xml_str)

    poster_detail = xmldoc.getElementsByTagName("Series")

    try:        
        for Series in poster_detail:
            poster = Series.getElementsByTagName("poster")[0].firstChild.nodeValue
            genre = Series.getElementsByTagName("Genre")[0].firstChild.nodeValue
            genre = genre[1:-1]
            genre = genre.replace('|',' | ').strip()
            studio = Series.getElementsByTagName("Network")[0].firstChild.nodeValue
            content_rating = Series.getElementsByTagName("ContentRating")[0].firstChild.nodeValue
            status = Series.getElementsByTagName("Status")[0].firstChild.nodeValue
            year = Series.getElementsByTagName("FirstAired")[0].firstChild.nodeValue
            year = year[:-6]
            return {'_genre' : genre, '_posterUrl' : poster, '_studio' : studio, 'content_rating' : content_rating, 'status' : status, 'year' : year}
    except Exception:
        writeLog("Poster nicht auf the TVDB", level=xbmc.LOGDEBUG)
        return 0


##########################################################################################################################
## get pvr channelname by id
##########################################################################################################################

def pvrchannelid2channelname(channelid):
    query = {
            "jsonrpc": "2.0",
            "method": "PVR.GetChannels",
            "params": {"channelgroupid": "alltv"},
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    if 'result' in res and 'channels' in res['result']:
        res = res['result'].get('channels')
        for channels in res:
            if channels['channelid'] == channelid:
                writeLog("SerienPlaner found id for channel %s" % (channels['label']), level=xbmc.LOGDEBUG)
                return channels['label']
    return False

##########################################################################################################################
## get pvr channel logo url
##########################################################################################################################

def pvrchannelid2logo(channelid):
    query = {
            "jsonrpc": "2.0",
            "method": "PVR.GetChannelDetails",
            "params": {"channelid": channelid, "properties": ["thumbnail"]},
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    if 'result' in res and 'channeldetails' in res['result'] and 'thumbnail' in res['result']['channeldetails']:
        return res['result']['channeldetails']['thumbnail']
    else:
        return False


##########################################################################################################################
## switch tu channel
##########################################################################################################################

def switchToChannel(pvrid):
    writeLog('Switch to channel id %s' % (pvrid), level=xbmc.LOGDEBUG)
    query = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Player.Open",
        "params": {"item": {"channelid": pvrid}}
        }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    if 'result' in res and res['result'] == 'OK':
        return True
    else:
        writeLog('Couldn\'t switch to channel id %s' % (pvrid), level=xbmc.LOGDEBUG)
    return False

##########################################################################################################################
## clear all info properties (info window) in Home Window
##########################################################################################################################

def clearInfoProperties():
    writeLog('clear all info properties (used in info popup)', level=xbmc.LOGDEBUG)
    for property in infoprops:
        WINDOW.clearProperty('TVHighlightsToday.Info.%s' % (property))
    for i in range(1, 6, 1):
        WINDOW.clearProperty('TVHighlightsToday.RatingType.%s' % (i))
        WINDOW.clearProperty('TVHighlightsToday.Rating.%s' % (i))

##########################################################################################################################
## get start Datum
##########################################################################################################################

def get_startdate():
    try:
        m = open("%s/datestamp.dat" % __datapath__,"r")
        datestamp_ = m.read()
        datestamp_ = datetime.datetime(*(time.strptime(datestamp_, '%d.%m.%Y')[0:6]))
        datestamp = datestamp_.strftime('%d.%m.%Y')
        today_ = time.strftime("%d.%m.%Y")
        today_ = datetime.datetime(*(time.strptime(today_, '%d.%m.%Y')[0:6]))

        i = datestamp_ - today_
        i = i.days
        return i
    except:
        pass
        i = 0
        return i


##########################################################################################################################
## clear content of widgets in Home Window
##########################################################################################################################

def clearWidgets(start_from=1):
    writeLog('Clear widgets from #%s and up' % (start_from), level=xbmc.LOGDEBUG)
    for i in range(start_from, 17, 1):
        for property in properties:
            WINDOW.clearProperty('SerienPlaner.%s.%s' % (i, property))

def refreshWidget(offset=0):

    Kategorie = WINDOW.getProperty('Kategorie')

    writeLog('refreshWidget Kategorie:  %s' % (Kategorie), level=xbmc.LOGDEBUG)
    listitems = []

    conn = sqlite3.connect(SerienPlaner)
    cur = conn.cursor()
    query = """SELECT %s
           FROM TVShowData
           WHERE julianday(_Starttime) + (_RunningTime / 24.0 / 60.0) > julianday('now', 'localtime')
           %s
           ORDER BY _Starttime
           LIMIT %s"""

    filter = ""
    parameters = []

    if not Kategorie or Kategorie == __LS__(30116):
        filter += ""
        parameters += ()
    else:
        filter += " AND WatchType = ?"
        parameters += (Kategorie,)
    if __series_in_db__:
        filter += " AND Serie_in_DB = ?"
        parameters += (True,)
    if __episode_not_in_db__:
        filter += " AND EpisodeInDB = ?"
        parameters += (False,)        
    if __firstaired__:
        filter += " AND neueEpisode LIKE ?"
        parameters += ('%'+'NEU'+'%',)

    query = query % (','.join(properties), filter, __maxHLCat__)
    cur.execute(query, parameters)
    try:
        for idx, data in enumerate(cur, offset):
            for field, item in zip(properties, data):     
            
                WINDOW.setProperty('SerienPlaner.%d.%s' % (idx, field), item)
                
            listitems.append(dict(zip(properties, data)))    

        return listitems
    finally:
    
        cur.execute("""DELETE FROM TVShowData WHERE julianday(_Starttime) + (_RunningTime / 24.0 / 60.0) < julianday('now', 'localtime')""")
        conn.commit()
        conn.close()

def get_Guide_Items(k, gdate, offset=0):
    
    i=200+(k)
    listitems = []

    conn = sqlite3.connect(SerienPlaner)
    cur = conn.cursor()
    query = """SELECT %s
           FROM TVShowData
           WHERE julianday(_Starttime) + (_RunningTime / 24.0 / 60.0) > julianday('now', 'localtime')
           %s
           ORDER BY _Starttime"""

    filter = ""
    parameters = []

 #   if not Kategorie or Kategorie == __LS__(30116):
 #       filter += ""
 #       parameters += ()
 #   else:
 #       filter += " AND WatchType = ?"
 #       parameters += (Kategorie,)
    filter += " AND Datum = ?"
    parameters += (gdate,)
    if __series_in_db__:
        filter += " AND Serie_in_DB = ?"
        parameters += (True,)
    if __episode_not_in_db__:
        filter += " AND EpisodeInDB = ?"
        parameters += (False,)
    if __firstaired__:
        filter += " AND neueEpisode LIKE ?"
        parameters += ('%'+'NEU'+'%',)

    query = query % (','.join(properties), filter)
    cur.execute(query, parameters)
    try:
        for idx, data in enumerate(cur, offset):
            for field, item in zip(properties, data):     
            
                WINDOW.setProperty('SerienPlaner.%s.TVGUIDE.%d.%s' % (i, idx, field), item)
                
            listitems.append(dict(zip(properties, data)))    

        return listitems
    finally:
    
#        cur.execute()
        conn.commit()
        conn.close()

def scrapeWLPage(category, day):
    url = url = '%s%s/%s' % (WLURL, SPWatchtypes[category], day)
    writeLog('Start scraping category %s from %s' % (category, url), level=xbmc.LOGDEBUG)

    i = 1
    page = getUnicodePage3(url)
    soup = BeautifulSoup(page, "html.parser",from_encoding="acii")

    blobs = WINDOW.getProperty('SP.%s.blobs' % (category))
    if blobs != '':

        for idx in range(1, int(blobs) + 1, 1):
            WINDOW.clearProperty('SP.%s.%s' % (category, idx))

#    for container in content:
    for container in soup.findAll('li', {'id': re.compile(r'e_[^\s]*')}):
        data = WLScraper()
        data.scrapeserien(container)

        pvrchannelID = channelName2channelId(data.channel)
        if __pvr_is_activ__ and not pvrchannelID:
            writeLog("SerienPlaner: Channel %s is not in PVR, discard entry" % (data.channel), level=xbmc.LOGDEBUG)
            continue   
        logoURL = pvrchannelid2logo(pvrchannelID)
        channel = pvrchannelid2channelname(pvrchannelID)
        serieinDB = TVShowName2TVShowID(data.tvshowname)
        tvshowdbid = TVShowName2TVShowDBID(data.tvshowname)
        episodeinDB = SeasonAndEpisodeInDB(tvshowdbid, data.staffel, data.episode)

        detailURL = 'http://www.wunschliste.de%s' % (data.detailURL)
        seriesUrl = 'http://www.wunschliste.de%s' % (data.nameURL)
        imdbnumber = get_thetvdbID(data.tvshowname)
#        if not imdbnumber:
#            org_ser_name = WLScraper ()
#            org_ser_name.get_original_series_name(getUnicodePage(seriesUrl), data.tvshowname)
#            imdbnumber = get_thetvdbID(org_ser_name.orig_tvshow)
#            writeLog("SerienPlaner: TVShow has original name: %s" % (imdbnumber), level=xbmc.LOGDEBUG) 
#        else:
#            pass
        if not imdbnumber:
##            details = WLScraper()
##            details.scrapeDetailPage(getUnicodePage(detailURL), 'div class="text"')
            tvshow = data.tvshowname
            tvshow = tvshow.encode('utf-8')
            tvshow = tvshow.replace('&', 'und')
            tvshow = tvshow.replace('- ', '').strip()
            tvshow = tvshow.replace("ß", "ss").strip()
            tvshow = tvshow.replace("ö", "oe")
            tvshow = tvshow.replace("ü", "ue")
            tvshow = tvshow.replace("ä", "ae")
            tvshow = tvshow.replace(',', '').strip()
            tvshow = tvshow.replace('.', '').strip()
            tvshow = tvshow.replace(' ', '-').strip()
            tvshow = tvshow.replace('/', '-').strip()
            tvshow = tvshow.replace("'", '').strip()
            tvshow = str(tvshow.lower())
            title = data.title
            title = title.encode('utf-8')
            title = title.replace("ß", "ss").strip()
            title = title.replace(',', '').strip()
            title = title.replace('- ', '').strip()
            title = title.replace("ö", "oe")
            title = title.replace("ü", "ue")
            title = title.replace("ä", "ae")
            title = title.replace(' ', '-').strip()        
            title = str(title.lower())
            url = "http://www.fernsehserien.de/%s/episodenguide" % (tvshow)
            detail_url = WLScraper()
            try:
                detail_url.get_scrapper_fernsehserien_path(getUnicodePage(url), tvshow, title)
                writeLog("Fernsehserienpath: %s" % (detail_url.detailpath), level=xbmc.LOGDEBUG)
            except:
                pass
            if not detail_url.detailpath:
                continue
            else:
                details = WLScraper()
                details.get_details_fernseserien(getUnicodePage(detail_url.detailpath), tvshow, title)
                clearlogo = WLScraper()
                clearlogo.get_fanarttv_clearlogo(imdbnumber, 'clearlogo')               
        else:
            details = WLScraper ()
            details.get_detail_thetvdb(imdbnumber, data.staffel, data.episode)
            clearlogo = WLScraper()
            clearlogo.get_fanarttv_clearlogo(imdbnumber, 'clearlogo')

##        if not details.epiid:
##            try:
##                pic_path = WLScraper ()
##                pic_path.get_scrapedetail_pcpath(getUnicodePage(detailURL), 'div class="text"')
##                thumbpath = pic_path.pic_path
##            except AttributeError:
##                pass
##        else:
        if not details.pic_path:
##            details = WLScraper()
##            details.scrapeDetailPage(getUnicodePage(detailURL), 'div class="text"')
            tvshow = data.tvshowname
            tvshow = tvshow.encode('utf-8')
            tvshow = tvshow.replace('&', 'und')
            tvshow = tvshow.replace('- ', '').strip()
            tvshow = tvshow.replace("ß", "ss").strip()
            tvshow = tvshow.replace("ö", "oe")
            tvshow = tvshow.replace("ü", "ue")
            tvshow = tvshow.replace("ä", "ae")
            tvshow = tvshow.replace(',', '').strip()
            tvshow = tvshow.replace('.', '').strip()
            tvshow = tvshow.replace(' ', '-').strip()
            tvshow = tvshow.replace('/', '-').strip()
            tvshow = tvshow.replace("'", '').strip()
            tvshow = str(tvshow.lower())
            title = data.title
            title = title.encode('utf-8')
            title = title.replace("ß", "ss").strip()
            title = title.replace(',', '').strip()
            title = title.replace('- ', '').strip()
            title = title.replace("ö", "oe")
            title = title.replace("ü", "ue")
            title = title.replace("ä", "ae")
            title = title.replace(' ', '-').strip()        
            title = str(title.lower())
            url = "http://www.fernsehserien.de/%s/episodenguide" % (tvshow)
            try:
                detail_url = WLScraper()
                detail_url.get_scrapper_fernsehserien_path(getUnicodePage(url), tvshow, title)
                writeLog("Fernsehserienpath: %s" % (detail_url.detailpath), level=xbmc.LOGDEBUG)
            except:
                pass
            if not detail_url.detailpath:
                pass
            else:
                details = WLScraper()
                details.get_details_fernseserien(getUnicodePage(detail_url.detailpath), tvshow, title)
        else:
            pass
        thumbpath = details.pic_path


        writeLog('', level=xbmc.LOGDEBUG)
        writeLog('ID:              SP.%s.%s' %(category, i), level=xbmc.LOGDEBUG)
        writeLog('TVShow:           %s' % (data.tvshowname), level=xbmc.LOGDEBUG)
        writeLog('Staffel:         %s' % (data.staffel), level=xbmc.LOGDEBUG)
        writeLog('Episode:         %s' % (data.episode), level=xbmc.LOGDEBUG)
        writeLog('Title:           %s' % (data.title), level=xbmc.LOGDEBUG)
        writeLog('Starttime:       %s' % (data.tvshowstarttime), level=xbmc.LOGDEBUG)
        writeLog('Datum:           %s' % (data.date), level=xbmc.LOGDEBUG)
        writeLog('neueEpisode:     %s' % (data.neueepisode), level=xbmc.LOGDEBUG)
        writeLog('Channel (SP):    %s' % (data.channel), level=xbmc.LOGDEBUG)
        writeLog('Channel (PVR):   %s' % (channel), level=xbmc.LOGDEBUG)
        writeLog('Channel logo:    %s' % (logoURL), level=xbmc.LOGDEBUG)
        writeLog('ChannelID (PVR): %s' % (pvrchannelID), level=xbmc.LOGDEBUG)
        writeLog('Description:     %s' % (details.plot), level=xbmc.LOGDEBUG)
        writeLog('Rating:          %s' % (details.rating), level=xbmc.LOGDEBUG)
        writeLog('Altersfreigabe:  %s' % (details.content_rating), level=xbmc.LOGDEBUG)
        writeLog('Genre:           %s' % (details.genre), level=xbmc.LOGDEBUG)
        writeLog('Studio:          %s' % (details.studio), level=xbmc.LOGDEBUG)
        writeLog('Status:          %s' % (details.status), level=xbmc.LOGDEBUG)
        writeLog('Jahr:            %s' % (details.year), level=xbmc.LOGDEBUG)
        writeLog('Thumb:           %s' % (thumbpath), level=xbmc.LOGDEBUG)
        writeLog('FirstAired:      %s' % (details.firstaired), level=xbmc.LOGDEBUG)
        writeLog('RunningTime:     %s' % (data.runtime), level=xbmc.LOGDEBUG)
        writeLog('Popup:           %s' % (detailURL), level=xbmc.LOGDEBUG)
        writeLog('poster:          %s' % (details.posterUrl), level=xbmc.LOGDEBUG)
        writeLog('fanart:          %s' % (details.fanartUrl), level=xbmc.LOGDEBUG)
        writeLog('Serie in DB:     %s' % (serieinDB), level=xbmc.LOGDEBUG)
        writeLog('TVShowDBID:      %s' % (tvshowdbid), level=xbmc.LOGDEBUG)
        writeLog('Episode in DB:   %s' % (episodeinDB), level=xbmc.LOGDEBUG)
        writeLog('Watchtype:       %s' % (category), level=xbmc.LOGDEBUG)
        writeLog('Clearlogo:       %s' % (clearlogo.clearlogo), level=xbmc.LOGDEBUG)
        writeLog('', level=xbmc.LOGDEBUG)

        blob = {
                'id': unicode('SP.%s.%s' % (i, category)),
                'tvshow': unicode(data.tvshowname),
                'staffel': unicode(data.staffel),
                'episode': unicode(data.episode),
                'title': unicode(data.title),
                'starttime': unicode(data.tvshowstarttime),
                '_starttime': data.starttimestamp,
                'date' : unicode(data.date),
                '_date': data.date,
                'neueepisode': unicode(data.neueepisode),
                'channel': unicode(data.channel),                
                'pvrchannel': unicode(channel),
                'logo': unicode(logoURL),
                'pvrid': unicode(pvrchannelID),
                'description': unicode(details.plot),
                'rating': unicode(details.rating),
                'content_rating': unicode(details.content_rating),
                'genre': unicode(details.genre),
                'studio': unicode(details.studio),
                'status': unicode(details.status),
                'year': unicode(details.year),
                'thumb': unicode(thumbpath),
                'firstaired': unicode(details.firstaired),
                'runtime': unicode(data.runtime),
                '_runtime': data.runtime,
                'poster': unicode(details.posterUrl),
                'fanart': unicode(details.fanartUrl),
                'clearlogo': unicode(clearlogo.clearlogo),
                'Serie_in_DB': serieinDB,
                'EpisodeInDB': episodeinDB,
                'category': unicode(category),
               }


        conn = sqlite3.connect(SerienPlaner)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS TVShowData(
            WatchType,
            Datum,
            _Datum,
            Starttime,
            _Starttime,
            Channel,
            TVShow,
            Staffel,
            Episode,
            Title,
            neueEpisode,
            Description,
            Rating,
            Altersfreigabe,
            Genre,
            Studio,
            Status,
            Jahr,
            FirstAired,
            RunningTime,
            _RunningTime,
            Thumb,
            Poster,
            Fanart,
            Clearlogo,
            PVRID,
            Logo,
            Serie_in_DB,
            EpisodeInDB,
            UNIQUE(Datum, Starttime, Channel)
            ON CONFLICT REPLACE);""")

        sql_command = """INSERT INTO TVShowData(
            WatchType,
            Datum,
            _Datum,
            Starttime,
            _Starttime,
            Channel,
            TVShow,
            Staffel,
            Episode,
            Title,
            neueEpisode,
            Description,
            Rating,
            Altersfreigabe,
            Genre,
            Studio,
            Status,
            Jahr,
            FirstAired,
            RunningTime,
            _RunningTime,
            Thumb,
            Poster,
            Fanart,
            Clearlogo,
            PVRID,
            Logo,
            Serie_in_DB,
            EpisodeInDB) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""";
        cur.execute(sql_command, (SPTranslations[blob['category']], blob['date'], blob['_date'], blob['starttime'], blob['_starttime'], blob['pvrchannel'], blob['tvshow'], blob['staffel'], blob['episode'], blob['title'], blob['neueepisode'], blob['description'], blob['rating'], blob['content_rating'], blob['genre'], blob['studio'], blob['status'], blob['year'], blob['firstaired'], blob['runtime'], blob['_runtime'], blob['thumb'], blob['poster'], blob['fanart'],blob['clearlogo'], blob['pvrid'], blob['logo'], blob['Serie_in_DB'], blob['EpisodeInDB']))
        conn.commit()
        conn.close()
        i += 1
        
        m = open("%s/datestamp.dat" % __datapath__,"w")
        m.write(str(data.date))
        m.close()



# M A I N
#________

# Get starting methode

methode = None
detailurl = None
pvrid = None

if len(sys.argv)==3:
    addon_handle = int(sys.argv[1])
    params = parameters_string_to_dict(sys.argv[2])
    methode = urllib.unquote_plus(params.get('methode', ''))
    guidedate = urllib.unquote_plus(params.get('guidedate', ''))
    url = urllib.unquote_plus(params.get('url', ''))

elif len(sys.argv)>1:
    params = parameters_string_to_dict(sys.argv[1])
    methode = urllib.unquote_plus(params.get('methode', ''))
    detailurl = urllib.unquote_plus(params.get('detailurl', ''))
    pvrid = urllib.unquote_plus(params.get('pvrid', ''))
    url = urllib.unquote_plus(params.get('url', ''))

writeLog("Methode from external script: %s" % (methode), level=xbmc.LOGDEBUG)
writeLog("Detailurl from external script: %s" % (detailurl), level=xbmc.LOGDEBUG)
writeLog("pvrid from external script: %s" % (pvrid), level=xbmc.LOGDEBUG)

if methode == 'scrape_serien':
    f = open("%s/background.dat" % __datapath__,"w")
    f.write(str(time.time()))
    f.close()    

    for category in categories():
        b = get_startdate()
        for i in range(b, __advancedDay__):
            scrapeWLPage(category, i)
    refreshWidget()

elif methode == 'refresh_screen':
    WINDOW.setProperty('SerienPlaner.Countdown', unicode(time.time()))
    writeLog('localtime %s' % (time.time()), level=xbmc.LOGDEBUG)
    refreshWidget()

elif methode == 'get_item_serienplaner':
    sp_items = refreshWidget()
    writeLog('spitems %s' % (sp_items), level=xbmc.LOGDEBUG)
    writeLog('SerienPlaner sysargv: '+str(sys.argv), level=xbmc.LOGDEBUG)
    url = '-'
    for sitem in sp_items:
        li = xbmcgui.ListItem(label2=sitem['TVShow'], label=sitem['Title'], thumbnailImage=sitem['Thumb'])

        if sitem['_Starttime'] <= datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'):
            li.setProperty("Playstatus", "IsRunning")
        else:
            li.setProperty("Playstatus", "IsInFuture")

        li.setProperty("channel", sitem['Channel'])
        li.setArt({'poster': sitem['Poster'], 'fanart': sitem['Fanart'], 'clearlogo' : sitem['Clearlogo']})
        li.setInfo('video', {'mediatype' : "episode", 'Season' : sitem['Staffel'], 'Episode' : sitem['Episode'], 'Title' : sitem['Title'], 'Genre' : sitem['Genre'], 'mpaa' : sitem['Altersfreigabe'], 'year' : sitem['Jahr'], 'plot' : sitem['Description'], 'rating' : sitem['Rating'], 'studio' : sitem['Studio'], 'tvshowtitle' : sitem['TVShow']})
        li.setProperty("senderlogo", sitem['Logo'])
        li.setProperty("starttime", sitem['Starttime'])
        li.setProperty("date", sitem['Datum'])
        li.setProperty("RunTime", sitem['RunningTime'])
        li.setProperty("PVRID", sitem['PVRID'])
        li.setProperty("status", sitem['Status'])
        li.setProperty('datetime', '%s %s' % (sitem['Datum'], sitem['Starttime']))
        li.setProperty('recordtime', sitem['_Starttime'])
        li.setProperty("recordname", '%s.S%sE%s.%s' % (sitem['TVShow'], sitem['Staffel'], sitem['Episode'], sitem['Title']))
        li.setProperty("DBType", '%s' % ("serienplaner"))
##        li.setEpisode("episode", sitem['Episode'])
##        li.setTitle("Title", sitem['Title'])
##        li.setProperty("rating", sitem['Rating'])
##        li.setProperty("genre", sitem['Genre'])
##        li.setProperty("studio", sitem['Studio'])
##        li.setProperty("year", sitem['Jahr'])
##        li.setProperty("altersfreigabe", sitem['Altersfreigabe'])
##        li.setProperty("label", sitem['Title'])
##        li.setProperty("label2", sitem['TVShow'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
    xbmc.executebuiltin("Container.Refresh")

elif methode == 'TV_SP_Guide':
   
    Popup = xbmcgui.WindowXMLDialog('script-serienplaner-TVGuide.xml', __path__, 'Default', '1080p')
    Popup.doModal() 

elif methode == 'get_Date':
    gdate = datetime.datetime.strftime(datetime.date.today(), '%d.%m.%Y')
    i=0
 
    for i in range(15):
        _gdate = datetime.date.today() + datetime.timedelta(days=i)

        gdate = _gdate.strftime('%d.%m.%Y')
        wday = _gdate.strftime("%a")

        WINDOW.setProperty('TV-Guide.%s.Date' % (i+1), unicode(gdate))
        WINDOW.setProperty('TV-Guide.%s.Wday' % (i+1), unicode(wday))       
        writeLog('spitems %s - %s' % (wday, WINDOW.getProperty('TV-Guide.%s.Date' % (i+1))), level=xbmc.LOGDEBUG)
        spg_items = get_Guide_Items(i, gdate)

        i=i+1     


elif methode == 'switch_channel':
    switchToChannel(int(pvrid))

elif methode=='show_select_dialog':
    writeLog('Methode: show select dialog', level=xbmc.LOGDEBUG)
    dialog = xbmcgui.Dialog()
    cats = [__LS__(30120), __LS__(30121), __LS__(30122), __LS__(30123), __LS__(30116)]
    ret = dialog.select(__LS__(30011), cats)

    if ret == 6:
        refreshWidget()
    elif 0 <= ret <= 5:
        writeLog('%s selected' % (cats[ret]), level=xbmc.LOGDEBUG)

        WINDOW.setProperty('Kategorie', unicode(cats[ret]))        
        refreshWidget()
        WINDOW.setProperty('SerienPlaner.Countdown', unicode(time.time()))

    else:
        pass
