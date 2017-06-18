# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import requests

from scrapy import signals
from scrapy.conf import settings
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from sqlalchemy import func
from strange.database import Proxy
from strange.database.session import Session


class StrangeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent='Scrapy'):
        super(RandomUserAgentMiddleware, self).__init__()
        user_agent_file = settings.get('USER_AGENT_FILE')
        if not user_agent_file:
            self.user_agents = [user_agent]
        else:
            with open(user_agent_file, 'r') as f:
                self.user_agents = [l.strip() for l in f.readlines()]


    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        if user_agent:
            request.headers.setdefault(b'User-Agent', user_agent)


class ProxyMiddleware(object):

    def __init__(self):
        self.session = Session().session

    def process_request(self, request, spider):
        proxy = (self.session
                 .query(Proxy)
                 .filter(Proxy.status == 0)
                 .order_by(func.random())
                 .first())
        if proxy:
            ip, port = proxy.ip, proxy.port
            p = "http://{}:{}".format(ip, port)
            request.headers.setdefault(b'proxy', p)


class NetEaseMusicMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == 'neteasemusic':
            proxies = None
            headers = requests.utils.default_headers()
            if 'proxy' in request.headers:
                proxy = request.headers.get('proxy')
                type = proxy.split(b':')[0]
                proxies = {type: proxy,}
            if 'User-Agent' in request.headers:
                user_agent = request.headers.get('User-Agent')
                headers.update({
                    'User-Agent': user_agent,
                })
            c = requests.get(request.url.replace('/#', ''), proxies=proxies,
                             headers=headers)
            content = c.content
            return HtmlResponse(request.url, body=content,
                                encoding='utf-8',request=request)
        return
