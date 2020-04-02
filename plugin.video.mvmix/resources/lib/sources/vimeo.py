# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests

site = 'vimeo'
headers={'X-Requested-With': 'XMLHttpRequest'}

def get_video_url(_id):
    video_url = None
    height = 0
    try:
        url = 'https://player.vimeo.com/video/%s/config' % str(_id)
        json_data = requests.get(url, headers=headers).json()
        for q in json_data['request']['files']['progressive']:
            if height < q['height']:
                height = q['height']
                video_url = q['url']
                if height == 720:
                    break
    except:
        pass
    return video_url