FROM python:3

WORKDIR /app

RUN wget https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/helpers.py && \
    wget https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/nova2.py && \
    wget https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/nova2dl.py && \
    wget https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/novaprinter.py && \
    wget https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/sgmllib3.py && \
    wget https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/socks.py

COPY . /app

RUN chmod -R 777 /app/tests
