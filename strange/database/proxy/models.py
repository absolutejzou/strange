from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, DateTime, SMALLINT, Interval

from strange.database import Base
from strange.database.proxy.choices import ProxyStatus


class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(Integer, primary_key=True)
    ip = Column(String(15), unique=True)
    port = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    status = Column(SMALLINT, default=ProxyStatus.UnAvailable)
    on_duration = Column(Interval(), default=timedelta())
