import xbmc,os
import json

def get_tag_list(file):
    json_data = []
    if os.path.exists(file):
        with open(file) as f:
            json_data = json.load(f)
    return json_data

def add_to_tag_list(file,tag):
    entries = get_tag_list(file)
    new_entry = {'tag': tag}
    if entries:
        for entry in entries:
            if entry['tag'].encode('utf-8') == tag:
                return
        entries.insert(0,new_entry)
        save(file,entries)
    else:
        save(file,[new_entry])

def save(file,entry):
    with open(file, 'w') as f:
        json.dump(entry, f)

def remove_from_tag_list(file,tag):
    json_data = get_tag_list(file)
    for i in xrange(len(json_data)):
        if json_data[i]['tag'].encode('utf-8') == tag:
            json_data.pop(i)
            break
    save(file,json_data)