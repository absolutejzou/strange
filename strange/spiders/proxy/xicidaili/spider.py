from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pyquery import PyQuery as pq
from strange.items.proxy.items import ProxyItem


class XiciDaili(CrawlSpider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']

    start_urls = ['http://www.xicidaili.com/nn/']

    rules = [
        Rule(LinkExtractor(allow=('nn\/', )),
             callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        html = pq(response.body)
        table = html("#ip_list")
        if not table:
            return
        trs = table('tr')


        for tr in trs.items():
            tds = tr('td')
            if tds:
                ip = pq(tds[1]).text()
                port = pq(tds[2]).text()

                yield ProxyItem(ip=ip, port=port)
