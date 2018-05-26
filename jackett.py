#VERSION: 1.02
#AUTHORS: ukharley
#         hannsen (github.com/hannsen)
#
#         Make sure to change your api key below

user_data = {
    'url': 'http://127.0.0.1:9117',  # default, change to yours if different
    'api_key': 'YOUR_API_KEY_HERE',  # add your api key
}

from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import json

try:
    # python2
    from urllib import urlencode, quote, unquote
except ImportError:
    # python3
    from urllib.parse import urlencode, quote, unquote


class jackett(object):
    """Generic provider for Torznab compatible api."""

    name = 'Jackett(torznab)'
    url = user_data['url']
    api_key = user_data['api_key']
    supported_categories = {
        'all': '',
        'movies': '2000',
        'tv': '5000',
        'music': '3000',
        'books': '8000'
    }

    def search(self, what, cat='all'):
        what = unquote(what)
        cat = cat.lower()
        base_url = self.url + "/api/v2.0/indexers/all/results?%s"
        category = self.supported_categories[cat]

        params = {
            'apikey': self.api_key,
            'Query': what
        }
        if category != '':
            params['Category[]'] = category
        params = urlencode(params)

        response = retrieve_url(base_url % params)
        j = json.loads(response)
        for i in j['Results']:
            res = dict(
                name=i['Title'],
                size='%d B' % i['Size'],
                seeds=i['Seeders'],
                leech=i['Peers'],
                engine_url="http://" + i['Tracker'],
                desc_link=i['Comments'])

            if i['MagnetUri']:
                res['link'] = i['MagnetUri']
            else:
                res['link'] = i['Link']

            prettyPrinter(res)


if __name__ == "__main__":
    s = jackett()
    s.search("harry potter", 'movies')
