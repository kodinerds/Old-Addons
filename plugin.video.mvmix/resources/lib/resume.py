import xbmcvfs
import json,os

import common

resume_file = common.resume_file()

def get_resume_point():
    json_data = None
    if os.path.isfile(resume_file):
        try:
            f = xbmcvfs.File(resume_file, 'r')
            json_data = json.load(f)
            f.close()
        except:
            pass
    return json_data

def save_resume_point(resume_point):
    try:
        f = xbmcvfs.File(resume_file, 'w')
        json.dump(resume_point, f)
        f.close()
    except:
        pass