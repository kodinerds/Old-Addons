# -*- coding: utf-8 -*-

import xbmc,xbmcvfs
import json,os,re

from resources.lib import common

site = 'local'

def get_videos(name):
    videos = []
    if common.video_source() == 'Music Video Library':
        videos = get_videos_from_library(name)
    else:
        if common.video_path():
            videos = get_videos_from_folder(name)
    return videos
    
def get_video_url(_id):
    return _id

def get_videos_from_library(name):
    videos = []
    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": { "properties": [ "title", "artist", "runtime", "file", "streamdetails", "thumbnail" ] }, "id": "libMusicVideos"}')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    json_response = json.loads(json_query)
    if json_response.has_key('result') and json_response['result'] != None and json_response['result'].has_key('musicvideos'):
        for mv in json_response['result']['musicvideos']:
            try:
                artists = mv['artist']
                title = mv['title']
                _id = mv['file'].encode('utf-8')
                duration = mv['runtime']
                image = mv['thumbnail']
                if artists[0].encode('utf-8').lower() == name.lower():
                    videos.append({'site':site, 'artist':artists, 'title':title, 'duration':duration, 'id':_id, 'image':image})
            except:
                pass
    return videos

def get_videos_from_folder(name):

    video_path = common.video_path()
    videos = []
    
    def add_videos(path,videos):
        dirs, files = xbmcvfs.listdir(path)
        for f in files:
            if f.endswith(('.strm','.webm','.mkv','.flv','.vob','.ogg','.avi','.mov','.qt','.wmv','.rm','.asf','.mp4','.m4v','.mpg','.mpeg','.3gp')):
                try:
                    _id = os.path.join(path, f)
                    filename = os.path.splitext(os.path.basename(_id))[0]
                    filename = re.sub('\_|\.', ' ', filename)
                    match = filename.split(' - ')
                    if len(match) == 1:
                        match = filename.split('-')
                    artist = match[0].strip()
                    title = match[1].strip()
                    if artist.lower() == name.lower():
                        videos.append({'site':site, 'artist':[artist], 'title':title, 'duration':'', 'id':_id, 'image':''})
                except:
                    pass
        return videos

    dirs, files = xbmcvfs.listdir(video_path)
    for d in dirs:
        path = os.path.join(video_path, d)
        videos = add_videos(path,videos)
    
    videos = add_videos(video_path,videos)
    
    return videos
