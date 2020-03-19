#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################################################
#
#          FILE:  plugin.program.newscenter/default.py
#
#        AUTHOR:  Tobias D. Oestreicher
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.0.6
#       CREATED:  13.02.2016
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
#     CHANGELOG:  (13.02.2016) TDOe - First Publishing
###########################################################################


import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

from resources.lib.NewsVideos import NewsVideos
from resources.lib.NewsLiveStreams import NewsLiveStreams
from resources.lib.NewsWetterKarten import NewsWetterKarten,NewsCenterGeoHelper
from resources.lib.NewsPollenflug import NewsPollenflug
from resources.lib.NewsUWZ import NewsUWZ
from resources.lib.NewsBuli import NewsBuli,PluginHelpers
from resources.lib.NewsFeed import NewsFeed

# To Remove: LatestDokus Widget
import json
import urllib2


# Dialogwindows

##########################################################################################################################
##
##########################################################################################################################
def show_bulispielplan(liga):
    DETAILWIN = xbmcgui.WindowXMLDialog('bulilist-spielplan-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

##########################################################################################################################
##
##########################################################################################################################
def show_bulinaechsterspieltag(liga):
    DETAILWIN = xbmcgui.WindowXMLDialog('bulilist-naechsterspieltag-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

##########################################################################################################################
##
##########################################################################################################################
def show_bulilist(liga):
    DETAILWIN = xbmcgui.WindowXMLDialog('bulilist-platzierung-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

##########################################################################################################################
##
##########################################################################################################################
def show_unwetterwarnungen():
    DETAILWIN = xbmcgui.WindowXMLDialog('unwetterwarnungen-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()





# To Remove: docu.cc Widget

##########################################################################################################################
##
##########################################################################################################################
def getUnicodePage(url):
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
def set_LatestDokus_to_Home(url):
    WINDOW = xbmcgui.Window( 10000 )
    content = str(getUnicodePage(url))
    NewDokus = json.loads(content)
    NewDokus = NewDokus['dokus']
    x=0
    for Doku in NewDokus:
        WINDOW.setProperty( "LatestDocu.%s.Title" % (x), Doku['title'] )
        WINDOW.setProperty( "LatestDocu.%s.Thumb" % (x), Doku['cover'] )
        WINDOW.setProperty( "LatestDocu.%s.Path" % (x),  'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (Doku['youtubeId']) )
        WINDOW.setProperty( "LatestDocu.%s.Tags" % (x),  Doku['dokuSrc'] )
        x+=1

##########################################################################################################################
##
##########################################################################################################################
def clear_LatestDokus_at_Home():
    WINDOW = xbmcgui.Window( 10000 )
    for i in range(1,25):
        WINDOW.clearProperty('LatestDocu.%s.Title' % i)
        WINDOW.clearProperty('LatestDocu.%s.Thumb' % i)
        WINDOW.clearProperty('LatestDocu.%s.Path' % i)
        WINDOW.clearProperty('LatestDocu.%s.Tags' % i)






##########################################################################################################################
##########################################################################################################################
##
##                                                       M  A  I  N
##
##########################################################################################################################
##########################################################################################################################

__addon__               = xbmcaddon.Addon()
__addonID__             = __addon__.getAddonInfo('id')
__addonDir__            = __addon__.getAddonInfo("path")
__addonFolder__         = xbmc.translatePath('special://home/addons/'+__addonID__).decode('utf-8')
__addonUserDataFolder__ = xbmc.translatePath("special://profile/addon_data/"+__addonID__).decode('utf-8')
__addonname__           = __addon__.getAddonInfo('name')
__version__             = __addon__.getAddonInfo('version')
__LS__                  = __addon__.getLocalizedString
__icon__                = os.path.join(__addonFolder__, "icon.png")#.encode('utf-8')

WINDOW                  = xbmcgui.Window( 10000 )





FeedFile = xbmc.translatePath('special://home/addons/'+__addonID__+'/NewsFeeds.json').decode('utf-8')
with open(FeedFile, 'r') as feeds:
    ConfigFeeds=feeds.read().rstrip('\n')

BuliFile = xbmc.translatePath('special://home/addons/'+__addonID__+'/Buli.json') #.decode('utf-8')
with open(BuliFile, 'r') as Mannschaften:
    BuliMannschaften=Mannschaften.read().rstrip('\n').decode('utf-8')


# Create Objects
ph   = PluginHelpers()

nv   = NewsVideos()
nls  = NewsLiveStreams()
nwk  = NewsWetterKarten()
nuwz = NewsUWZ()
nb   = NewsBuli()
nf   = NewsFeed()


if len(sys.argv)==3:
    addon_handle = int(sys.argv[1])
    params = ph.parameters_string_to_dict(sys.argv[2])
    methode = urllib.unquote_plus(params.get('methode', ''))
    buliliga = urllib.unquote_plus(params.get('buliliga', ''))
    url = urllib.unquote_plus(params.get('url', ''))
    headerpic = urllib.unquote_plus(params.get('headerpic', ''))
    clickable = urllib.unquote_plus(params.get('clickable', ''))
elif len(sys.argv)>1:
    params = ph.parameters_string_to_dict(sys.argv[1])
    methode = urllib.unquote_plus(params.get('methode', ''))
    buliliga = urllib.unquote_plus(params.get('buliliga', ''))
    url = urllib.unquote_plus(params.get('url', ''))
    headerpic = urllib.unquote_plus(params.get('headerpic', ''))
    clickable = urllib.unquote_plus(params.get('clickable', ''))
else:
    methode = None
    buliliga = 1

if clickable == '':
    clickable = 1

ph.writeLog("Methode in Script: %s" % (methode),level=xbmc.LOGDEBUG )


##########################################################################################################################
## Check methode to process
##########################################################################################################################

## Service
if methode=='start_service':
        WINDOW.setProperty( "LatestNews.Service", "active" )
elif methode=='stop_service':
        WINDOW.setProperty( "LatestNews.Service", "inactive" )



## Skinmode
elif methode=='set_skinmode':
        __addon__.setSetting('skinnermode', 'true')
elif methode=='unset_skinmode':
        __addon__.setSetting('skinnermode', 'false')



## Play Videos
elif methode=='play_tagesschau':
        nv.PlayTagesschau()

elif methode=='play_tagesschau_100':
        nv.PlayTagesschau100()

elif methode=='play_wetteronline':
        nv.PlayWetterOnline()

elif methode=='play_wetterinfo':
        nv.PlayWetterInfo()

elif methode=='play_wetternet':
        nv.PlayWetterNet()

elif methode=='play_tagesschauwetter':
        nv.PlayTagesschauWetter()

elif methode=='play_kinder_nachrichten':
        nv.PlayKinderNachrichten()

elif methode=='play_mdr_aktuell_130':
        nv.PlayMDRAktuell130()

elif methode=='play_rundschau100':
        nv.PlayRundschau100()

elif methode=='play_ndraktuellkompakt':
        nv.PlayNDRAktuellKompakt()



# Play Livestreams
elif methode=='play_livestream_euronews':
        nls.PlayEuronews()

elif methode=='play_livestream_ntv':
        nls.PlayNTV()

elif methode=='play_livestream_n24':
        nls.PlayN24()

elif methode=='play_livestream_tagesschau24':
        nls.PlayTagesschau24()

elif methode=='play_livestream_phoenix':
        nls.PlayPhoenix() 

elif methode=='play_livestream_dw':
        nls.PlayDW()



# Selects
elif methode=='show_select_dialog':
    allfeeds = json.loads(str(ConfigFeeds))
    feedname=[]
    for f in allfeeds:
        feedname.append(f['name'])
    dialog       = xbmcgui.Dialog()
    ret          = dialog.select(str(__LS__(30112)),feedname)
    headerpic    = allfeeds[ret]['pic']
    url          = allfeeds[ret]['url']
    notifyheader = str(__LS__(30010))
    xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30150))+' ,8000,'+__icon__+')')
    nf.feed2property(url, headerpic)

elif methode=='show_livestream_select_dialog':
    dialog = xbmcgui.Dialog()
    ret = dialog.select(__LS__(30190), [__LS__(30191), __LS__(30192), __LS__(30193), __LS__(30194), __LS__(30195), __LS__(30196)])
    if ret == 0:
        nls.PlayTagesschau24()
    elif ret == 1:
        nls.PlayEuronews()
    elif ret == 2:
        nls.PlayNTV()
    elif ret == 3:
        nls.PlayN24()
    elif ret == 4:
        nls.PlayPhoenix()
    elif ret == 5:
        nls.PlayDW()

elif methode=='show_buli_select':
    dialog = xbmcgui.Dialog()
    ret = dialog.select(str(__LS__(30153)), [str(__LS__(30128)), str(__LS__(30129)), str(__LS__(30125)), str(__LS__(30126)), __LS__(30091), __LS__(30092)])
    if ret == 0:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "1" )
        show_bulilist(1)        
    elif ret == 1:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "2" )
        show_bulilist(2)
    elif ret == 2:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "1" )
        show_bulispielplan("1")
    elif ret == 3:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "2" )
        show_bulispielplan(2)
    elif ret == 4:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "1" )
        show_bulinaechsterspieltag(1)
    elif ret == 5:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "2" )
        show_bulinaechsterspieltag(2)




