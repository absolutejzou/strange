from datetime import datetime
from scrapy.exceptions import DropItem
from strange.database import Proxy
from strange.database.proxy.choices import ProxyStatus
from strange.database.session import Session
from sqlalchemy import and_


class ProxyPipeline(object):
    def open_spider(self, spider):
        self.session = Session().session

    def process_item(self, item, spider):
        if not item['ip']:
            return DropItem('drop item, ip is: %s' % item['ip'])

        proxy = (self.session
                 .query(Proxy)
                 .filter(and_(Proxy.ip == item['ip'],
                              Proxy.port == item['port']))
                 .first())

        now = datetime.now()

        if proxy:
            if proxy.status == ProxyStatus.Available:
                return DropItem('drop item, ip exist: %s' % item['ip'])
            else:
                proxy.updated_at = now
                proxy.created_at = now
                self.session.commit()
        else:
            proxy = Proxy(ip=item['ip'],
                          port=item['port'],
                          created_at=now,
                          updated_at=now)

            self.session.add(proxy)
            self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
