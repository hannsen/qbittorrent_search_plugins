#VERSION: 1.1
#AUTHORS: hoanns
# snowfl.com
# only first page atm

import base64
import json
import random
import re
import string
import time
# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url


# noinspection PyPep8Naming
class snowfl(object):
    url = "https://snowfl.com"
    name = "snowfl"
    var_match = re.compile('"/"\+(.*?)\+"/search/"')

    def download_torrent(self, url):
        urls = url.split('~')
        urls[0] = base64.b64encode((urls[0].encode())).decode()
        query = self.url + '/' + urls[2] + '/link/' + urls[1] + '/' + urls[0] + '?_=' + str(int(time.time() * 1000))
        data = json.loads(retrieve_url(query))
        print(data['url'] + ' ' + url)

    def randStr(self, N):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))

    def search(self, what, cat='all'):
        script = retrieve_url(self.url + '/main.min.js')
        var_name =re.findall(self.var_match, script)[0]
        bak_match = re.compile(var_name + '="(.*?)"')
        bak = re.findall(bak_match, script)[0]
        query = self.url + '/' + bak + "/search/" + what + "/" + self.randStr(8) + "/0/SEED/NONE/1?_=" + str(int(time.time() * 1000))
        results = json.loads(retrieve_url(query))

        for result in results:
            temp_result = {
                'name': result['title'],
                'size': result['size'],
                'desc_link': result['pageLink'],
                'seeds': result['seed'],
                'leech': result['leech'],
                'engine_url': self.url
            }
            try:
                temp_result['link'] = result['magnetLink']
            except KeyError:
                temp_result['link'] = result['pageLink'] + '~' + result['source'] + '~' + bak
            prettyPrinter(temp_result)

        return


if __name__ == "__main__":
    engine = snowfl()
    engine.search('fire')
