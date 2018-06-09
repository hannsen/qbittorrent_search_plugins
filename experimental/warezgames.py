# VERSION: 0.1
# AUTHORS: hoanns


import re
import requests
import subprocess

from novaprinter import prettyPrinter
from helpers import retrieve_url


# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
# headers = {'User-Agent': user_agent}


# noinspection PyPep8Naming
class warezgames(object):
    url = "http://www.warezgames.com/"
    name = "WarezGames"

    def search(self, what, cat='all'):
        what = what.lower()

        process = subprocess.Popen(['phantomjs.exe', 'getigg.js', what], stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        igg_data = out.decode('utf-8')

        csrin_query = "https://cs.rin.ru/forum/search.php?keywords=" + what + "&terms=all&author=&sc=1&sf=titleonly&sk=t&sd=d&sr=topics&st=0&ch=300&t=0"
        csrin_data = retrieve_url(csrin_query)

        # results = re.findall(self.result_page_match, data)
        #
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
        #
        # return


if __name__ == "__main__":
    engine = warezgames()
    engine.search('isaac binding')
