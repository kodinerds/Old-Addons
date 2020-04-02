# coding: utf-8
import urllib2
import json
import os.path
import xbmcplugin
import xbmcgui

URI = sys.argv[0]
ADDON_HANDLE = int(sys.argv[1])
MAIN_API_URL = 'https://backend.sportdeutschland.tv/api/'
MAX_PER_PAGE = 200
PATH = os.path.dirname(os.path.realpath(__file__))
ICON = os.path.join(PATH, 'icon.png')
FOLDER = os.path.join(PATH, 'resources', 'media', 'folder.png')
FOLDER_LIVE = os.path.join(PATH, 'resources', 'media', 'folder_live.png')

def get_json_data(url, version = 2): # version in {2,3}
    # new api calls need v3 for now v2 is enough
    # v3 harder to parse and higher runtime
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    req.add_header('Accept', 'application/vnd.vidibus.v%i.html+json' % version)
    return urllib2.urlopen(req).read()

def add_folder(title, mode, arg='', thumb=FOLDER):
    link = '%s?mode=%s' % (URI, mode)
    if arg: link += '&arg=' + arg
    item = xbmcgui.ListItem(title, iconImage = ICON, thumbnailImage = thumb)
    return xbmcplugin.addDirectoryItem(handle = ADDON_HANDLE, url = link, listitem = item, isFolder = True)

def latest(arg, page_number = 1):
    url = '%sassets?access_token=true&page=%i&per_page=%i' % (MAIN_API_URL, page_number, MAX_PER_PAGE)
    list_videos(url)

def search(query = '', page_number = 1):
    import urllib
    if query:
        query = urllib.quote_plus(query)
    else:
        from xbmc import Keyboard
        keyboard = Keyboard('', 'Nach Video suchen')
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = urllib.quote_plus(keyboard.getText())
        else: return
    url = '%s%s%s' % (MAIN_API_URL, 'search?access_token=true&page=%i&per_page=%i&q=' % (page_number, MAX_PER_PAGE), query)
    list_videos(url)

def sports(arg):
    url = MAIN_API_URL + 'sections?per_page=9999'
    try:
        json_data = get_json_data(url)
        data = json.loads(json_data)
        data = sorted(data['items'], key = lambda k: k.get('title', '').lower())
    except: return
    for item in data:
        try: add_folder(item['title'].title().replace(' Wm ', ' WM ', 1).replace(' Em ', ' EM ', 1), 'videos', item['uuid'])
        except: continue

def videos(uuid, page_number = 1):
    url = '%ssections/%s/assets?access_token=true&page=%i&per_page=%i' % (MAIN_API_URL, uuid, page_number, MAX_PER_PAGE)
    list_videos(url)

def list_videos(json_url):
    try:
        json_data = get_json_data(json_url)
        data = json.loads(json_data)
        data = data['items']
    except: return
    for item in data:
        if item.get('video'):
            try:
                try:
                    date = '%s.%s.%s - ' % (item['date'][8:10], item['date'][5:7], item['date'][0:4])
                except:
                    date = ''
                title = item.get('title', '').replace('\t', ' ')
                if title[0] == ' ':
                    title = title[1:]
                title = date + title
                thumb = item.get('image', '')
                if thumb.endswith('_620x350.jpg'):
                    thumb = thumb[:-12] + '_400x225.jpg'
                stream_url = item['video'].replace('.smil?', '.m3u8?', 1)
                desc = item.get('teaser', '')
                li = xbmcgui.ListItem(title, iconImage=ICON, thumbnailImage=thumb)
                li.setInfo(type='Video', infoLabels={'Title': title, 'Plot': desc})
                li.addStreamInfo('video', {'duration': item.get('duration', 0)})
                xbmcplugin.addDirectoryItem(handle = ADDON_HANDLE, url = stream_url, listitem = li)
            except: continue

def live(arg):
    url = MAIN_API_URL + 'assets/next_live?access_token=true'
    try:
        json_data = get_json_data(url)
        data = json.loads(json_data)
        data = sorted(data['items'], key = lambda k: k.get('live_at', k.get('date', '')))
    except: return
    import time, calendar
    for item in data:
        try:
            title = item.get('title', '').replace('\t', ' ')
            if title[0] == ' ':
                title = title[1:]
            if item.get('video'):
                title = '[B][COLOR ffee334e]LIVE[/COLOR] %s[/B]' % title
                stream_url = item['video'].replace('.smil?', '.m3u8?', 1)
                playable = 'true'
            else:
                try:
                    struct_time = time.strptime(item.get('live_at', item.get('date', '')),'%Y-%m-%dT%H:%M:%SZ')
                    date = time.strftime('%a, %d.%m.%Y, %H:%M', time.localtime(calendar.timegm(struct_time))) + ' - '
                except:
                    date = ''
                title = date + title
                stream_url = ''
                playable = 'false'
            thumb = item.get('image', '')
            if thumb.endswith('_620x350.jpg'):
                thumb = thumb[:-12] + '_400x225.jpg'
            desc = item.get('teaser', '')
            li = xbmcgui.ListItem(title, iconImage=ICON, thumbnailImage=thumb)
            li.setInfo(type='Video', infoLabels={'Title': title, 'Plot': desc})
            li.setProperty('IsPlayable', playable)
            xbmcplugin.addDirectoryItem(handle = ADDON_HANDLE, url = stream_url, listitem = li)
        except: continue

def index(arg):
    url = MAIN_API_URL + 'live_events?access_token=true&page=1&per_page=20' # if more than 20 livestreams all streams are listed though
    count = 0
    try:
        json_data = get_json_data(url)
        data = json.loads(json_data)
        data = data['items']
        for item in data:
            if item.get('now'):
                count += 1
    except: pass
    title = 'Live (%i)' % count
    if count:
        add_folder('[B][COLOR ffee334e]%s[/COLOR][/B]' % title, 'live', thumb=FOLDER_LIVE)
    else:
        add_folder(title, 'live')
    add_folder('Suche', 'search')
    add_folder('Neueste Videos', 'latest')
    add_folder('Alle Sportarten', 'sports')

params = dict(part.split('=') for part in sys.argv[2][1:].split('&') if len(part.split('=')) == 2)
mode = params.get('mode', 'index')
arg = params.get('arg', '')
exec '%s(arg)' % mode
xbmcplugin.endOfDirectory(ADDON_HANDLE)
