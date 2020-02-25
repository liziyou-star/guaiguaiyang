from core.proxy_spider.base_spider import BaseSpider
from utils.http import get_request_headers
import time
import random
import requests
import sys
sys.path.append('../')
from core.db import mongo_pool
import re
import js2py


"""
实现西刺代理爬虫：http://www.xicidaili.com/nn/1
定义一个类，继承通用爬虫类(BasicSpider
提供urls, group_xpath 和 detail_xpath
"""
class XiciSpider(BaseSpider):
    urls = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1,11)]
    group_xpath = '//*[@id="ip-list"]/tr[position()>1]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()'
    }

    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类的方法，发送请求，获取响应数据
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        return response

class Ip3366Spider(BaseSpider):
    urls = ['http://www.Ip3366.net/free/?stype={}&page={}'.format(i,j) for i in range(1, 3, 1) for j in range(1,8)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类的方法，发送请求，获取响应数据
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        return response.content

class KaiSpider(BaseSpider):
    urls = ['http://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 6)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

    # 当我们两个页面访问时间间隔太短了，就报错了；这是一种反爬手段；
    # noinspection PyUnreachableCode
    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类的方法，发送请求，获取响应数据
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        return response.content

class ProxylistplusSpider(BaseSpider):
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-list-{}'.format(i) for i in range(1, 7)]
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()'
    }

    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类的方法，发送请求，获取响应数据
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        return response.content


    # ip66代理
class Ip66Spider(BaseSpider):
    urls = ['http://www.66ip.cn/{}'.format(i) for i in range(1, 11)]
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }

    def get_page_from_url(self, url):
        time.sleep(random.uniform(1, 3))
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        # if response.status_code == 521:
        #     # 这个cookie信息不是通过服务器响应设置过来的；是通过js加密生成的
        #     # 真正的js在po里面
        #     result = re.findall('window.onload=setTimeout\("(.+?)",200\);\s*(.+?)\s*</script> ', response.content.decode('GBK'))
        #     print(result)
        #     # 执行js，返回真正的js，把'eval("qo=eval;qo(po);")' 替换为 return po
        #     func_str = result[0][1]
        #     func_str = func_str.replace('eval("qo=eval;qo(po);")', 'return po')
        #     print(func_str)
        #     # 获取执行js的环境
        #     context = js2py.EvalJs()
        #     # 加载（执行）func_str
        #     context.execute(func_str)
        #     # 执行这个方法，生成我们需要的js
        #     context.execute('code = {};'.format(result[0][0]))
        #     # 打印最终生成的代码
        #     print(context.code)
        #     cookie_str = re.findall("document.cookie='(.+?); ", context.code)[0]
        #     print(cookie_str)
        #     headers['Cookie'] = cookie_str
        #     response = requests.get(url, headers=headers)
        #     print(response.content.decode('GBK'))
        #     return response.content.decode('GBK')
        # else:
        #     return response.content.decode('GBK')
        return response.content

class Free89ipSpider(BaseSpider):
    '''
    89ip代理爬虫
    '''
    urls = ['http://www.89ip.cn/index{}.html'.format(i) for i in range(1, 11)]

    group_xpath = '//div/table[@class="layui-table"/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }

    def get_page_from_url(self, url):
        # 随机等待1到3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类的方法，发送请求，获取响应数据
        headers = get_request_headers()
        response = requests.get(url, headers=headers)
        return response.content

    # def get_proxies(self):
    #     proxies = super().get_proxies()
    #     for item in proxies:
    #         item.ip = str(item.ip).replace("\n", "").replace("\t", "")
    #         item.area = str(item.area).replace("\n", "").replace("\t", "")
    #         item.port = str(item.port).replace("\n", "").replace("\t", "")
    #         # 返回Proxy对象
    #         yield item
    #
    # def get_ip():
    #     proxy_list = []
    #     for ip in ip_list:
    #         proxy_list.append('http://' + ip)
    #     proxy_ip = random.choice(proxy_list)
    #     proxies = {'http': proxy_ip}
    #     return proxies

# if __name__ == '__main__':
#     spider = KaiSpider()
#     spider = Ip3366Spider()
#     spider = XiciSpider()
#     spider = ProxylistplusSpider()
#     spider = Ip66Spider()
#     spider = Free89ipSpider()