# Settings
elif methode=='set_default_feed':
    allfeeds = json.loads(str(ConfigFeeds))
    feedname=[]
    for f in allfeeds:
        feedname.append(f['name'])

    dialog = xbmcgui.Dialog()
    ret = dialog.select(str(__LS__(30155)),feedname)
    defaultfeedname=allfeeds[ret]['name']
    __addon__.setSetting('storedefault',defaultfeedname)




# Dialogwindows
elif methode=='show_bulilist':
    WINDOW.setProperty("NewsCenter.Buli.LigaInfo", buliliga )
    show_bulilist(buliliga)

elif methode=='show_bulispielplan':
    WINDOW.setProperty("NewsCenter.Buli.LigaInfo", buliliga )
    show_bulispielplan(buliliga)

elif methode=='show_bulinaechsterspieltag':
    WINDOW.setProperty("NewsCenter.Buli.LigaInfo", buliliga )
    show_bulinaechsterspieltag(buliliga)

elif methode=='show_wetter_karte':
    DETAILWIN = xbmcgui.WindowXMLDialog('wetterkarten-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

elif methode=='show_wetter_karte_bundesland':
    DETAILWIN = xbmcgui.WindowXMLDialog('wetterkarten-bundesland-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()




# Container
elif methode=='get_buli_spielplan_items':
    spielelist = nb.get_buli_spielplan_items(buliliga)
    url = '-'
    for sitem in spielelist:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=sitem['Logo'])
        li.setProperty("Spieldatum", str(sitem['Spieldatum']))
        li.setProperty("Mannschaft1", sitem['Mannschaft1'])
        li.setProperty("Mannschaft2", sitem['Mannschaft2'])
        li.setProperty("Mannschaft1Logo", sitem['Mannschaft1Logo'])
        li.setProperty("Mannschaft2Logo", sitem['Mannschaft2Logo'])
        li.setProperty("Ergebniss", str(sitem['Ergebniss']))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


elif methode=='get_buli_table_items':
    bulilist = nb.get_buli_table_items(buliliga)
    url = '-'
    for sitem in bulilist:
        Logo = sitem['Logo']
        Logo = Logo.encode('utf-8')
        li = xbmcgui.ListItem(sitem['Label'], iconImage=Logo)
        li.setProperty("Spiele", str(sitem['Spiele']))
        li.setProperty("SUN", sitem['SUN'])
        li.setProperty("Platz", str(sitem['Platz']))
        li.setProperty("Tore", str(sitem['Tore']))
        li.setProperty("Punkte", str(sitem['Punkte']))
        li.setProperty("StatPic", str(sitem['StatPic']))
        li.setProperty("Logo", str(sitem['Logo']))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


elif methode=='get_buli_naechsterspieltag_items':
    bulilist = nb.get_buli_naechsterspieltag_items(buliliga)
    url = '-'
    for sitem in bulilist:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=__icon__)
        li.setProperty("Mannschaft1", sitem['Mannschaft1'])
        li.setProperty("Mannschaft2", sitem['Mannschaft2'])
        li.setProperty("Mannschaft1Logo", str(sitem['Logo1']))
        li.setProperty("Mannschaft2Logo", str(sitem['Logo2']))
        li.setProperty("Spieldatum", str(sitem['Label']))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)



