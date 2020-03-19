#!/usr/bin/python
###########################################################################
#
#          FILE:  plugin.program.tvhighlights/starter.py
#
#        AUTHOR:  Tobias D. Oestreicher
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.1.5
#       CREATED:  05.02.2016
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
#     CHANGELOG:  (02.09.2015) TDOe - First Publishing
###########################################################################

import os,re,xbmc,xbmcgui,xbmcaddon

__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__path__ = __addon__.getAddonInfo('path')
__LS__ = __addon__.getLocalizedString
__icon__ = xbmc.translatePath(os.path.join(__path__, 'icon.png'))

OSD = xbmcgui.Dialog()

# Helpers #

def notifyOSD(header, message, icon=xbmcgui.NOTIFICATION_INFO, disp=4000, enabled=True):
    if enabled:
        OSD.notification(header.encode('utf-8'), message.encode('utf-8'), icon, disp)

def writeLog(message, level=xbmc.LOGNOTICE):
        xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  message.encode('utf-8')), level)

# End Helpers #

_mdelay = int(re.match('\d+', __addon__.getSetting('mdelay')).group())
_screenrefresh = int(re.match('\d+', __addon__.getSetting('screenrefresh')).group())

writeLog('Content refresh: %s mins, screen refresh: %s mins' % (_mdelay, _screenrefresh), level=xbmc.LOGDEBUG)

class MyMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs ):
        xbmc.Monitor.__init__(self)
        self.settingsChanged = False

    def onSettingsChanged(self):
        self.settingsChanged = True

class Starter():

    def __init__(self):
        self.enableinfo = False
        self.showOutdated = False
        self.prefer_hd = True
        self.mdelay = 0
        self.screenrefresh = 0

    def getSettings(self):
        self.enableinfo = True if __addon__.getSetting('enableinfo').upper() == 'TRUE' else False
        self.showOutdated = True if __addon__.getSetting('showOutdated').upper() == 'TRUE' else False
        self.prefer_hd = True if __addon__.getSetting('prefer_hd').upper() == 'TRUE' else False
        self.mdelay = int(re.match('\d+', __addon__.getSetting('mdelay')).group()) * 60
        self.screenrefresh = int(re.match('\d+', __addon__.getSetting('screenrefresh')).group()) * 60
        self.delay = int(re.match('\d+', __addon__.getSetting('delay')).group()) * 1000
        self.refreshcontent = self.mdelay/self.screenrefresh
        self.mincycle = int(re.match('\d+', __LS__(30151)).group()) * 60
        self.poll = self.screenrefresh/self.mincycle

        writeLog('Settings (re)loaded')
        writeLog('Show notifications:       %s' % (self.enableinfo), level=xbmc.LOGDEBUG)
        writeLog('Show outdated Broadcasts: %s' % (self.showOutdated), level=xbmc.LOGDEBUG)
        writeLog('Prefer HD channel:        %s' % (self.prefer_hd), level=xbmc.LOGDEBUG)
        writeLog('Scraper start delay:      %s msecs' % (self.delay), level=xbmc.LOGDEBUG)
        writeLog('Refresh interval content: %s secs' % (self.mdelay), level=xbmc.LOGDEBUG)
        writeLog('Refresh interval screen:  %s secs' % (self.screenrefresh), level=xbmc.LOGDEBUG)
        writeLog('Refreshing multiplicator: %s' % (self.refreshcontent), level=xbmc.LOGDEBUG)
        writeLog('Poll cycles:              %s' % (self.poll), level=xbmc.LOGDEBUG)

        if self.delay > 0:
            xbmc.sleep(self.delay)

        xbmc.executebuiltin('XBMC.RunScript(plugin.program.tvhighlights,"?methode=scrape_highlights")')

    def start(self):
        writeLog('Starting %s V.%s' % (__addonname__, __version__))
        notifyOSD(__LS__(30010), __LS__(30106), __icon__, enabled=self.enableinfo)
        self.getSettings()

        ## Thoughts: refresh = 5m; refresh-content=120 => i-max=120/5;

        _c = 0
        _pc = 0
        monitor = MyMonitor()
        while not monitor.abortRequested():
            if monitor.settingsChanged:
                self.getSettings()
                monitor.settingsChanged = False
            if monitor.waitForAbort(self.mincycle):
                break
            _pc += 1
            if _pc < self.poll:
                continue
            _c += 1
            _pc = 0
            if _c >= self.refreshcontent:
                writeLog('Scrape TV Today Highlights')
                notifyOSD(__LS__(30010), __LS__(30018), __icon__, enabled=self.enableinfo)
                xbmc.executebuiltin('XBMC.RunScript(plugin.program.tvhighlights,"?methode=scrape_highlights")')
                _c = 0
            else:
                notifyOSD(__LS__(30010), __LS__(30109), __icon__, enabled=self.enableinfo)
                if not self.showOutdated:
                    writeLog('Refresh content on home screen')
                    xbmc.executebuiltin('XBMC.RunScript(plugin.program.tvhighlights,"?methode=refresh_screen")')

if __name__ == '__main__':
    starter = Starter()
    starter.start()
    del starter
