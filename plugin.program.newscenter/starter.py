#!/usr/bin/python
###########################################################################
#
#          FILE:  plugin.program.newscenter/starter.py
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

import os,sys,xbmc,xbmcgui,xbmcaddon
from resources.lib.NewsBuli import PluginHelpers
from resources.lib.NewsWetterKarten import NewsCenterGeoHelper

__addon__     = xbmcaddon.Addon()
__addonID__   = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__version__   = __addon__.getAddonInfo('version')
__path__      = __addon__.getAddonInfo('path')
__LS__        = __addon__.getLocalizedString
__icon__      = xbmc.translatePath(os.path.join(__path__, 'icon.png'))


WINDOW         = xbmcgui.Window( 10000 )
ph             = PluginHelpers()

##############################################################################################################################
##
##
##
##############################################################################################################################
class MyMonitor( xbmc.Monitor ):
    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def __init__( self, *args, **kwargs ):
        xbmc.Monitor.__init__( self )

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def onSettingsChanged( self ):
        if self.settings_setlocation() == 1:
            self.settings_initialize()

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def get_settings(self):
        ph.writeLog("Settings (re)loaded")
        self.show_tagesschau         = __addon__.getSetting('show_tagesschau').strip()
        self.show_tagesschau100      = __addon__.getSetting('show_tagesschau100').strip()
        self.show_mdraktuell         = __addon__.getSetting('show_mdraktuell')
        self.show_ndrkompakt         = __addon__.getSetting('show_ndrkompakt')
        self.show_brrundschau100     = __addon__.getSetting('show_brrundschau100')
        self.show_kindernews         = __addon__.getSetting('show_kindernews')
        self.show_tagesschauwetter   = __addon__.getSetting('show_tagesschauwetter')
        self.show_wetter60           = __addon__.getSetting('show_wetter60')
        self.show_wetterinfo         = __addon__.getSetting('show_wetterinfo')
        self.show_wetternet          = __addon__.getSetting('show_wetternet')
        self.show_unwetter_warn_icon = __addon__.getSetting('show_unwetter_warn_icon')
        self.skinnermode             = __addon__.getSetting('skinnermode')
        self.enableinfo              = __addon__.getSetting('enableinfo')
        self.refreshcontent          = int(__addon__.getSetting('mdelay')) * 60

        ph.writeLog('Show notifications:            %s' % (self.enableinfo))
        ph.writeLog('Refresh Intervall :            %s' % (self.refreshcontent))
        ph.writeLog('Skinner Mode:                  %s' % (self.skinnermode))
        ph.writeLog('Show Video Tagesschau:         %s' % (self.show_tagesschau), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video Tagesschau100:      %s' % (self.show_tagesschau100), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video MDR Aktuell:        %s' % (self.show_mdraktuell), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video NDR Kompakt:        %s' % (self.show_ndrkompakt), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video BR Rundschau:       %s' % (self.show_brrundschau100), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video Kindernews:         %s' % (self.show_kindernews), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video Tagesschau Wetter:  %s' % (self.show_tagesschauwetter), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video Wetter Online:      %s' % (self.show_wetter60), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video Wetter Info:        %s' % (self.show_wetterinfo), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Video Wetter Net:         %s' % (self.show_wetternet), level=xbmc.LOGDEBUG)
        ph.writeLog('Show Thunderstorm Warn Icon:   %s' % (self.show_unwetter_warn_icon), level=xbmc.LOGDEBUG)

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def set_visible_properties(self):
        ph = PluginHelpers()
        ph.writeLog("Make userselection visible", level=xbmc.LOGDEBUG)
        WINDOW.setProperty("NewsCenter.Visible.Tagesschau",        self.show_tagesschau)
        WINDOW.setProperty("NewsCenter.Visible.Tagesschau100",     self.show_tagesschau100)
        WINDOW.setProperty("NewsCenter.Visible.MDRAktuell",        self.show_mdraktuell)
        WINDOW.setProperty("NewsCenter.Visible.NDRKompakt",        self.show_ndrkompakt)
        WINDOW.setProperty("NewsCenter.Visible.BRRundschau100",    self.show_brrundschau100)
        WINDOW.setProperty("NewsCenter.Visible.KinderNachrichten", self.show_kindernews)
        WINDOW.setProperty("NewsCenter.Visible.TagesschauWetter",  self.show_tagesschauwetter)
        WINDOW.setProperty("NewsCenter.Visible.Wetter60",          self.show_wetter60)
        WINDOW.setProperty("NewsCenter.Visible.WetterInfo",        self.show_wetterinfo)
        WINDOW.setProperty("NewsCenter.Visible.WetterNet",         self.show_wetternet)
        WINDOW.setProperty("NewsCenter.Visible.UnwetterWarnIcon",  self.show_unwetter_warn_icon)

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def settings_setlocation(self):
        plz = __addon__.getSetting('plz')
        gh = NewsCenterGeoHelper()
        ort = gh.plz2ort(plz)
        bundesland = gh.plz2bundesland(plz)
        if unicode(__addon__.getSetting('storeort'),'utf-8') != ort:
            __addon__.setSetting('storeort',ort) 
            __addon__.setSetting('storebundesland',bundesland) 
            return 0
        return 1

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def settings_initialize(self):
        ph = PluginHelpers()
        ph.writeLog("Settings (re)loaded")
        self.get_settings()
        self.set_visible_properties()
        xbmc.executebuiltin('XBMC.RunScript(plugin.program.newscenter,"?methode=refresh")')




##############################################################################################################################
##
##
##
##############################################################################################################################
class Starter():
    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def __init__(self):
        self.enableinfo = False
        self.refreshcontent = 0

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def stop(self):
        ph = PluginHelpers()
        ph.writeLog('Stopping %s' % (__addonname__))

    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def start(self):
        ph = PluginHelpers()
        ph.writeLog('Starting %s V.%s' % (__addonname__, __version__))

        monitor = MyMonitor()
        monitor.settings_initialize()

        ph.notifyOSD(__LS__(30010), __LS__(30106), __icon__, enabled=monitor.enableinfo)
        
        while not monitor.abortRequested():
            if ( monitor.waitForAbort(monitor.refreshcontent) | monitor.refreshcontent == 0 ):
                self.stop()
                break
            monitor.skinnermode = __addon__.getSetting('skinnermode')
            if monitor.skinnermode == 'True':
                shouldrun = WINDOW.getProperty( "LatestNews.Service" )
                if shouldrun == "active":
                    ph.notifyOSD(__LS__(30010), __LS__(30108), __icon__, enabled=monitor.enableinfo)
                    xbmc.executebuiltin('XBMC.RunScript(plugin.program.newscenter,"?methode=refresh")')
            else:
                ph.notifyOSD(__LS__(30010), __LS__(30108), __icon__, enabled=monitor.enableinfo)
                xbmc.executebuiltin('XBMC.RunScript(plugin.program.newscenter,"?methode=refresh")')

        self.stop()
    

##########################################################################################################################
##########################################################################################################################
##
##                                                       M  A  I  N
##
##########################################################################################################################
##########################################################################################################################


if __name__ == '__main__':
    starter = Starter()
    starter.start()
    del starter

