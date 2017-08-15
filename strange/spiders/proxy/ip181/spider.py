from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery as pq

from strange.items.proxy.items import ProxyItem


class IP181(CrawlSpider):
    name = 'ip181'

    custom_settings = {
        'ITEM_PIPELINES': {
            'strange.pipelines.proxy.pipelines.ProxyPipeline': 300
        }
    }

    allowed_domains = ['ip181.com']

    start_urls = ['http://www.ip181.com/daili/1.html']

    rules = [
        Rule(LinkExtractor(allow=('daili\/', )),
             callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        html = pq(response.body)
        table = html('table')
        tbody = table('tbody')
        trs = tbody('tr').not_('.active')

        for tr in trs.items():
            tds = tr('td')
            ip = pq(tds[0]).html()
            port = pq(tds[1]).html()

            yield ProxyItem(ip=ip, port=port)
