# -*- coding: utf-8 -*-

import xbmc,os
import json
import xbmcvfs

datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.laola1tv/').decode('utf-8')
if not xbmcvfs.exists(datapath):
    xbmcvfs.mkdir(datapath)
file = os.path.join(datapath,'cache.json')

def get_cache_data():
    data = None
    if os.path.isfile(file):
        f = xbmcvfs.File(file, 'r')
        data = json.load(f)
        f.close()
    return data

def cache_data(data):
    try:
        f = xbmcvfs.File(file, 'w')
        json.dump(data, f)
        f.close()
    except:
        pass