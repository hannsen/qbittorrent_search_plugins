#VERSION: 1.01
#AUTHORS: hoanns
# magnetdl.com
# only first page atm

import re
# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url


# noinspection PyPep8Naming
class magnetdl(object):
    url = "http://www.magnetdl.com/"
    name = "MagnetDL"
    games_to_parse = 10
    result_page_match = re.compile(
        '<td\sclass="m"><a\shref="(magnet.*?)"\stitle=".*?class="n"><a\shref="(.*?)"\stitle="(.*?)">.*?<td\sclass="t5">.*?</td><td>.*?</td><td>(.*?)</td><td\sclass="s">(.*?)</td><td\sclass="l">(.*?)</td>')

    def search(self, what, cat='all'):
        query = self.url + what[:1] + '/' + what
        print(query)
        data = retrieve_url(query)
        results = re.findall(self.result_page_match, data)

        for result in results:
            temp_result = {
                'name': result[2],
                'size': result[3],
                'link': result[0],
                'desc_link': self.url[1:] + result[1],
                'seeds': result[4],
                'leech': result[5],
                'engine_url': self.url
            }
            prettyPrinter(temp_result)

        return


if __name__ == "__main__":
    engine = magnetdl()
    engine.search('lol')
