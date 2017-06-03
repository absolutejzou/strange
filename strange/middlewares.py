# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from scrapy.conf import settings
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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


class PhantomJSMiddleware(object):
    def __init__(self):
       pass

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def process_request(self, request, spider):
        service_args = ['--load-images=false', '--disk-cache=true']

        dcap = DesiredCapabilities.PHANTOMJS
        user_agent = ('Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) '
                      'Gecko/20100101 Firefox/4.0.1')
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        dcap['browserName'] = user_agent.split('/')[0]
        dcap['platform'] = 'Windows'
        dcap['version'] = user_agent.split(' ')[0].split('/')[1]

        self.driver = webdriver.PhantomJS(executable_path=
                                          settings.get('PHANTOMJS_DRIVER'),
                                          service_args=service_args,
                                          desired_capabilities=dcap)

        if spider.name == 'neteasemusic':
            self.driver.get(request.url)
            self.driver.switch_to.frame('g_iframe')
            body = self.driver.page_source.encode('utf-8')
            current_url = self.driver.current_url

            return HtmlResponse(current_url, body=body,
                               encoding='utf-8', request=request)
        return
