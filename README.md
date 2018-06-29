[Plugin list](https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins)

# qbit_search_plugins
Don't blame me if these run slow, it has to use chinese servers

looking for more torrent sites

## ali213.net : ali213.py
  Chinese Gaming Website

  Beware that they sometimes upload uncracked games on here.
  If you click the "Show description page" button, you will get additional non-torrent links.
  For more info open the file inside a text editor and read the first lines

## bt.3dmgame.com : threedm.py
  Chinese Gaming Website

  Beware that they sometimes upload uncracked games on here.
  

## [Jackett](https://github.com/Jackett/Jackett) : jackett.py
  Search engine for a wide range of trackers

  *  You will need to have the jackett service installed and running.
  *  There is an optional `jackett.json` file, which you can put in the same folder, so your configuration will survive updates
  *  The plugin tries to get your api key automatically, if that fails:
      * you will need to replace `YOUR_API_KEY_HERE` with your own in the `jackett.py` or `jackett.json` file
      * Your api key is written under the `Adding a Jackett indexer in Sonarr or Radarr` section
  * If your jackett does not run under `http://127.0.0.1:9117` you will need to change that as well

## small-games.info : smallgames.py
  Russian Gaming Website
  
  Not all results return a torrent file.
  Click description button to see the game page for it.
  If there is a mediaget button, you can add &direct=1
  to its link to get the torrent file.
