from datetime import datetime

from sqlalchemy import Column, String, DateTime, BigInteger, Date

from strange.database import Base


class PlayList(Base):
    __tablename__ = 'netease_playlist'

    id = Column(String(64), primary_key=True)
    name = Column(String(255))
    fav = Column(BigInteger)
    img = Column(String(512))
    updated_at = Column(DateTime, default=datetime.now())


class Song(Base):
    __tablename__ = 'netease_song'

    id = Column(String(64), primary_key=True)
    name = Column(String(255))
    artist = Column(String(64))
    album = Column(String(64))
    comment_count = Column(BigInteger)
    img = Column(String(512))
    updated_at = Column(DateTime, default=datetime.now())


class Artist(Base):
    __tablename__ = 'netease_artist'

    id = Column(String(64), primary_key=True)
    name = Column(String(255))
    updated_at = Column(DateTime, default=datetime.now())


class Album(Base):
    __tablename__ = 'netease_album'

    id = Column(String(64), primary_key=True)
    name = Column(String(255))
    artist = Column(String(64))
    publish_at = Column(Date)
    updated_at = Column(DateTime, default=datetime.now())
