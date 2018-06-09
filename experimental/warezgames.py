# VERSION: 0.1
# AUTHORS: hoanns


import re
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
        igg_match = re.compile("<a\shref=\"(.*?)\"\s.*?rel=\"bookmark\".*?>(.*?)</a>")

        csrin_query = "https://cs.rin.ru/forum/search.php?keywords=" + what + "&terms=all&author=&sc=1&sf=titleonly&sk=t&sd=d&sr=topics&st=0&ch=300&t=0"
        csrin_data = retrieve_url(csrin_query)
        csrin_match = re.compile("<a\shref=\"(.*?)\"\sclass=\"topictitle\".*>(.*?)</a>")

        cs_results = re.findall(csrin_match, csrin_data)
        igg_results = re.findall(igg_match, igg_data)

        for i in igg_results:
            self.printName(i[1] + " [IGG]", i[0])
        for i in cs_results:
            self.printName(i[1] + " [cs_rin]", "https://cs.rin.ru/forum" + i[0][1:])

    def printName(self, name, link):
        prettyPrinter({
            'name': name,
            'size': -1,
            'link': link,
            'desc_link': link,
            'seeds': -1,
            'leech': -1,
            'engine_url': self.url
        })


if __name__ == "__main__":
    engine = warezgames()
    engine.search('isaac')
