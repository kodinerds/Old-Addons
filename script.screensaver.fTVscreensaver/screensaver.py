#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Sebastian Sänger (su4lfred@gmail)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import xbmcaddon
import xbmc
import xbmcgui
import thread
from time import time
import json
import urllib
import random
import xbmcvfs

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path').decode("utf-8")

class Screensaver(xbmcgui.WindowXMLDialog):

    refresh_prop = 0 #when to refresh the properties
    refresh_media = 0 #when to refresh the media list    
    WINDOW = None #object representing the home window
    kodi_tvshows = None #array for tv shows
    kodi_videos = None #array for movie files
    images = None #array for image folder
    images_index = 0
    tv_index = 0
    movie_index = 0

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def onInit(self):        
        #init        
        self.log("fTVscreensaver Started")
        self.WINDOW = xbmcgui.Window(10000)
        self.kodi_tvshows = list()
        self.kodi_videos = list()
        self.WINDOW.setProperty('fTVscreensaver.Ready',"")
        self.abort_requested = False
        self.started = False
        self.exit_monitor = self.ExitMonitor(self.exit)
        #get settings
        self.DimEnabled = addon.getSetting('DimEnabled')
        self.DimTimer = addon.getSetting('DimTimer')
        self.DimLevel = addon.getSetting('DimLevel')
        self.ScrollSpeed = addon.getSetting('scrollspeed')
        #set dim
        if self.DimEnabled == 'true':
            xbmcgui.Window(10000).setProperty('fTVscreensaver.Dim', '1')
            xbmcgui.Window(10000).setProperty('fTVscreensaver.DimTimer', self.DimTimer)
            xbmcgui.Window(10000).setProperty('fTVscreensaver.DimLevel', self.DimLevel)
        #set scrollspeed
        xbmcgui.Window(10000).setProperty('fTVscreensaver.Scrollspeed', self.ScrollSpeed)
        #grab images and set properties
        self.scanContent()        
        self.slideshow()

    def slideshow(self):
        # Use custom image folder
        if addon.getSetting('source') == '1': 
            while not self.abort_requested:
                if(time() >= self.refresh_prop):                    
                    foundImages = len(self.images)                             
                    if(len(self.images) > 0):                        
                        try:    
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.1',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.2',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.3',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.4',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.5',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.6',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.7',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.8',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.9',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.10',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.11',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.12',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.13',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.14',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.15',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.16',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.1',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.2',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.3',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.4',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.5',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.6',self.images[self.randomNum(foundImages)])
                            self.WINDOW.setProperty('fTVscreensaver.Poster.7',self.images[self.randomNum(foundImages)])                            
                        except IndexError:
                            pass                    
                    refresh_interval = int(addon.getSetting('refresh'))                     
                    self.refresh_prop = time() + refresh_interval
                    self.WINDOW.setProperty('fTVscreensaver.Ready',"true")        
                if self.abort_requested:
                    self.log('fTVscreensaver abort_requested')
                    self.exit()
                    return
                xbmc.sleep(500)
        # Use Kodi library via JSON
        else:
            while not self.abort_requested:
                if(time() >= self.refresh_prop):                    
                    foundVideos = len(self.kodi_videos)                    
                    if(len(self.kodi_videos) > 0):    
                        try:    
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.1',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.2',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.3',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.4',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.5',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.6',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.7',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.8',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.9',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.10',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.11',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.12',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.13',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.14',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.15',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.FanArt.16',self.kodi_videos[self.randomNum(foundVideos)].fan_art)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.1',self.kodi_videos[self.randomNum(foundVideos)].poster)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.2',self.kodi_videos[self.randomNum(foundVideos)].poster)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.3',self.kodi_videos[self.randomNum(foundVideos)].poster)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.4',self.kodi_videos[self.randomNum(foundVideos)].poster)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.5',self.kodi_videos[self.randomNum(foundVideos)].poster)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.6',self.kodi_videos[self.randomNum(foundVideos)].poster)
                            self.WINDOW.setProperty('fTVscreensaver.Poster.7',self.kodi_videos[self.randomNum(foundVideos)].poster)                            
                        except IndexError:
                            pass                    
                    refresh_interval = int(addon.getSetting('refresh'))                     
                    self.refresh_prop = time() + refresh_interval
                    self.WINDOW.setProperty('fTVscreensaver.Ready',"true")        
                if self.abort_requested:
                    self.log('fTVscreensaver abort_requested')
                    self.exit()
                    return
                xbmc.sleep(500)

    def exit(self):
        self.abort_requested = True

        #Clear properties
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.1')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.2')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.3')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.4')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.5')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.6')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.7')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.8')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.9')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.10')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.11')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.12')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.13')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.14')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.15')
        self.WINDOW.clearProperty('fTVscreensaver.FanArt.16')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.1')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.2')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.3')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.4')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.5')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.6')
        self.WINDOW.clearProperty('fTVscreensaver.Poster.7')
        self.WINDOW.clearProperty('fTVscreensaver.Dim')
        self.WINDOW.clearProperty('fTVscreensaver.StartLoop')
        self.WINDOW.clearProperty('fTVscreensaver.DimTimer')
        self.WINDOW.clearProperty('fTVscreensaver.DimLevel')

        self.exit_monitor = None
        self.log('exit')
        self.close()

    def log(self, msg):
        xbmc.log(u'fTV Screensaver: %s' % msg)

    def scanContent(self):     
        # Use custom image folder
        if addon.getSetting('source') == '1':
            path = addon.getSetting('path')
            self.images = self.scanFolder(path)            
        # Use Kodi library via JSON
        else:
            # Fetch movies
            media_array = self.getJSON('VideoLibrary.GetMovies','{"properties":["title","art","year","file","plot"]}')                
            if(media_array != None and media_array.has_key('movies')):
                self.kodi_videos = list()    #reset the list
                self.movie_index = 0                
                for aMovie in media_array['movies']:
                    newMedia = XbmcMedia()
                    newMedia.title = aMovie['title']                    
                    if(aMovie['art'].has_key('fanart')):
                        newMedia.fan_art = aMovie['art']['fanart']
                    if(aMovie['art'].has_key('poster')):
                        newMedia.poster = aMovie['art']['poster']
                    if(newMedia.verify()):
                        self.kodi_videos.append(newMedia)
                random.shuffle(self.kodi_videos)                
            self.log("found movies " + str(len(self.kodi_videos)))            
            media_array = self.getJSON('VideoLibrary.GetTVShows','{"properties":["title","art","year","file","plot"]}')
            # Fetch tv shows
            if(media_array != None and media_array.has_key('tvshows')):
                self.kodi_tvshows = list()
                self.tv_index = 0                 
                for aShow in media_array['tvshows']:
                    newMedia = XbmcMedia()
                    newMedia.title = aShow['title']                    
                    if(aShow['art'].has_key('fanart')):
                        newMedia.fan_art = aShow['art']['fanart']
                    if(aShow['art'].has_key('poster')):
                        newMedia.poster = aShow['art']['poster']
                    if(newMedia.verify()):
                        self.kodi_videos.append(newMedia) #join fetched shows to the movie list
                random.shuffle(self.kodi_videos)
            self.log("found tv " + str(len(self.kodi_tvshows)))
                
    def scanFolder(self, path):
        #Scan set folder for images with png and jpg extension
        self.log('scanFolder started with path: %s' % repr(path))
        dirs, files = xbmcvfs.listdir(path)
        images = [
            xbmc.validatePath(path + f) for f in files
            if f.lower()[-3:] in ('jpg', 'png')
        ]
        if addon.getSetting('recursive') == 'true':
            for directory in dirs:
                if directory.startswith('.'):
                    continue
                images.extend(
                    self.scanFolder(
                        xbmc.validatePath('/'.join((path, directory, '')))
                    )
                )
        self.log('scanFolder ends')
        return images

    def getJSON(self,method,params):
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "' + method + '" , "params" : ' + params + ' , "id":1 }')
        jsonobject = json.loads(json_response.decode('utf-8','replace'))       
        if(jsonobject.has_key('result')):
            return jsonobject['result']
        else:
            self.log("no result " + str(jsonobject),xbmc.LOGDEBUG)
            return None

    def randomNum(self,size):
        #return random number from 0 to x-1
        return random.randint(0,size -1)

class XbmcMedia:
    title = ''
    fan_art = ''
    poster = ''
    logo = ''
    plot = ''
    season = ''
    episode = ''
    thumb = ''
    path = ''
    
    def verify(self):
        result = True
        if(self.title == '' or self.fan_art == '' or self.poster == ''):
            result = False
        return result

if __name__ == '__main__':
    screensaver = Screensaver(
        'script-fTV-screensaver-main.xml',
        addon_path,
        'default',
    )
    screensaver.doModal()
    del screensaver
    sys.modules.clear()
