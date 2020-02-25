from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule
import time


from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL



class ProxyTester(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    def run(self):
        proxies = self.mongo_pool.find_all()
        for proxy in proxies:
            #把代理ip添加到队列中
            self.queue.put(proxy)
        #开启多个异步检测代理ip
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            #通过异步回调，使用死循环不断执行这个方法
            self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)
        #让当前线程等待队列任务完成
        self.queue.join()

    def __check_one_proxy(self):
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        # 如果代理不可用，让代理分数-1
        if proxy.speed == -1:
            proxy.score -= 1
            # 如果代理分数等于0就从数据库中删除该代理
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                # 否则更新该代理ip
                self.mongo_pool.update_one(proxy)
        else:
            # 如果代理可用，就恢复该代理的分数，更新到数据库
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        #调试队列的task_done方法
        self.queue.task_done()

    @classmethod
    def start(cls):
        proxy_tester = cls()
        proxy_tester.run()
        #每隔一段时间检测代理ip
        schedule.every(TEST_PROXIES_INTERVAL).hours.do(proxy_tester.run)
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    # pt = ProxyTester()
    # pt.run()
    ProxyTester.start()

