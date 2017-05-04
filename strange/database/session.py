from sqlalchemy.orm import sessionmaker
from strange.database import engine


class Session(object):
    def __init__(self):
        pass

    @property
    def session(self):
        s = sessionmaker(bind=engine)
        return s()
