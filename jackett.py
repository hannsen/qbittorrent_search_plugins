#VERSION: 0.1
#AUTHORS: ukharley
#
#

from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import json

try:
    # python2
    from urllib import urlencode, quote, unquote
except ImportError:
    # python3
    from urllib.parse import urlencode, quote, unquote


class jacket(object):
    """Generic provider for Torznab compatible api."""

    def __init__(self):
        pass

    name = 'Jacket(torznab)'
    url = 'http://127.0.0.1:9117'  # default, change to yours
    api_key = ''  # add your api key
    supported_categories = {'all': '',
                            'movies': '2000',
                            'tv': '5000',
                            'music': '3000',
                            'books': '8000'
                            }

    def search(self, what, cat='all'):
        cat = cat.lower()
        baseURL = "http://127.0.0.1:9117/api/v2.0/indexers/all/results?%s"
        what = unquote(what)
        category = self.supported_categories[cat]
        if category != '':
            params = urlencode({
                'apikey': self.api_key,
                'Query': what,
                'Category[]': category
            })
        else:
            params = urlencode({
                'apikey': self.api_key,
                'Query': what,
            })

        response = retrieve_url(baseURL % params)
        j = json.loads(response)
        for i in j['Results']:
            tbytes = float(i['Size'])
            size = "-1"

            if tbytes > 1024 * 1024 * 1024:
                size = "%.1f GB" % (tbytes / (1024 * 1024 * 1024))

            elif tbytes > 1024 * 1024:
                size = "%.1f MB" % (tbytes / (1024 * 1024))

            elif tbytes > 1024:
                size = "%.1f KB" % (tbytes / 1024)

            else:
                size = "%.1f B" % (tbytes)

            if i['MagnetUri']:
                res = dict(link=i['MagnetUri'],
                           name=i['Title'],
                           size=size,
                           seeds=i['Seeders'],
                           leech=i['Peers'],
                           engine_url=self.url,
                           desc_link=i['Comments'])
            else:
                res = dict(link=i['Link'],
                           name=i['Title'],
                           size=size,
                           seeds=i['Seeders'],
                           leech=i['Peers'],
                           engine_url=self.url,
                           desc_link=i['Comments'])

            prettyPrinter(res)


if __name__ == "__main__":
    s = jacket()
    s.search("harry potter", 'movies')
