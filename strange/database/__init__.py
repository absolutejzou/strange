from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

db_type = 'postgresql'
db_user = ''
db_password = ''
db_host = ''
db_port = 1111
db_database = ''

db_args = ('{0}://{1}:{2}@{3}:{4}/{5}'
           .format(db_type, db_user, db_password,
                   db_host, db_port, db_database))
engine = create_engine(db_args)

metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

from strange.database.proxy.models import Proxy
from strange.database.neteasemusic.models import PlayList, Song, Artist, Album


metadata.create_all()
