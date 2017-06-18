from urllib.parse import urlparse, parse_qs
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pyquery import PyQuery as pq
from strange.items.neteasemusic.items import (PlayListItem, SongItem,
                                              ArtistItem, AlbumItem)


class NetEaseMusic(CrawlSpider):
    name = 'neteasemusic'

    custom_settings = {
        'ITEM_PIPELINES': {
            'strange.pipelines.neteasemusic.pipelines.NetEaseMusicPipeline': 400
        }
    }

    allowed_domains = ['music.163.com']

    start_urls = ['http://music.163.com/#/discover/playlist']

    rules = (
        Rule(LinkExtractor(allow=('/playlist\?id=', )),
             callback='parse_playlist', follow=True),
        Rule(LinkExtractor(allow=('/song\?id=', )),
             callback='parse_song', follow=True),
        Rule(LinkExtractor(allow=('/artist\?id=', )),
             callback='parse_artist', follow=True),
        Rule(LinkExtractor(allow=('/album\?id=', )),
             callback='parse_album', follow=True),
    )

    def get_url_id(self, url):
        _url = ''.join(url.split('#')[-1:])
        qs = urlparse(_url).query
        params = parse_qs(qs)
        id = params.get('id', [None])[0]
        return id

    def parse_playlist(self, response):
        url = response.url
        id = self.get_url_id(url)
        if not id:
            return

        html = pq(response.body)

        # name
        h2_name = html('h2[@class="f-ff2 f-brk"]')
        if not h2_name:
            return
        name = h2_name[0].text

        # img
        img = html('img[@class="j-img"]')
        if not img:
            return
        img_url = pq(img[0]).attr('data-src')

        # fav
        a = html('a[@data-res-id="' + id + '"][@data-res-action="fav"]')
        if not a:
            return
        a_html = pq(a[0])
        fav = int(a_html.attr('data-count'))

        return PlayListItem(id=id, name=name, img=img_url, fav=fav)

    def parse_song(self, response):
        url = response.url
        id = self.get_url_id(url)
        if not id:
            return

        html = pq(response.body)

        cnt = html('div[@class="cnt"]')
        if not cnt:
            return

        # name
        _cnt = pq(cnt[0])
        em = _cnt('em[@class="f-ff2"]')
        if not em:
            return
        name = em[0].text

        des = _cnt('p[@class="des s-fc4"]')
        if not (des and len(des) == 2):
            return

        # artist
        _artist = pq(des[0])('a[@class="s-fc7"]')
        if not _artist:
            return
        artist_url = pq(_artist[0]).attr('href')
        if not artist_url:
            return
        artist_id = self.get_url_id(artist_url)

        # album
        _album = pq(des[1])('a[@class="s-fc7"]')
        if not _artist:
            return
        album_url = pq(_album[0]).attr('href')
        if not album_url:
            return
        album_id = self.get_url_id(album_url)

        # comment count
        comment = _cnt('span[@id="cnt_comment_count"]')
        if not comment:
            return
        comment_count = comment[0].text
        if not comment_count.isdigit():
            comment_count = None

        # img
        cvrwrap = html('div').filter('.cvrwrap')
        if not cvrwrap:
            return
        img = cvrwrap('img').filter('.j-img')
        if not img:
            return
        img_url = img.attr('data-src')

        return SongItem(id=id, name=name, artist=artist_id, album=album_id,
                        comment_count=comment_count, img=img_url)

    def parse_artist(self, response):
        url = response.url

        # id
        id = self.get_url_id(url)
        if not id:
            return

        html = pq(response.body)

        # name
        btm = html('div').filter('.btm')
        if not btm:
            return
        artist_name = btm('h2').filter('#artist-name')
        if not artist_name:
            return
        name = artist_name.text()

        return ArtistItem(id=id, name=name)

    def parse_album(self, response):
        url = response.url

        # id
        id = self.get_url_id(url)
        if not id:
            return

        html = pq(response.body)

        # name
        tit = html('div').filter('.tit')
        if not tit:
            return

        album_name = tit('h2').filter('.f-ff2')
        if not album_name:
            return
        name = album_name.text()

        # artist
        topblk = html('div').filter('.topblk')
        if not topblk:
            return

        artist_url = topblk('p').filter('.intr')('a').filter('.s-fc7')
        if not artist_url:
            return
        artist_id = self.get_url_id(artist_url.attr('href'))

        # time
        intr = topblk('p').filter('.intr')
        if not (intr and len(intr) == 2):
            return
        time_intr = pq(intr[1])
        publish_date = time_intr.text().split('：')[-1].strip()

        return AlbumItem(id=id, name=name, artist=artist_id,
                         publish_date=publish_date)
