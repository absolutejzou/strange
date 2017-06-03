from datetime import datetime
import inflection
from strange.database.neteasemusic.models import PlayList, Song, Artist, Album
from strange.database.session import Session


class NetEaseMusicPipeline(object):
    def open_spider(self, spider):
        self.session = Session().session

    def process_item(self, item, spider):
        self.dispatch(item, spider)
        return item

    def dispatch(self, item, spider):
        getattr(self, 'process_' +
                inflection.underscore(item.__class__.__name__))(item, spider)

    def process_play_list_item(self, item, spider):
        play_list = PlayList(id=item['id'],
                             name=item['name'],
                             img=item['img'],
                             fav=item['fav'])

        self.session.merge(play_list)
        self.session.commit()

    def process_song_item(self, item, spider):
        song = Song(id=item['id'],
                    name=item['name'],
                    artist=item['artist'],
                    album=item['album'],
                    comment_count=item['comment_count'],
                    img=item['img'])

        self.session.merge(song)
        self.session.commit()

    def process_artist_item(self, item, spider):
        artist = Artist(id=item['id'],
                        name=item['name'])

        self.session.merge(artist)
        self.session.commit()

    def process_album_item(self, item, spider):
        album = Album(id=item['id'],
                      name=item['name'],
                      artist=item['artist'],
                      publist_at=datetime.strptime(item['publish_date'],
                                                   '%Y-%m-%d'))

        self.session.merge(album)
        self.session.commit()

    def close_spider(self, spider):
        self.session.close()