elif methode=='get_feed_items':
    feedjson = nf.feed2container2()
    for sitem in feedjson:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=sitem['Logo'])
        li.setProperty("Desc", sitem['Desc'])
        li.setProperty("HeaderPic", sitem['HeaderPic'])
        li.setProperty("Date", sitem['Date'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)




# Wetterkarten
elif methode=='get_dwd_pics_base':
        nwk.DWD_Base(clickable)

elif methode=='get_dwd_pics_base_uwz':
        nwk.DWD_Base_UWZ(clickable)

elif methode=='get_dwd_pics_extended':
        nwk.DWD_Extended(clickable)

elif methode=='get_dwd_pics_bundesland':
        nwk.DWD_Bundesland(clickable)

elif methode=='get_dwd_pics_bundesland_uwz':
        nwk.DWD_Bundesland_UWZ(clickable)

elif methode=='get_dwd_pics_base_extended':
        nwk.DWD_Base_Extended(clickable)

elif methode=='get_euronews_wetter_pics':
        nwk.Euronews(clickable)




# Pollen
elif methode=='get_pollen_items':
        npf = NewsPollenflug()
        npf.get_pollen_items()




# Unwetter
elif methode=='get_unwetter_warnungen':
        if __addon__.getSetting('plz') != '':
            nuwz.Warnungen("DE", __addon__.getSetting('plz'))
        else:
            notifyheader= str(__LS__(30010))
            xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30149))+' ,4000,'+__icon__+')')

