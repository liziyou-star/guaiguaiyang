from gevent import monkey
monkey.patch_all()

#导入协程池
from gevent.pool import Pool
import schedule
import time

import importlib
from settings import PROXIES_SPIDERS
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
from settings import RUN_SPIDERS_INTERVAL




class RunSpider(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        #创建协程池对象
        self.coroutine_pool = Pool()


    def get_spider_from_settings(self):
        """根据配置文件信息，获取爬虫对象列表"""
        #遍历配置文件中爬虫信息，获取每个爬虫全类名
        for full_class_name in PROXIES_SPIDERS:
            #获取模块名和类名
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            #根据模块名，导入模块
            module = importlib.import_module(module_name)
            # #根据类名，从模块中，获取类
            cls = getattr(module, class_name)
            #创建爬虫对象
            spider = cls()
            # print(spider)
            yield spider


    def run(self):
        # 根据配置文件信息，获取爬虫对象列表
        spiders = self.get_spider_from_settings()
        for spider in spiders:
            #把处理一个代理爬虫的代码抽到一个方法用于处理一个爬虫任务
            # self.__execute_one_spider_task(spider)
            self.coroutine_pool.apply_async(self.__execute_one_spider_task, args=(spider,))
            #调用协程的join方法，让当前线程等待协程任务的未完成
        self.coroutine_pool.join()

    def __execute_one_spider_task(self, spider):
        try:
            for proxy in spider.get_proxies():
                # 检测代理IP(调用检测模块)
                proxy = check_proxy(proxy)
                # 如果可用，写入数据库(调用数据库模块,speed不为-1就说明可用)
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
                    # print(proxy)
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def start(cls):
        rs = RunSpider()
        rs.run()
        #每间隔多少个小时运行爬虫
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    # rs = RunSpider()
    # rs.run()
    RunSpider.start()
    # def task():
    #     print('呵呵')
    #
    # schedule.every(10).seconds.do(task)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)