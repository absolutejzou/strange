
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery as pq

from strange.items.proxy.items import ProxyItem


class KuaiDaiLi(CrawlSpider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']

    start_urls = ['http://www.kuaidaili.com/proxylist/1/']

    rules = [
        Rule(LinkExtractor(allow=('proxylist\/', )),
             callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        html = pq(response.body)
        table = html('#index_free_list')
        tbody = table('tbody')
        trs = tbody('tr')

        for tr in trs.items():
            td_ip = tr('[data-title=IP]')
            ip = td_ip.html()
            td_port = tr('[data-title=PORT]')
            port = td_port.html()

            yield ProxyItem(ip=ip, port=port)
