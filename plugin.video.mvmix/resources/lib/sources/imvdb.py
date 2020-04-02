# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
import urllib

site = 'imvdb'
headers = {'IMVDB-APP-KEY': 'hjyG4SOzr73y6Prb95G1jeeIG1z5HwkYQTFULuud'}

def get_videos(artist):
    videos = []
    try:
        url = 'https://imvdb.com/api/v1/search/videos'
        params = {'q':urllib.quote_plus(artist), 'per_page':'100', 'page':'1'}
        json_data = requests.get(url, headers=headers, params=params).json()
    except:
        return False
    try:
        results = json_data['results']
        for v in results:
            try:
                name = v['artists'][0]['name']
                if name.encode('utf-8').lower() == artist.lower():
                    _id = str(v['id'])
                    title = str(v['song_title'])
                    image = urllib.quote(v['image']['o'].encode('utf-8'), safe='%/:=&?~#+!$,;\'@()*[]')
                    duration = ''
                    videos.append({'site':site, 'artist':[artist], 'title':title, 'duration':duration, 'id':_id, 'image':image})
            except:
                pass
    except:
        pass
    return videos

def get_video_url(_id):
    video_url = None
    try:
        url = 'http://imvdb.com/api/v1/video/%s' % _id
        params = {'include':'sources'}
        json_data = requests.get(url, headers=headers, params=params).json()
        for q in json_data['sources']:
            if q['source'] == 'vimeo':
                import vimeo
                video_url = vimeo.get_video_url(q['source_data'])
                break
            if q['source'] == 'youtube':
                import youtube
                video_url = youtube.get_video_url(q['source_data'])
                break
    except:
        pass
    return video_url