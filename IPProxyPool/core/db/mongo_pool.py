from pymongo import MongoClient
import pymongo
import random
from settings import MONGO_URL
from utils.log import logger
from domain import Proxy

"""
实现代理池的数据库模块
作用：用于对proxies集合进行数据库的相关操作
目标：实现对数据库增删改查相关操作
步骤：
1.在init中，建立数据连接，获取要操作的集合，在del方法中关闭数据库连接
"""
class MongoPool(object):
    def __init__(self):
        # 1.1.在init中，建立数据连接
        self.client = MongoClient(MONGO_URL)
        #1.2 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        #关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info('插入新的代理:{}'.format(proxy))
        else:
            logger.warning("已经存在的代理:{}".format(proxy))

    def update_one(self, proxy):
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info("删除代理ip: {}".format(proxy))

    def find_all(self):
        cursor = self.proxies.find()
        for item in cursor:
            # 删除_id这个key
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy


    def find(self, conditions={}, count=0):
        """
        实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，速度升序，保证优质的代理IP在上面
        :param conditions: 查询条件字典
        :param count: 限制最多取出多少个代理ip
        :return: 返回满足要求代理ip列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort([('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)])
        #准备列表，用于存储查询处理代理ip
        proxy_list = []
        #遍历 cursor
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        #返回满足要求代理Ip（proxy对象）列表
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        实现根据协议类型和要访问网站的域名，获取代理ip列表
        :param protocol:协议
        :param domain:域名
        :param count:限制获取多个代理ip
        :param nick_type:匿名类型，默认获取高匿的代理ip
        :return:满足要求代理ip列表
        """
        conditions = {'nick_type': nick_type}
        if protocol is None:
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in':[0,2]}
        else:
            conditions['protocol'] = {'$in':[1,2]}
        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}
        #返回满足要求代理ip列表
        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        实现根据协议类型和要访问网站的域名，随机获取一个代理ip
        :param protocol:
        :param domain:
        :param count:
        :param nick_type:
        :return: 返回满足要求的一个随机代理Ip
        """
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        #从proxy_list列表中，随机取出一个代理ip返回
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        实现把指定域名添加到指定Ip的disable_domain列表中
        :param ip: ip地址
        :param domain: 域名
        :return: 如果返回True, 就表示添加成功了，返回false添加推向了
        """
        # print(self.proxies.count_documents({'_id': ip, 'disable_domains':domain}))
        if self.proxies.count_documents({'_id': ip, 'disable_domains':domain}) == 0:
            #如果disable_domains字段中没有这个域名，才添加
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False




if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy('202.104.113.35', port='53281')
    # proxy = Proxy('202.104.113.36', port='53281')
    # mongo.insert_one(proxy)
    # proxy = Proxy('202.105.114.35', port='9999')
    # mongo.update_one(proxy)
    # proxy = Proxy('202.104.113.35', port='9999')
    # mongo.delete_one(proxy)
    # for proxy in mongo.find_all():
    #     print(proxy)
    # dic = {"ip": "202.104.113.38", "port": "53281","protocol":0,"nick_type":0,"speed": 8.2,"area":None,"score":50,"disable_domains":["jd.com"]}
    # dic = {"ip": "202.104.113.39", "port": "53281","protocol":1,"nick_type":0,"speed": 1.2,"area":None,"score":50,"disable_domains":["taobao.com"]}
    # dic = {"ip": "202.104.113.40", "port": "53281","protocol":2,"nick_type":0,"speed": 4.0,"area":None,"score":50,"disable_domains":[]}
    # dic = {"ip": "202.104.113.41", "port": "53281","protocol":2,"nick_type":0,"speed": -1,"area":None,"score":49,"disable_domains":[]}

    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)
    # for proxy in mongo.find():
    # for proxy in mongo.find({'protocol':2},count=1):
    #     print(proxy)

    # for proxy in mongo.get_proxies(protocol='https'):
    # for proxy in mongo.get_proxies(protocol='https', domain='taobao.com'):
    #      print(proxy)

    # mongo.disable_domain('202.104.113.38', 'taobao.com')