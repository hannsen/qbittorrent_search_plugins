# VERSION: 1.2
# AUTHORS: hoanns
# magnetdl.com
# only first page atm

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
    bak_match = re.compile('bak64="(.*?)"')

    def randStr(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    def search(self, what, cat='all'):
        script = retrieve_url(self.url + '/main.min.js')
        bak = re.findall(self.bak_match, script)[0]
        print(bak)
        query = self.url + '/' + bak + "/search/" + what + "/" + self.randStr() + "/0/SEED/NONE/1?_=" + str(int(time.time() * 1000))
        print(query)
        results = json.loads(retrieve_url(query))
        print(results[100])

        # for result in results:
        #     temp_result = {
        #         'name': result[2],
        #         'size': result[3],
        #         'link': result[0],
        #         'desc_link': self.url[:-1] + result[1],
        #         'seeds': result[4],
        #         'leech': result[5],
        #         'engine_url': self.url
        #     }
        #     prettyPrinter(temp_result)

        return


if __name__ == "__main__":
    engine = snowfl()
    engine.search('fire')
