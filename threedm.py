#VERSION: 1.00
#AUTHORS: hoanns


# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from html.parser import HTMLParser
from re import compile as re_compile

#qBt
from novaprinter import prettyPrinter
from helpers import download_file, retrieve_url

class threedm(object):
    """ Search engine class """
    url = "http://bt.3dmgame.com/"
    name = "3dmgame"

    class Parsar(HTMLParser):

        def __init__(self, url):
            HTMLParser.__init__(self)
            self.url = url
            self.current_item = None
            self.save_data = None
            self.handle_that_data = False
            self.name_repl = re_compile("^\s*")

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                params = dict(attrs)
                try:
                    link = params["href"]
                    if link.startswith("down.php?"):
                        self.current_item = dict()
                        self.current_item["desc_link"] = self.url + link.replace("down.php", "show.php")
                        self.current_item["engine_url"] = self.url
                        self.current_item["link"] = self.url + link
                        self.save_data = "name"
                        self.handle_that_data = True
                except KeyError:
                    pass
            elif self.save_data == "name" and tag == "td":
                self.save_data = "size"
                self.handle_that_data = True
            elif self.save_data == "size" and tag == "span":
                self.save_data = "seeds"
                self.handle_that_data = True
            elif self.save_data == "seeds" and tag == "span":
                self.save_data = "leech"
                self.handle_that_data = True
                
        def handle_data(self, data):
            if self.handle_that_data:
                if self.save_data == "name":
                    if 'name' not in self.current_item:
                        self.current_item["name"] = ""
                    self.current_item["name"] += data
                else:
                    self.current_item[self.save_data] = data
                if self.current_item.__len__() == 7:
                    self.current_item["name"] = self.name_repl.sub("", self.current_item["name"])
                    prettyPrinter(self.current_item)
                    self.current_item = None
                    self.save_data = None

        def handle_endtag(self, tag):
            if self.save_data == "name":
                if tag == "a":
                    self.handle_that_data = False
            else:
                self.handle_that_data = False

    def search(self, what, cat='all'):
        query = "http://bt.3dmgame.com/search.php?keyword=" + what
        data = retrieve_url(query)

        parser = self.Parsar(self.url)
        parser.feed(data)
        
        del data
        return

if __name__ == "__main__":

    engine = threedm()
    engine.search('drive')

