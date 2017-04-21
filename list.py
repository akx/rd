import argparse
import json
import re
import shelve
from operator import itemgetter

YOUTUBE_RES = [
    re.compile('https://www.youtube.com/watch\?v=([^&]+)'),
    re.compile('https://youtu.be/([^&]+)'),
]


def list_entries(subreddit):
    with shelve.open('{}.shelf'.format(subreddit)) as shelf:
        items = [process_item(item) for item in shelf.values()]
        items = [item for item in items if item]
        items.sort(key=itemgetter('score'), reverse=True)
        for item in items:
            print(json.dumps(item, sort_keys=True))



def process_item(item):
    url = item['url']
    video_id = None
    for r in YOUTUBE_RES:
        m = r.match(url)
        if m:
            video_id = m.group(1)
    if not video_id:
        print(item)
        return None
    score = item['ups'] - item['downs']
    return {
        'score': score,
        'url': 'https://youtu.be/%s' % video_id,
        'title': item['title'],
        'nsfw': item['over_18'],
    }


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('subreddit')
    args = ap.parse_args()
    list_entries(args.subreddit)
