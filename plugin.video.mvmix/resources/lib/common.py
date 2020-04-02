import xbmc,xbmcaddon,xbmcgui
import os,re

addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo('id')
datapath = xbmc.translatePath('special://profile/addon_data/%s' % addon_id).encode('utf-8')

def log(msg):
    xbmc.log(str(msg), xbmc.LOGNOTICE)

def sites():
    sites = [
            ('local', addon.getSetting('local')),('vevo', addon.getSetting('vevo')),
            ('imvdb', addon.getSetting('imvdb')),('youtube', addon.getSetting('youtube')),
            ]
    sites = [i[0] for i in sites if i[1] == 'true']
    return sites

def import_site(site):
    if site == 'local':
        from .sources import local
        return local
    if site == 'vevo':
        from .sources import vevo
        return vevo
    if site == 'imvdb':
        from .sources import imvdb
        return imvdb
    if site == 'youtube':
        from .sources import youtube
        return youtube
    
def clean_title(title):
    title = re.sub('(?:\(|\[)\s*\w*\s*official.*?(?:\)|\])|video\s*-\s*dvd|\(video\)|official\s*video|offizielles\s*video|official\s*dvd|official\s*video\s*hd|music\s*video|official\s*music\s*video|download\s*link', '', title, flags=re.I)
    title = re.sub('"|\'|hd|hq|1080p|720p|4k|\d+\s*fps|\s*new\!\s*$|widescreen|(?:\s*|\.).flv|full\s*(?:size|version|ver.)|music\s*clip', '', title, flags=re.I)
    title = re.sub('high quality|  quality\s*$|\s*\+\s*download|\s*\d{4}\s*$', '', title, flags=re.I)
    title = re.sub('\[\s*\]|\(\s*\)|\(\s*$|\[\s*$|\+\s*$', '', title, flags=re.I)
    title = re.sub('\s{2}', ' ', title, flags=re.I)
    return title.strip()
    
def enter_artist():
    artist = None
    dialog = xbmcgui.Dialog()
    artist = dialog.input('Enter Artist', type=xbmcgui.INPUT_ALPHANUM)
    return artist

def get_start_artist():
    start_artist = None
    import resume
    resume_point = resume.get_resume_point()
    try:
        start_artist = resume_point['start_artist'].encode('utf-8')
    except:
        pass
    return start_artist

def artist_list_file():
    return os.path.join(datapath,'artist_list.json')

def artist_list(mode=False,value_1=False,value_2=False):
    import artist_list
    if mode == 'add':
        artist_list.add_to_artist_list(artist_list_file(),value_1,value_2)
    elif mode == 'delete':
        artist_list.remove_from_artist_list(artist_list_file(),value_1)
    else:
        return artist_list.get_artist_list(artist_list_file())
    
def tag_list_file():
    return os.path.join(datapath,'tag_list.json')
    
def tag_list(mode=False,value=False):
    import tag_list
    if mode == 'add':
        tag_list.add_to_tag_list(tag_list_file(),value)
    elif mode == 'delete':
        tag_list.remove_from_tag_list(tag_list_file(),value)
    else:
        return tag_list.get_tag_list(tag_list_file())
        
def get_tag(name):
    tag = None
    if name == 'Play Genre':
        dialog = xbmcgui.Dialog()
        tag = dialog.input('Enter Genre', type=xbmcgui.INPUT_ALPHANUM)
        if tag:
            tag_list('add',tag)
    else:
        tag = name
    return tag

def ignore_list_file():
    return os.path.join(datapath,'ignore_list.json')

def ignore_list(mode=False,value=False):
    import ignore_list
    if mode == 'add':
        ignore_list.add_to_ignore_list(ignore_list_file(),value)
    elif mode == 'delete':
        ignore_list.remove_from_ignore_list(ignore_list_file(),value)
    else:
        return ignore_list.get_ignore_list(ignore_list_file())

def cache_file():
    return os.path.join(datapath,'cache_%s.json')
    
def resume_file():
    return os.path.join(datapath,'resume.json')
    
def artists_source():
    return addon.getSetting('artists_source')

def artists_path():
    return addon.getSetting('artists_path').encode('utf-8')
    
def get_local_artists():
    import local_artists
    return local_artists.get_local_artists(artists_source(),artists_path())
    
def video_source():
    return addon.getSetting('video_source')
    
def video_path():
    return addon.getSetting('video_path').encode('utf-8')
    
def iconimage():
    home = addon.getAddonInfo('path').decode('utf-8')
    return xbmc.translatePath(os.path.join(home, 'icon.png'))
    
def limit_tag():
    return addon.getSetting('limit_tag')
    
def process():
    return addon.getSetting('process')
    
def process_false():
    addon.setSetting('process', 'False')
    
def process_true():
    addon.setSetting('process', 'True')
    
def limit_result():
    return addon.getSetting('limit_result')
    
def limit_artists(n=False):
    if n:
        addon.setSetting('limit_artists', str(n))
    else:
        return addon.getSetting('limit_artists')

def utf_enc(string):
    try:
        string = string.encode('utf-8')
    except:
        pass
    return string