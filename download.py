import argparse
import shelve
import time

import requests


def download(subreddit, t):
    url = 'https://www.reddit.com/r/{}/top.json'.format(subreddit)
    params = {'t': t, 'limit': 100, 'show': 'all'}
    with requests.session() as sess, shelve.open('{}.shelf'.format(subreddit)) as shelf:
        sess.headers['User-Agent'] = 'rd-downloader/0.1'
        while True:
            print(url, params)
            resp = sess.get(url, params=params)
            if resp.status_code == 429:  # Throttled :(
                print('429', resp.content)
                time.sleep(5)
                continue
            resp.raise_for_status()
            data = resp.json()
            new_params = process_listing(shelf, data)
            params.update(new_params)
            if not params['after']:
                return


def process_listing(storage, data):
    data = data['data']
    for child in data.get('children', ()):
        child = child['data']
        if child['id'] not in storage:
            print(child['id'])
        storage[child['id']] = child
    return {'after': data['after']}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('subreddit')
    ap.add_argument('-t', default='all')
    args = ap.parse_args()
    download(args.subreddit, args.t)
