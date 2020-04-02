# -*- coding: utf-8 -*-

import re,threading,time

import cache
import common
sites = common.sites()
from filter_list import *

def get_videos(artist):
    start_time = time.time()
    videos = []
    result = []
    threads = []
    for site in sites:
        threads.append(threading.Thread(target=videos_thread, args=(site,artist,result)))
    [i.start() for i in threads]
    [i.join() for i in threads]
    for r in result:
        if r:
            for v in r:
                videos.append(v)
    videos = filter_videos(videos)
    videos = sort_videos(videos)
    videos = remove_duplicates(videos)
    complete_time = time.time() - start_time
    common.log('[mvmixPlayer] mode: %s - time: %s' % ('get_videos',str(complete_time)))
    return videos
            
def videos_thread(site,artist,result):
    start_time = time.time()
    video_list = []
    video_list = cache.get_value(site,artist)
    #video_list = None
    if video_list == None:
        video_list = common.import_site(site).get_videos(artist)
        if not video_list == False:
            cache.save_value(site,artist,video_list)
    result.append(video_list)
    complete_time = time.time() - start_time
    common.log('[mvmixPlayer] site: %s - time: %s' % (site,str(complete_time)))
    return result
    
def remove_duplicates(videos):
    all_ids = [ clean(i['title'].lower()) for i in videos ]
    videos = [ videos[ all_ids.index(id) ] for id in set(all_ids) ]
    return videos
    
def clean(title):
    try: title = title.encode('utf-8')
    except: pass
    try: title = title.split('|')[0]
    except: pass
    title = re.sub(' and | und |(?:^|\s)der |(?:^|\s)die |(?:^|\s)das |(?:^|\s)the ','', title)
    title = re.sub('[(]feat.*?$|[(]ft.*?$|( ft(.| ).*?$)|[(]with .*?[)]| feat. .*?$','', title)
    title = re.sub('extended version|extended video', 'extended', title)
    title = re.sub('\(lyric video\)|\(official lyric video\)|\(lyric version\)|\(lyrics\)', 'lyrics', title)
    title = re.sub('(\’|\´|\`|\\xe2\\x80\\x98)', '', title)
    title = re.sub('\s|\n|([[])|([]])|\s(vs|v[.])\s|(:|;|-|\+|\~|\*|"|\'|,|\.|\?|\!|\=|\&|/)|([(])|([)])', '', title)
    return title
    
def sort_videos(videos):
    sorted_video_list = []
    for site in sites:
        for video in videos:
            video['title'] = common.clean_title(video['title'])
            video_site = video['site']
            if video_site == site:
                sorted_video_list.append(video)  
    return sorted_video_list

def filter_videos(videos):
    for f in filter_list:
        videos = [x for x in videos if not re.findall((f), common.utf_enc(x['title']), re.IGNORECASE)]
    videos = [x for x in videos if not re.findall(common.utf_enc(x['artist'][0]), common.utf_enc(x['title']), re.IGNORECASE)]
    ignore_list = common.ignore_list()
    for i in ignore_list:
        videos = [x for x in videos if not (str(i['id']) == str(x['id']) and i['site'] == x['site'])]
    return videos