# -*- coding: utf-8 -*-

import xbmc,xbmcgui,xbmcplugin
import random,sys

import common
import videos as __videos__

class mvmixArtistPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        xbmc.Player.__init__( self )

    def playArtists(self,artists):
        self.is_active = True
        self.artists = artists
        self.video_list = []
        self.playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self.clear_playlist()
        self.add_video()
        self.play(self.playlist)

    def onPlayBackStarted(self):
        common.log('[mvmixArtistPlayer] playback started')
        self.sleep(2000)
        if (xbmc.Player().isPlayingVideo()):
            title = 'Now playing:'
            name = xbmc.getInfoLabel('VideoPlayer.Title')
            cover = xbmc.getInfoImage('VideoPlayer.Cover')
            xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title, name.replace(',',''), 15*1000, cover))
            self.add_video()
            self.add_next_video()      

    def onPlayBackStopped(self):
        common.log('[mvmixPlayer] playback stopped')
        self.is_active = False
        self.clear_playlist()
    
    def sleep(self, s):
        xbmc.sleep(s)
        
    def clear_playlist(self):
        self.playlist.clear()
        
    def add_video(self,artist=False):
        common.log('[mvmixPlayer] add video')
        video_url = None
        loops = 0
        while not video_url and not xbmc.abortRequested and self.is_active:
            self.set_artist()
            common.log('[mvmixPlayer] loops: %s' % str(loops))
            common.log('[mvmixPlayer] artist: %s' % str(self.artist))
            videos = __videos__.get_videos(self.artist)
            videos = self.remove_added_videos(videos)
            common.log('[mvmixPlayer] videos found: %s' % str(len(videos)))
            if videos:
                video = videos[random.randint(0,(len(videos)-1))]
                self.video_list.append(video)
                video_url = common.import_site(video['site']).get_video_url(video['id'])
                if video_url:
                    artist = common.utf_enc(video['artist'][0])
                    title = common.utf_enc(video['title'])
                    name = '%s - %s' % (artist,title)
                    listitem = xbmcgui.ListItem(name, thumbnailImage=video['image'])
                    self.playlist.add(video_url, listitem=listitem)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, listitem)
            else:
                self.remove_artist_from_list()
            self.sleep(500)
            loops += 1
            if loops == 20:
                self.video_list = []
            elif loops > 30:
                self.is_active = False
                break

    def add_next_video(self):
        result = 2
        if (xbmc.Player().isPlayingVideo()):
            try: result = (int(xbmc.getInfoLabel('Playlist.Length(video)')) - int(xbmc.getInfoLabel('Playlist.Position(video)')))
            except: pass
            if result < 2:
                self.add_video()

    def remove_added_videos(self, videos):
        try:
            if videos and self.video_list:
                for v in videos[:]:
                    for v_l in self.video_list:
                        if v['title'] == v_l['title']:
                            videos.remove(v)
        except:
            pass
        return videos
        
    def remove_artist_from_list(self):
        self.artists = [x for x in self.artists if x['artist'] != self.artist]

    def set_artist(self):
        artist = self.artists[random.randint(0,(len(self.artists)-1))]
        self.artist = common.utf_enc(artist['artist'])