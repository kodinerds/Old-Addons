import xbmc,os
import json

def get_artist_list(file):
    json_data = []
    if os.path.exists(file):
        with open(file) as f:
            json_data = json.load(f)
    return json_data

def add_to_artist_list(file,artist,image):
    entries = get_artist_list(file)
    new_entry = {'artist': artist, 'image': image}
    if entries:
        for entry in entries:
            if entry['artist'].encode('utf-8') == artist:
                return
        entries.insert(0,new_entry)
        save(file,entries)
    else:
        save(file,[new_entry])

def save(file,entry):
    with open(file, 'w') as f:
        json.dump(entry, f)
        
def remove_from_artist_list(file,artist):
    json_data = get_artist_list(file)
    for i in xrange(len(json_data)):
        if json_data[i]['artist'].encode('utf-8') == artist:
            json_data.pop(i)
            break
    save(file,json_data)