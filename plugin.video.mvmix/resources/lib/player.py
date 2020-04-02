# -*- coding: utf-8 -*-

import xbmc,xbmcgui,xbmcplugin
import random,sys

import lastfm
import common
import resume
import videos as _videos_

class mvmixPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        xbmc.Player.__init__( self )

    def playArtist(self,artist):
        self.is_active = True
        common.process_true()
        common.limit_artists(common.limit_result())
        self.similar_artists = []
        self.ignore_list = []
        self.video_list = []
        self.genre_list = lastfm.get_artist_genre(artist)
        self.start_artist = artist
        self.last_artist = self.start_artist
        self.artist = artist
        self.set_resume_point()
        self.playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self.clear_playlist()
        self.add_video(artist)
        self.play(self.playlist)

    def onPlayBackStarted(self):
        common.log('[mvmixPlayer] playback started')
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
        if not artist:
            self.similar_artists = lastfm.get_similar_artists(self.artist)
        while not video_url and not xbmc.abortRequested and self.is_active:
            loops += 1
            self.set_artist(artist)
            self.artist = common.utf_enc(self.artist)
            common.log('[mvmixPlayer] loop: %s' % str(loops))
            common.log('[mvmixPlayer] artist: %s' % str(self.artist))
            videos = _videos_.get_videos(self.artist)
            videos = self.remove_added_videos(videos)
            common.log('[mvmixPlayer] videos found: %s' % str(len(videos)))
            if videos:
                common.limit_artists(common.limit_result())
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
                self.add_to_ignore_list()
            if artist and not video_url and not self.similar_artists:
                self.similar_artists = lastfm.get_similar_artists(artist)
            resume_point = {'start_artist': self.start_artist, 'artist': self.artist,
                            'genre_list': self.genre_list, 'video_list': self.video_list,
                            'ignore_list': self.ignore_list}
            resume.save_resume_point(resume_point)
            self.sleep(500)
            if loops == 20:
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

    def set_similiar_artists(self):
        if int(common.limit_artists()) <= 50 or not self.similar_artists:
            common.limit_artists(int(common.limit_artists())+5)
            self.similar_artists = lastfm.get_similar_artists(self.last_artist)
        elif int(common.limit_artists()) > 50:
            self.similar_artists = lastfm.get_similar_artists(self.last_artist)
            if self.similar_artists:
                self.last_artist = self.similar_artists[random.randint(0,(len(self.similar_artists)-1))]
        
    def set_artist(self,a):
        next_artist = False
        loop = 0
        if a and not self.similar_artists:
            return
        while not next_artist and not xbmc.abortRequested and self.is_active:
            loop += 1
            self.remove_ignored_artists()
            for x in range(0,10):
                if self.similar_artists:
                    artist = self.similar_artists[random.randint(0,(len(self.similar_artists)-1))]
                    genres = lastfm.get_artist_genre(artist)
                    if lastfm.compare_genres(self.genre_list,genres) == True:
                        self.artist = artist
                        next_artist = True
                        break
                    else:
                        self.add_to_ignore_list(artist)
                        self.remove_ignored_artists()
            if not next_artist:
                self.set_similiar_artists()
            if loop == 20:
                break
            
    def add_to_ignore_list(self, artist=False):
        if not artist:
            artist = self.artist
        if not artist in self.ignore_list:
            self.ignore_list.append(artist)
            self.remove_ignored_artists()
        
    def remove_ignored_artists(self):
        try:
            if self.similar_artists and self.ignore_list:
                for a in self.similar_artists[:]:
                    for b in self.ignore_list:
                        if a == b:
                            self.similar_artists.remove(a)
        except:
            pass
            
    def set_resume_point(self):
        resume_point = resume.get_resume_point()
        if resume_point:
            try:
                if self.start_artist == resume_point['start_artist']:
                    try: self.start_artist = resume_point['start_artist']
                    except: pass
                    try: self.artist = resume_point['artist']
                    except: pass
                    try: self.genre_list = resume_point['genre_list']
                    except: pass
                    try: self.video_list = resume_point['video_list']
                    except: pass
                    try: self.ignore_list = resume_point['ignore_list']
                    except: pass
            except:
                pass