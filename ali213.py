#VERSION: 1.1
#AUTHORS: hoanns
# Chinese Gaming Site
# Beware that they sometimes upload uncracked games on here.
#
# I have to do 3 page requests (to chinese servers) per game
# to get to the english release name and torrent.
# So I set the games_to_parse (see below) value to 5.


import re
import threading
import time
# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url


# noinspection PyPep8Naming
class ali213(object):
    url = "http://down.ali213.net/"
    name = "ali213"
    # The ali search is not strict and will give you all kinds of bogus games
    # I am fine with the 5 most relevant games to parse, since I will not use broad search terms
    games_to_parse = 5
    # first size (e.g. 40.7G) then game page (e.g. arksurvivalevolved.html)
    result_page_match = re.compile(
        '<p class="downAddress"><a href="http://down.ali213.net/pcgame/(.*?)" target="_blank">.*?<em>(.{2,7})</em>')

    supported_categories = {'all': True,
                            'games': True,
                            'software': True}

    first_dl_site = "http://www.soft50.com/"
    final_dl_site = "http://btfile.soft5566.com/y/"

    def handle_gamepage(self, size_gamepage):
        data = retrieve_url(self.url + 'pcgame/' + size_gamepage[0])
        down_url_match = re.compile('var downUrl ="/(.*?)"')
        url_key_soft50 = down_url_match.findall(data)
        if url_key_soft50:
            data = ''
            tries = 0
            while data == '' and tries < 20:
                time.sleep(2)
                data = retrieve_url(self.first_dl_site + url_key_soft50[0])
                tries += 1

            down_url_match = re.compile('class="result_js" href="(.*?)" target="_blank">')
            url_soft5566 = down_url_match.findall(data)
            if url_soft5566:
                data = retrieve_url(url_soft5566[0])
                desc_site = url_soft5566[0]
                down_url_match = re.compile('id="btbtn" href="' + self.final_dl_site + '(.*?)" target="_blank"')
                url_torrent = down_url_match.findall(data)
                if url_torrent:
                    result = {
                        'name': url_torrent[0],
                        'size': size_gamepage[1],
                        'link': self.final_dl_site + url_torrent[0],
                        'desc_link': desc_site,
                        'seeds': -1,
                        'leech': -1,
                        'engine_url': self.url
                    }
                    prettyPrinter(result)
        return

    def search(self, what, cat='all'):

        query = "http://down.ali213.net/search?kw=" + what + "&submit="
        data = retrieve_url(query)
        found_games = re.findall(self.result_page_match, data)

        if found_games:
            if self.games_to_parse > len(found_games):
                self.games_to_parse = len(found_games)
            # handling each gamepage in parallel, to not waste time on waiting for requests
            # for 10 games this speeds up from 37s to 6s run time
            threads = []
            for i in range(self.games_to_parse):
                t = threading.Thread(target=self.handle_gamepage, args=(found_games[i],))
                threads.append(t)
                t.start()

            # search method needs to stay alive until all threads are done
            for t in threads:
                t.join()

        return


if __name__ == "__main__":
    engine = ali213()
    engine.search('ark.survival', 'games')
