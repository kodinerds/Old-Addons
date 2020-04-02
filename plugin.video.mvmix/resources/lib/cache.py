import xbmcvfs
import json,os,time

import common

file = common.cache_file()

def delete_cache(object):
    if os.path.isfile(file % object):
        st = xbmcvfs.Stat(file % object)
        current = round(time.time())
        access = st.st_atime()
        at = (current - access) / 3600
        at = str(at).split('.')[0]
        size = st.st_size()
        s = int(size) / 1024
        t = 24*5
        if 'lastfm' in object:
            t = 24*30
        if int(at) > t or s > 1024:
            xbmcvfs.delete(file % object)

def load_json(object,lastfm):
    json_data = None
    if lastfm == 'tag': object = 'lastfm_tag'
    elif lastfm: object = 'lastfm2'
    delete_cache(object)
    if os.path.isfile(file % object):
        try:
            f = xbmcvfs.File(file % object, 'r')
            json_data = json.load(f)
            f.close()
        except:
            pass
    return json_data

def save_value(object,string,value,lastfm=False):
    if object == 'local':
        return
    json_data = load_json(object,lastfm)
    if json_data:
        entry = None
        try: entry = json_data[object]
        except: pass
        if entry:
            json_data[object][string] = value
        else:
            json_data[object] = {string: value}
    else:
        json_data = {object: {string: value}}
    if lastfm == 'tag': object = 'lastfm_tag'
    elif lastfm: object = 'lastfm2'
    try:
        f = xbmcvfs.File(file % object, 'w')
        json.dump(json_data, f)
        f.close()
    except:
        pass

def get_value(object,string,lastfm=False):
    value = None
    if object == 'local':
        return
    json_data = load_json(object,lastfm)
    try: object = object.decode('utf-8')
    except: pass
    try: string = string.decode('utf-8')
    except: pass
    if json_data:
        try:
            value = json_data[object][string]
        except:
            pass
    return value