elif methode=='get_uwz_count':
        if __addon__.getSetting('plz') != '':
            nuwz.WarnAnzahl("DE", __addon__.getSetting('plz'))
        else:
            notifyheader=str(__LS__(30010))
            xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30149))+' ,4000,'+__icon__+')')

elif methode=='get_uwz_maps':
        nwk.UWZ(clickable)

elif methode=='show_unwetter_warnungen':
	show_unwetterwarnungen()




# Default Entry
elif methode=='refresh':
        WINDOW.setProperty( "LatestNews.Service", "active" )
        notifyheader= str(__LS__(30010))
        notifytxt   = str(__LS__(30108))
        xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifytxt+' ,4000,'+__icon__+')')
        allfeeds = json.loads(str(ConfigFeeds))
        storedefault=__addon__.getSetting('storedefault')
        if storedefault != '':
            for f in allfeeds:
                if f['name'] == storedefault:
                    url=f['url']
                    pic=f['pic']
                    break
        else:
            url="http://www.kodinerds.net/index.php/BoardFeed/?at=30575-8e710f12c83d6c7f66184ca3354f2c83baf4bbed"
            pic="http://www.kodinerds.net/images/wbbLogo.png"
        nf.feed2property(url, pic)

        if __addon__.getSetting('plz') != '':
            nuwz.WarnAnzahl("DE", __addon__.getSetting('plz'))
            WINDOW.setProperty( "NewsCenter.PLZ", __addon__.getSetting('plz') )
            WINDOW.setProperty( "NewsCenter.Bundesland", __addon__.getSetting('storebundesland') )
            WINDOW.setProperty( "NewsCenter.Ort", __addon__.getSetting('storeort') )
        else:
            xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30149))+' ,4000,'+__icon__+')')
        # To Remove: LatestDokus Widget
        set_LatestDokus_to_Home('http://doku.cc/api.php?get=new-dokus&page=1')




elif methode==None:
    allfeeds = json.loads(str(ConfigFeeds))
    feedname=[]
    for f in allfeeds:
        feedname.append(f['name'])
    dialog = xbmcgui.Dialog()
    ret = dialog.select("News Auswahl",feedname)
    headerpic=allfeeds[ret]['pic']
    url=allfeeds[ret]['url']
    notifyheader= str(__LS__(30010))
    xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30150))+' ,8000,'+__icon__+')')
    nf.feed2property(url, headerpic)

