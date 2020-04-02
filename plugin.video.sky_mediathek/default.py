# -*- coding: utf-8 -*-
import urllib
import urllib2
import os.path
import re
import xbmcplugin
import xbmcaddon
import xbmcgui

URI = sys.argv[0]
ADDON_HANDLE = int(sys.argv[1])
path = os.path.dirname(os.path.realpath(__file__))
icon = os.path.join(path, 'icon.png')

base_url = 'http://www.sky.de'
video_player = '3424888239001'

def clean_text(text):
    return text.replace('&#34;', '"').replace('&amp;', '&').replace('&#39;', "'")
    
def get_resized_thumbnail(image_url, width = 400):
    return 'http://images1-prose-opensocial.googleusercontent.com/gadgets/proxy?url=%s&container=prose&gadget=a&rewriteMime=image/*&resize_w=%i&no_expand=1' % (image_url, width)
    
def play_video(stream_url):
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, xbmcgui.ListItem(path=stream_url))
    
def add_video(title, resource, thumb = '', mode = 'play-video', duration_in_seconds = 0, desc = ''):
    link = URI + '?resource=' + urllib.quote_plus(resource) + '&mode=' + mode
    liz = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumb)
    liz.setInfo(type='Video', infoLabels={'Title': title, 'Plot': desc})
    liz.addStreamInfo('video', {'duration': duration_in_seconds})
    liz.setProperty('IsPlayable', 'true')
    return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=link, listitem=liz)
    
def add_category(title, mode, resource, current_page = 1):
    link = URI + '?mode=' + mode + '&current_page=' + str(current_page) + '&resource=' + resource
    liz = xbmcgui.ListItem(title, iconImage=icon)
    return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=link, listitem=liz, isFolder=True)
    
def warning(text, title = 'Sky Mediathek', time = 4500):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (title, text, time, icon))
    
def get_stream_url(page_url):
    import json
    video_id = page_url.split('/')[-1]
    rescue_url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + video_id
    url = 'http://c.brightcove.com/services/viewer/htmlFederated?playerID=%s&%%40videoPlayer=%s' % (video_player, video_id)
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
        'Referer' : page_url,
        'Connection' : 'keep-alive'
    }
    try:
        req = urllib2.Request(url, None, headers)
        data = urllib2.urlopen(req).read()
        regex_json_data = 'var\s*experienceJSON\s*=\s*{(.+?)}\s*;\s*\n'
        json_data = '{%s}' % re.findall(regex_json_data, data)[0]
        videos = json.loads(json_data)['data']['programmedContent']['videoPlayer']['mediaDTO']['renditions']
        stream_url = rescue_url
        addon = xbmcaddon.Addon(id='plugin.video.sky_mediathek')
        PREFERED_HEIGHT = (360, 720)[int(addon.getSetting('maxVideoQuality'))]
        for video in videos:
            stream_url = video['defaultURL']
            if video['frameHeight'] == PREFERED_HEIGHT:
                break
        return stream_url
    except:
        return rescue_url


def list_all_videos(page_number = 1, category_id = ''):
    pagination_url = base_url + '/me03pagination.sr?QUERY_TYPE=PLAYLIST_ID&QUERY_VALUE=%s&ANC_LINK=&show_date=true&show_category=false&FIRST_ELEMENT_NUMBER=-1&page=%i' % (category_id, page_number)
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}
    try:
        req = urllib2.Request(pagination_url, None, headers)
        html = urllib2.urlopen(req).read()
    except: return False
    regex_all_videos = '<div class="videoPlayer__poster">.*?<img src="(.+?)".*?</span>(.*?)</div>.*?class="airingDate__date">(.+?)<.*?href="(.+?)".*?>(.+?)<'
    all_videos = re.findall(regex_all_videos, html, re.DOTALL)
    for video in all_videos:
        if 'videoPlayer__lockedCaption' in video[1]:
            continue
        thumb = video[0].split('.jpg')[0].replace('https:', 'http:', 1) + '.jpg'
        thumb = get_resized_thumbnail(thumb)
        date = video[2].split(', ')[-1].split('. ')[0] + '.'
        try:
            duration_in_seconds = video[2].split('| ')[-1]
            duration_in_seconds = duration_in_seconds[:duration_in_seconds.find(' ')]
            splitted = duration_in_seconds.split(':')
            duration_in_seconds = int(splitted[0]) * 60 + int(splitted[1])
        except: duration_in_seconds = 0
        url = base_url + video[3]
        if not video[3][-8:-1].isdigit(): continue
        title = clean_text(video[4])
        add_video('%s - %s' % (date, title), url, thumb, 'play-video', duration_in_seconds)
    if ('var lastPage = false;' not in html) or len(all_videos) != 4: return -1 # than is last page
    return True # else not last page

def add_videos(page_number = 1, category = ''):
    for page in range((page_number-1)*3 + 1,page_number*3 + 1):
        return_code = list_all_videos(page, category)
        if not return_code: return warning('Keine Netzwerkverbindung?')
        if return_code == -1:
            # last page reached
            xbmcplugin.endOfDirectory(ADDON_HANDLE)
            return True
    add_category(title = '[B]%s (%i)[/B]' % ('Nächste Seite', page_number+1), mode = 'list-videos', resource = category, current_page = page_number+1)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)
    return True

params = dict(part.split('=') for part in sys.argv[2][1:].split('&') if len(part.split('=')) == 2)
mode = urllib.unquote_plus(params.get('mode', ''))

if mode == 'play-video':
    category = urllib.unquote_plus(params.get('resource', ''))
    play_video(get_stream_url(category))
elif mode == 'list-videos':
    category = urllib.unquote_plus(params.get('resource', ''))
    add_videos(int(params.get('current_page', 1)), category)
else:
    categories = (
        ('Neue Videos',             '27610441001'),
        ('1. Bundesliga',           '32548888001'),
        ('2. Bundesliga',           '32548889001'),
        ('DFB Pokal',               '30700836001'),
        ('Premier League',          '33728263001'),
        ('Champions League',        '33569461001'),
        ('Europa League',           '37988504001'),
        ('1. Liga AT',              '29734631001'),
        ('2. Liga AT',              '29713021001'),
        ('Formel 1',                '27583543001'),
        ('Formel E',                '3764627965001'),
        #('Tennis',                 'CONTACT_ME_IF_KNOWN'),
        ('Handball',                '3784218159001'),
        ('Basketball (ABL)',        '1254984328001'),
        ('Golf',                    '27610440001'),
        #('Boxen',                  'CONTACT_ME_IF_KNOWN'),
        ('Wintersport',             '3261159912001'),
        ('Beachvolleyball',         '2359637262001'),
        ('Sport-Dokumentationen',   '3852736962001'),
        ('Sonstige Videos',         '1711753593001'),
        ('Kinotrailer',             '1772804035001'),
        ('DVD Trailer',             '1772804034001'),
        ('Serien-Highlights',       '1574504486001'),
        ('Kinopolis',               '1219349353001'),
        ('Sky Magazin',             '1219349354001'),
        ('Neu auf Sky',             '1772804032001'),
        ('Sky90',                   '44551452001'),
    )
    for category in categories:
        add_category(category[0], 'list-videos', category[1])
    xbmcplugin.endOfDirectory(ADDON_HANDLE)