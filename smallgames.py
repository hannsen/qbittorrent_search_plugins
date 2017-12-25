# -*- coding: utf-8 -*-
#VERSION: 1.00
#AUTHORS: hoanns
#  small-games.info
#  Not all results return a torrent file.
#  Click description button to see the game page for it.
#  If there is a mediaget button, you can add &direct=1
#  to its link to get the torrent file.

import os
import re
import tempfile
import urllib.request

from helpers import retrieve_url
# qBt
from novaprinter import prettyPrinter


# noinspection PyPep8Naming
class smallgames(object):
    url = "http://small-games.info/"
    name = 'small-games.info'
    result = {
        'seeds': -1,
        'leech': -1,
        'engine_url': url
    }
    supported_categories = {'all': True,
                            'games': True}

    def download_torrent(self, url):
        file, path = tempfile.mkstemp('.torrent')
        file = os.fdopen(file, "wb")

        # Download url
        req = urllib.request.Request(url)

        response = urllib.request.urlopen(req)
        dat = response.read()

        data = dat.decode('utf-8', 'replace')
        if data == 'No link found!' or data == 'some error':
            return None
        else:
            # Write it to a file
            file.write(dat)
            file.close()
            # return file path
            print(path + " " + url)

    def search(self, what, cat='all'):

        query = "http://small-games.info/?go=search&go=search&search_text=" + what
        data = retrieve_url(query)
        match = re.compile('<a title=\"(.*?)\"\shref=\"/.*?i=(\d*).*?Скачать\sигру\s\((.{2,11})\)')
        results = match.findall(data)

        for res in results:
            self.result['name'] = res[0]
            self.result['link'] = self.url + "getTorrent.php?direct=1&gid=" + res[1]
            self.result['desc_link'] = self.url + "?go=game&c=61&i=" + res[1]
            #  it always MB, and the M from the string is a weird russian one
            #  so pretty printer will not recognize it
            self.result['size'] = res[2][:-3] + 'MB'
            prettyPrinter(self.result)


if __name__ == "__main__":
    engine = smallgames()
    engine.search('eco')
