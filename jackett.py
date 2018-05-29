#VERSION: 1.05
#AUTHORS: ukharley
#         hannsen (github.com/hannsen)
#
#         (Optional) Change your api key below

user_data = {
    'url': 'http://127.0.0.1:9117',  # default, change to yours if different
    'api_key': 'YOUR_API_KEY_HERE',  # add your api key
}

import json
from novaprinter import prettyPrinter

try:
    # python2
    from urllib import urlencode, quote, unquote
    import urllib2 as urllib_request
    from urllib2 import HTTPError as HTTP_Error
except ImportError:
    # python3
    from urllib.parse import urlencode, quote, unquote
    from urllib import request as urllib_request
    from urllib.error import HTTPError as HTTP_Error


# noinspection PyPep8Naming
class jackett(object):
    """Generic provider for Torznab compatible api."""

    what = ""
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
        self.what = what
        cat = cat.lower()
        base_url = self.url + "/api/v2.0/indexers/all/results?%s"
        category = self.supported_categories[cat]

        # user did not change api_key, trying to get from config
        if self.api_key == "YOUR_API_KEY_HERE":
            response = self.get_response(self.url + "/api/v2.0/server/config")
            self.api_key = json.loads(response)['api_key']

        params = {
            'apikey': self.api_key,
            'Query': what
        }
        if category != '':
            params['Category[]'] = category
        params = urlencode(params)

        response = self.get_response(base_url % params)
        j = json.loads(response)
        for i in j['Results']:
            res = dict(
                name='%s [%s]' % (i['Title'], i['Tracker']),
                size='%d B' % i['Size'],
                seeds=i['Seeders'],
                leech=i['Peers'],
                engine_url=self.url,
                desc_link=i['Comments'])

            if i['MagnetUri']:
                res['link'] = i['MagnetUri']
            else:
                res['link'] = i['Link']

            prettyPrinter(res)

    def get_response(self, query):
        try:
            response = urllib_request.urlopen(query).read()
        except HTTP_Error:
            self.handle_error()
            quit()
        # noinspection PyUnboundLocalVariable
        return response

    def handle_error(self):
        error_msg = "Failure to connect to Jackett server! Please check API Key and URL / "
        prettyPrinter({
            'seeds': -1,
            'size': -1,
            'leech': -1,
            'engine_url': self.url,
            'link': self.url,
            'desc_link': self.url,
            'name': error_msg + self.what
        })


if __name__ == "__main__":
    s = jackett()
    s.search("harry potter", 'movies')
