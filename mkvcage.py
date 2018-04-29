#VERSION: 1.1
#AUTHORS: hoanns
# movie and tv show site
# Will only parse the first search result site, sorry
# tv and movie category will not be differentiated

import re
import threading
# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url


# noinspection PyPep8Naming
class mkvcage(object):
    url = "http://www.mkvcage.bid"
    name = "MkvCage"
    games_to_parse = 10
    result_page_match = re.compile('<h2 class="entry-title"><a href="http://(.*?)"')

    supported_categories = {'all': True,
                            'movies': True,
                            'tv': True}

    def handle_page(self, url):
        data = retrieve_url(url)
        size_match = re.compile('<strong>File\sSize:</strong>\s(.*?)(<br|\n)')
        try:
            size = size_match.findall(data)[0][0]
        except IndexError:
            size = -1
        try:
            dl_match = re.compile('<a\sclass="buttn\storrent"\shref="http://www.mkvcage.com/torrents/(.*?)"')
            dl = dl_match.findall(data)[0]
        except IndexError:
            return
        result = {
            'name': dl,
            'size': size,
            'link': "http://www.mkvcage.com/torrents/" + dl,
            'desc_link': url,
            'seeds': -1,
            'leech': -1,
            'engine_url': self.url
        }
        prettyPrinter(result)
        return

    def search(self, what, cat='all'):

        query = "http://www.mkvcage.bid/?s=" + what
        data = retrieve_url(query)
        found_games = re.findall(self.result_page_match, data)

        if found_games:
            if self.games_to_parse > len(found_games):
                self.games_to_parse = len(found_games)
            # handling each page in parallel, to not waste time on waiting for requests
            # for 8 entries this speeds up from 8s to 3s run time
            threads = []
            for i in range(self.games_to_parse):
                # self.handle_page("http://" + found_games[i])
                t = threading.Thread(target=self.handle_page, args=("http://" + found_games[i],))
                threads.append(t)
                t.start()

            # search method needs to stay alive until all threads are done
            for t in threads:
                t.join()

        return


if __name__ == "__main__":
    engine = mkvcage()
    engine.search('fire')
