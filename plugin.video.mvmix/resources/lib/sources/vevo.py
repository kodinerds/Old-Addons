# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests

site = 'vevo'
headers = {'User-Agent':'iPad','X-Requested-With': 'XMLHttpRequest'}

def get_videos(artist):
    videos = []
    token = get_token()
    artist_id = get_artist_id(artist,token)
    if artist_id:
        try:
            url = 'https://apiv2.vevo.com/artist/%s/videos' % str(artist_id)
            headers['Authorization'] = 'Bearer '+token
            params = {'size':'200', 'page':'1'}
            json_data = requests.get(url, headers=headers, params=params).json()
        except:
            return False
        try:
            for v in json_data['videos']:
                try:
                    _id = v['isrc']
                    title = v['title']
                    image = v['thumbnailUrl']
                    duration = ''
                    try:
                        duration = v['duration']
                    except:
                        pass
                    if v['categories'][0] == 'Music Video':
                        videos.append({'site':site, 'artist':[artist], 'title':title, 'duration':duration, 'id':_id, 'image':image})
                except:
                    pass
        except:
            pass
    elif artist_id == False:
        return False
    return videos
    
def get_video_url(_id):
    video_url = None
    try:
        token = get_token()
        url = 'https://apiv2.vevo.com/video/%s/streams/mp4' % str(_id)
        headers['Authorization'] = 'Bearer '+token
        json_data = requests.get(url, headers=headers).json()
        for q in json_data:
            if q['quality'].lower() == 'high':
                video_url = q['url']
                break
    except:
        pass
    return video_url

def get_artist_id(artist,token):
    artist_id = None
    try:
        url = 'https://apiv2.vevo.com/search'
        headers['Authorization'] = 'Bearer '+token
        params = {'q':artist, 'includecategories':'music video'}
        json_data = requests.get(url, headers=headers, params=params).json()
        artists = json_data['artists']
        for a in artists:
            if a['name'].encode('utf-8').lower() == artist.lower():
                artist_id = a['urlSafeName']
                break
    except:
        return False
    return artist_id

def get_token():
    token = ''
    try:
        url = 'https://accounts.vevo.com/token'
        post_data = {'client_id': 'SPupX1tvqFEopQ1YS6SS', 'grant_type': 'urn:vevo:params:oauth:grant-type:anonymous'}
        json_data = requests.post(url, headers=headers, data=post_data).json()
        token = json_data['legacy_token']
    except:
        pass
    return token
