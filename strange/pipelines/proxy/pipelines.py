from datetime import datetime
from scrapy.exceptions import DropItem
from strange.database import Proxy
from strange.database.proxy.choices import ProxyStatus
from strange.database.session import Session


class ProxyPipeline(object):
    def open_spider(self, spider):
        self.session = Session().session

    def process_item(self, item, spider):
        if not item['ip']:
            return DropItem('drop item, ip is: %s' % item['ip'])

        exist = (self.session
                 .query(Proxy)
                 .filter(Proxy.ip == item['ip'])
                 .filter(Proxy.status == ProxyStatus.Available)
                 .count())
        if exist:
            return DropItem('drop item, ip exist: %s' % item['ip'])

        now = datetime.now()

        proxy = Proxy(ip=item['ip'],
                      port=item['port'],
                      created_at=now,
                      updated_at=now)
        self.session.add(proxy)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
