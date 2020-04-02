import xbmc,xbmcvfs
import json,re

def get_local_artists(artists_source,artists_path):
    artists = []
    if artists_source == 'Music Library':
        artists = get_artists_from_library()
    else:
        if artists_path:
            artists = get_artists_from_folder(artists_path)
    return artists
    
def get_artists_from_library():
    artists = []
    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": { "properties": [ "thumbnail" ] }, "sort": { "order": "ascending", "method": "artist", "ignorearticle": false }, "id": 1}')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    json_response = json.loads(json_query)
    if json_response.has_key('result') and json_response['result'] != None and json_response['result'].has_key('artists'):
        artists = json_response["result"]["artists"]
    return artists
    
def get_artists_from_folder(artists_path):
    artists = []
    dirs, files = xbmcvfs.listdir(artists_path)
    for d in dirs:
        try:
            dir = re.sub('\_', ' ', d)
            match = dir.split(' - ')
            if len(match) == 1:
                match = dir.split('-')
            if len(match) > 1:
                artist = match[0].strip()
                thumbnail = ''
                if artist and artist.lower() != 'va':
                    artists.append({'artist': artist, 'thumbnail': thumbnail})
        except:
            pass
    artists = remove_duplicates(artists)
    artists.sort()
    return artists

def remove_duplicates(artists):
    all_ids = [ i['artist'].lower() for i in artists ]
    artists = [ artists[ all_ids.index(id) ] for id in set(all_ids) ]
    return artists