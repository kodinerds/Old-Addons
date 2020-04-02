# -*- coding: utf-8 -*-

import json

from resources.lib import simple_requests as requests
import common
import cache

api_url = 'http://ws.audioscrobbler.com/2.0/'
api_key = 'b25b959554ed76058ac220b7b2e0a026'

def get_artists(query):
    artists = []
    try:
        params = {'method':'artist.search', 'artist':query, 'api_key':api_key,
                    'format':'json', 'limit':'25'}
        json_data = requests.get(api_url, params=params).json()
        for a in json_data['results']['artistmatches']['artist']:
            artist = a['name']
            image = a['image'][-1]['#text']
            listeners = a['listeners']
            if image:
                artists.append({'artist': artist, 'image': image, 'listeners': listeners})
    except:
        pass
    artists = remove_duplicates(artists)
    artists = sorted(artists, key=lambda k:int(k['listeners']), reverse=True)
    return artists

def get_similar_artists(artist):
    n = '100'
    value = cache.get_value(artist,n,lastfm=True)
    if value == None:
        value = []
        try:
            params = {'method':'artist.getsimilar', 'artist':artist, 'autocorrect':'1',
                        'limit':n, 'api_key':api_key, 'format':'json'}
            json_data = requests.get(api_url, params=params).json()
            for item in json_data['similarartists']['artist']:
                value.append(item['name'])
            cache.save_value(artist,n,value,lastfm=True)
        except:
            pass
    similar_artists = []
    for s in value:
        similar_artists.append(s)
        if len(similar_artists) == int(common.limit_artists()):
            break
    return similar_artists
    
def get_artists_by_tag(tag):
    n = '500'
    value = cache.get_value(tag,n,lastfm='tag')
    if value == None:
        value = []
        try:
            params = {'method':'tag.gettopartists', 'tag':tag, 'api_key':api_key,
                        'format':'json', 'limit':n}
            json_data = requests.get(api_url, params=params).json()
            for a in json_data['topartists']['artist']:
                try:
                    value.append({'artist':a['name']})
                except:
                    pass
            cache.save_value(tag,n,value,lastfm='tag')
        except:
            pass
    artists = []
    for a in value:
        artists.append(a)
        if len(artists) == int(common.limit_tag()):
            break
    return artists

def compare_genres(genre_list,genres):
    if genre_list and genres:
        x = 0
        for a in genres:
            for b in genre_list:
                if a == b:
                    x += 1
                if x == 2:
                    return True
    return False

def get_artist_genre(artist):
    genre_list = cache.get_value(artist,'genre',lastfm='tag')
    if genre_list == None:
        genre_list = []
        try:
            params = {'method':'artist.gettoptags', 'artist':artist, 'api_key':api_key, 'format':'json'}
            json_data = requests.get(api_url, params=params).json()
            for tag in json_data['toptags']['tag']:
                genre_list.append(tag['name'])
                if len(genre_list) == 5:
                    break
            cache.save_value(artist,'genre',genre_list,lastfm='tag')
        except:
            pass
    return genre_list
                
def remove_duplicates(artists):
    all_ids = [ i['artist'] for i in artists ]
    artists = [ artists[ all_ids.index(id) ] for id in set(all_ids) ]
    return artists