# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import subprocess
import sys
import os
import xbmcgui
import subprocess, platform
import pyxbmct

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__settings__            = xbmcaddon.Addon(id="script.skinhelper.ping")

WINDOW = xbmcgui.Window(10000)

def Ping(hostname,kodiproperty,onpix,offpix):
        DETACHED_PROCESS = 8
        response=0
        if platform.system() == "Windows":
           command="ping "+hostname+" -n 1 -w 1000"
           response = subprocess.call(command,creationflags=DETACHED_PROCESS)
        else:
           command="ping -w 1 -c 1 " + hostname
           result = os.popen(command).read()
           if ("100%" in result):
              response = 1
           else:
              response = 0
        
        if response == 1:
           WINDOW.setProperty(kodiproperty,offpix)
           return False
        else:
           WINDOW.setProperty(kodiproperty,onpix)
           return True
   
def wake(mac):
        xbmc.executebuiltin("WakeOnLan(" + mac + ")")
        
def Note(host):
        hostname = __settings__.getSetting(host)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("WOL","Wake Up Server " + hostname, 3000, __icon__))
