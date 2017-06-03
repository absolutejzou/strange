import scrapy


class PlayListItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    fav = scrapy.Field()
    img = scrapy.Field()


class SongItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    artist = scrapy.Field()
    album = scrapy.Field()
    comment_count = scrapy.Field()
    img = scrapy.Field()


class ArtistItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class AlbumItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    artist = scrapy.Field()
    publish_date = scrapy.Field()
