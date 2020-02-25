import requests
from utils.http import get_request_headers
from lxml import etree
from domain import Proxy

class BaseSpider(object):
    #提供三个类成员变量
    #urls: 代理ip网址的url的列表
    urls = []
    #group_xpath: 分组XPATH, 获取包含代理ip信息标签列表的XPATH
    group_xpath = ''
    #detail_xpath: 组内XPATH，获取代理IP详情的信息XPATH，格式为：{'ip':'xx','port':'xx','area':'xx'}
    detail_xpath = {}


    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath


    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content

    def get_first_from_list(self,lis):
        #如果列表中有元素就返回第一个，否则就返回空串
        return lis[0] if len(lis) != 0 else ''

    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            yield proxy

    def get_proxies(self):
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies

if __name__ == '__main__':
    spider = BaseSpider()

    # for proxy in spider.get_proxies():
    #     print(proxy)