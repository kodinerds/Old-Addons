import xbmc,os
import json

def get_ignore_list(file):
    json_data = []
    if os.path.exists(file):
        with open(file) as f:
            json_data = json.load(f)
    return json_data

def add_to_ignore_list(file,data):
    entries = get_ignore_list(file)
    new_entry = data
    if entries:
        for entry in entries:
            if entry['id'] == data['id'] and entry['site'] == data['site']:
                return
        entries.insert(0,new_entry)
        save(file,entries)
    else:
        save(file,[new_entry])

def save(file,entry):
    with open(file, 'w') as f:
        json.dump(entry, f)
        
def remove_from_ignore_list(file,data):
    json_data = get_ignore_list(file)
    for i in xrange(len(json_data)):
        if json_data[i]['id'] == data['id'] and json_data[i]['site'] == data['site']:
            json_data.pop(i)
            break
    save(file,json_data)