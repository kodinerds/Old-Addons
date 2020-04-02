# -*- coding: utf-8 -*-

from resources.lib.client import Client
from resources.lib import laola
from resources.lib import cache
from resources.lib.common import *

client = Client()

def run():
    if mode == 'root':
        client.user()
        if client.cookie:
            if addon.getSetting('startup') == 'true':
                start_is_helper()
                data = client.menu()
                if data:
                    cache.cache_data(data)
                    addon.setSetting('startup', 'false')
            else:
                data = cache.get_cache_data()
            laola.menu(data)
    elif mode == 'sports':
        laola.sports(cache.get_cache_data(), title)
    elif mode == 'sub_menu':
        laola.sub_menu(client.feeds(params, id))
    elif mode == 'live':
        laola.live(client.live_feed())
    elif mode == 'videos':
        laola.video(client.feeds(params, id))
    elif mode == 'play':
        laola.play(path())
        client.deletesession()
        
def path():
    url = unas_url(client.player(id, params))
    if url:
        return master(client.unas_xml(url))

def unas_url(data):
    if data.get('status', 'error') == 'success':
        return data['data']['stream-access'][0]
    else:
        message = data.get('message', 'error')
        dialog.ok(addon_name, utfenc(message))

def master(data):
    a = re.search('auth="(.*?)"', data)
    b = re.search('url="(http.*?)"', data)
    c = re.search('comment="(.*?)"', data)
    if a and b:
        return '%s?hdnea=%s' % (b.group(1), a.group(1))
    elif c:
        dialog.ok(addon_name, utfenc(c.group(1)))

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', ['root'])[0]
title = args.get('title', [''])[0]
id = args.get('id', [''])[0]
params = args.get('params', [''])[0]
if not args:
    args = version
log('[%s] arguments: %s' % (addon_id, str(args)))

run()