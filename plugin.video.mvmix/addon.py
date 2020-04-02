# -*- coding: utf-8 -*-

import xbmcgui,xbmc,xbmcplugin
import sys,urllib,urlparse

from resources.lib import common

iconImage = common.iconimage()
pluginhandle = int(sys.argv[1])

def root():
    addDir('Local Artists','list_local_artists',iconImage,'')
    addDir('Play By Genre','list_tags',iconImage,'')
    addDir('Search Artist','list_artists',iconImage,'')
    artist = common.get_start_artist()
    if artist:
        artist = 'Resume: %s' % artist
        addDir(artist,'play',iconImage,'',add=False)
    artist_list = common.artist_list()
    for a in artist_list:
        artist = a['artist'].encode('utf-8')
        image = a['image']
        cm = []
        u = build_url({'artist': artist, 'mode': 'remove_artist'})
        cm.append( ('Remove Artist', 'Container.Update(%s)' % u) )
        addDir(artist,'play',image,cm)
    xbmcplugin.endOfDirectory(pluginhandle)

def list_tags():
    addDir('Play Genre','play_tag',iconImage,'')
    tag_list = common.tag_list()
    for t in tag_list:
        tag = t['tag'].encode('utf-8')
        cm = []
        u = build_url({'tag': tag, 'mode': 'remove_tag'})
        cm.append( ('Remove Genre', 'Container.Update(%s)' % u) )
        url = build_url({'name': tag, 'mode': 'play_tag', 'image': iconImage})
        item=xbmcgui.ListItem(tag, iconImage="DefaultFolder.png", thumbnailImage=iconImage)
        item.addContextMenuItems( cm )
        xbmcplugin.addDirectoryItem(pluginhandle,url=url,listitem=item,isFolder=True)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def play_tag():
    name = args['name'][0]
    tag = common.get_tag(name)
    if tag:
        from resources.lib import lastfm
        artists = lastfm.get_artists_by_tag(tag)
        if artists:
            play_artists(artists)

def list_artists():
    artist = None
    artist = common.enter_artist()
    artist = artist.decode('utf-8')
    common.log('[mvmixPlayer] artist entered: %s' % (artist.encode('utf-8')))
    if artist:
        addDir(artist.encode('utf-8').strip(),'play','','')
        from resources.lib import lastfm
        artists = lastfm.get_artists(artist)
        common.log('[mvmixPlayer] artists found: %s' % str(len(artists)))
        for a in artists:
            artist = a['artist'].encode('utf-8').strip()
            image = a['image']
            addDir(artist,'play',image,'')
        xbmcplugin.endOfDirectory(pluginhandle)
        
def list_local_artists():
    artists = common.get_local_artists()
    for a in artists:
        artist = a['artist']
        try: artist = artist.encode('utf-8')
        except: pass
        image = a['thumbnail']
        try: image = image.encode('utf-8')
        except: pass
        addDir(artist,'play',image,'',add=False)
    xbmcplugin.addSortMethod(pluginhandle, 1)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def play_artists(artists=False):
    if not artists:
        artists = common.get_local_artists()
    kill_old_process()
    if artists:
        from resources.lib.artist_player import mvmixArtistPlayer
        player = mvmixArtistPlayer()
        player.playArtists(artists)
        while player.is_active and not xbmc.abortRequested:
            player.sleep(200)

def play():
    artist = None
    try:
        artist = args['name'][0]
        image = args['image'][0]
        add = args['add'][0]
        if add == 'True':
            common.artist_list('add',artist,image)
    except:
        pass
    try: artist = args['artist'][0]
    except: pass
    kill_old_process()
    if artist:
        from resources.lib.player import mvmixPlayer
        player = mvmixPlayer()
        player.playArtist(artist)
        while player.is_active and common.process() == 'True' and not xbmc.abortRequested:
            player.sleep(200)
            
def kill_old_process():
    process = common.process()
    if process == 'True':
        common.process_false()
        xbmc.sleep(300)

def list_artist_videos():
    artist = args['artist'][0]
    image = ''
    try: image = args['image'][0]
    except: pass
    add = str(args['add'][0])
    if add == 'True': 
        common.artist_list('add',artist,image)
    from resources.lib import videos as __videos__
    videos = __videos__.get_videos(artist)
    for video in videos:
        artist = common.utf_enc(video['artist'][0])
        title = common.utf_enc(video['title'])
        name = '%s - %s' % (artist,title)
        u = build_url({'site': video['site'], 'id': video['id'], 'name':name, 'mode': 'play_video'})
        listitem = xbmcgui.ListItem(title, thumbnailImage=video['image'])
        listitem.setInfo(type='Video', infoLabels={'Duration':video['duration']})
        listitem.setProperty('IsPlayable', 'true')
        cm = []
        q = build_url({'u':u, 'name':name, 'mode':'queue_video', 'image':video['image']})
        cm.insert(0, ('Add to Playlist', 'XBMC.RunPlugin(%s)' % q) )
        i = build_url({'site': video['site'], 'id': video['id'], 'mode': 'ignore_video'})
        cm.append( ('Ignore Video', 'Container.Update(%s)' % i) )
        if cm:
            listitem.addContextMenuItems( cm )
        if not video['duration'] or video['duration'] > 120:
            xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=listitem)
    xbmcplugin.addSortMethod(pluginhandle, 1)
    xbmcplugin.endOfDirectory(pluginhandle)

def queue_video():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    name = args['name'][0]
    u = args['u'][0]
    image = args.get('image', '')
    if image:
        image = image[0]
    listitem = xbmcgui.ListItem(name, thumbnailImage=image)
    listitem.setProperty('IsPlayable', 'true')
    playlist.add(url=u, listitem=listitem)
    
def play_video():
    _id = args['id'][0]
    site = args['site'][0]
    name = args.get('name', [''])[0]
    video_url = common.import_site(site).get_video_url(_id)
    if video_url:
        listitem = xbmcgui.ListItem(name, path=video_url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    
def addDir(name,mode,image,cm,add=True):
    item_name = name
    if name.startswith('Resume: '):
        name = name.replace('Resume: ','')
    url = build_url({'name': name, 'mode': mode, 'image': image, 'add': add})
    item=xbmcgui.ListItem(item_name, iconImage="DefaultFolder.png", thumbnailImage=image)
    if not cm: cm = []
    if not name == 'Search Artist' and not name == 'Local Artists':
        u = build_url({'artist': name, 'mode': 'list_artist_videos', 'image': image, 'add': add})
        cm.insert(0, ('Show Artist Videos', 'Container.Update(%s)' % u) )
    if name == 'Local Artists':
        u = build_url({'mode': 'play_artists'})
        cm.insert(0, ('Play Local Artists', 'XBMC.RunPlugin(%s)' % u) )
    if cm:
        item.addContextMenuItems( cm )
    xbmcplugin.addDirectoryItem(pluginhandle,url=url,listitem=item,isFolder=True)

def ignore_video():
    _id = args['id'][0]
    site = args['site'][0]
    data = {'site':site, 'id':_id}
    common.ignore_list('add',data)

def remove_artist():
    artist = args['artist'][0]
    common.artist_list('delete',artist)

def remove_tag():
    tag = args['tag'][0]
    common.tag_list('delete',tag)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)
    
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
common.log('Arguments: '+str(args))

if mode==None:
    root()
else:
    exec '%s()' % mode[0]