from multiprocessing import Process
from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyApi

def run():
    process_list = []
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTester.start))
    process_list.append(Process(target=ProxyApi.start))

    #遍历进程列表，启动所有进程
    for process in process_list:
        #设置守护进程
        process.daemon = True
        process.start()

    #遍历进程列表，让主进程等待子进程的完成
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()