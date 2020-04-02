# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
from resources.lib import common
import urlparse, re, urllib
from .signature.cipher import Cipher

site = 'youtube'

def get_videos(artist):
    videos = []
    url = 'https://www.googleapis.com/youtube/v3/search'
    headers = {'Host': 'www.googleapis.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.36 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate'}
    params = {'part':'snippet','type':'video','maxResults':'50',
                'q':'%s video' % artist,'key':'AIzaSyCky6iU_p2VjvpXwTSOpPVLsGFIdR51lQE',
                }
    try:
        json_data = requests.get(url, params=params, headers=headers).json()
    except:
        return False
    try:
        items = json_data['items']
        videos = add_videos(videos, items, artist)
        if len(videos) > 1:
            json_data,items = get_more_items(json_data, url, params, headers)
            videos = add_videos(videos, items, artist)
        if len(videos) > 3:
            json_data,items = get_more_items(json_data, url, params, headers)
            videos = add_videos(videos, items, artist)
    except:
        pass
    return videos

def add_videos(videos, items, artist):
    for item in items:
        try:
            _id = item['id']['videoId']
            snippet = item['snippet']
            t = snippet['title'].encode('utf-8')
            spl = split_title(t)
            name = spl[0].strip().decode('utf-8')
            title = spl[1].strip().decode('utf-8')
            if len(spl) > 2:
                title = '%s - %s' % (title, spl[2].strip().decode('utf-8'))
            description = snippet['description'].lower().encode('utf-8')
            channel = snippet['channelTitle'].lower().replace(' ','').encode('utf-8')
            name = check_name(artist,name)
            name_2 = check_name(artist,title)
            if artist.lower() == name.encode('utf-8').lower() or artist.lower() == name_2.encode('utf-8').lower():
                if artist.lower() == name_2.encode('utf-8').lower():
                    title = name
                if status(channel,artist,title,description) == True:
                    image = snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
                    duration = ''
                    title = clean_title(title)
                    videos.append({'site':site, 'artist':[name], 'title':title, 'duration':duration, 'id':_id, 'image':image})
        except:
            pass
    return videos
    
def get_more_items(json_data, url, params, headers):
    items = []
    json_data2 = {}
    try:
        npt = json_data['nextPageToken']
        if npt:
            params['pageToken'] = npt
            json_data2 = requests.get(url, params=params, headers=headers).json()
            items = json_data2['items']
    except:
        pass
    return json_data2, items
    
def get_video_url(_id):
    video_url = None
    headers = {'Host': 'www.youtube.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.36 Safari/537.36',
                'Referer': 'https://www.youtube.com',}
    params = {'v': _id}
    url = 'https://youtube.com/watch'
    html = ''
    cookie = ''
    try:
        html = requests.get(url, params=params, headers=headers).text
    except:
        pass
    pos = html.find('<script>var ytplayer')
    if pos >= 0:
        html2 = html[pos:]
        pos = html2.find('</script>')
        if pos:
            html = html2[:pos]
    re_match_js = re.search(r'\"js\"[^:]*:[^"]*\"(?P<js>.+?)\"', html)
    js = ''
    cipher = None
    if re_match_js:
        js = re_match_js.group('js').replace('\\', '').strip('//')
        if not js.startswith('http'):
            js = 'http://www.youtube.com/%s' % js
        cipher = Cipher(java_script_url=js)
        
    re_match = re.search(r'\"url_encoded_fmt_stream_map\"\s*:\s*\"(?P<url_encoded_fmt_stream_map>[^"]*)\"', html)
    if re_match:
        url_encoded_fmt_stream_map = re_match.group('url_encoded_fmt_stream_map')
        url_encoded_fmt_stream_map = url_encoded_fmt_stream_map.split(',')
        for value in url_encoded_fmt_stream_map:
            value = value.replace('\\u0026', '&')
            attr = dict(urlparse.parse_qsl(value))
            url = attr.get('url', None)
            if url:
                url = urllib.unquote(attr['url'])
                if 'signature' in url:
                    video_url = url
                    break
                signature = ''
                if attr.get('s', ''):
                    signature = cipher.get_signature(attr['s'])
                elif attr.get('sig', ''):
                    signature = attr.get('sig', '')
                if signature:
                    url += '&signature=%s' % signature
                    video_url = url
                    break
    return video_url
    
def status(channel,artist,title,description):
    title = title.lower()
    artist = artist.lower().replace(' ','')
    channel = channel.lower()
    a = ['lyric', 'no official', 'not official', 'unofficial', 'un-official', 'non-official', 'vevo']
    if any(x in title for x in a):
        if 'official lyric video' in title:
            return True
        else:
            return False
    b = [
        'parody', 'parodie', 'fan made', 'fan-made', 'fanmade', 'fan mv', 'fan edit', 'vocal cover',
        'dance cover', 'dance practice',
        'custom video', 'music video cover', 'music video montage', 'video preview',
        'guitar cover', 'drum through', 'guitar walk', 'drum walk',
        'guitar demo', '(drums)', 'drum cam', 'drumcam', '(guitar)',
        'our cover of', 'in this episode of', 'official comment', 'short video about',
        'short ver', 'full set', 'full album stream', 'hour version',
        '"reaction"', 'reaction!', 'video reaction', 'reaction video',
        'v reaction', '[reaction]', '| reaction', '(review)', '(preview)',
        'splash news', 'not an official', 'music video awards'
    ]
    if any(x in title for x in b) or any(x in description for x in b):
        return False
    c = [' animated ', 'i don\'t own', 'i do not own', 'preview of',
         'no official', 'not official', 'unofficial', 'un-official', 'non-official']
    if any(x in description for x in c):
        return False
    d = [u"\u2665", u"\u2661", 'cover by', 'hq remake', 'remake by']
    if any(x in title for x in d):
        return False
    j = ['tmz']
    if any(channel == x for x in j):
        return False
    e = ['official video', 'taken from', 'itunes.apple.com', 'itunes.com', 'smarturl.it', 'j.mp']
    if any(x in description for x in e):
        return True
    f = ['official video', 'official music video', 'offizielles video', 'us version']
    if any(x in title for x in f) and description:
        return True
    g = ['records', 'official']
    if any(x in channel for x in g):
        return True
    h = ['vevo']
    if any(channel.endswith(x) for x in h):
        return True
    return False

def split_title(t):
    if (t.startswith('[') and '「' in t):
        t = re.sub('\[\w{2}\]', '', t) + ' official music video'
    elif (t.startswith('【') and ' - ' in t):
        t = re.sub('\【\w{2}\】', '', t) + ' official music video'
    t = t.replace('「',' - ').replace('」','')
    t = t.replace('–', '-')
    if not '-' in t and '"' in t:
        t = re.sub(' "', ' - ', t)
    if not '-' in t and ' / ' in t:
        t = re.sub(' / ', ' - ', t)
    if re.search(' - ', t):
        return t.split(' - ')
    elif re.search('- ', t):
        return t.split('- ')
    elif re.search(' -', t):
        return t.split(' -')
    else:
        return t.split('-')

def clean_title(title):
    try: title = title.split('|')[0]
    except: pass
    if not re.findall('\(.+?-.+?\)', title):
        try: title = title.split(' - ')[0]
        except: pass
    return title
    
def check_name(artist,name):
    if not artist.lower() == name.encode('utf-8').lower():
        split_tags = [',','&','(feat','feat','ft']
        for tag in split_tags:
            if tag in name:
                splitted = name.split(tag)
                if len(splitted) > 1:
                    name = splitted[0].strip()
                    break
    return name
