MAX_SCORE = 50

#日志的配置信息
import logging
LOG_LEVEL = logging.DEBUG
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'Log.Log'

#测试代理ip的超时时间
TEST_TIMEOUT = 10

# MongoDB数据库的URL
MONGO_URL = 'mongodb://127.0.0.1:27017'

PROXIES_SPIDERS = [
    #爬虫的全类名，路径：模块.类名
    'core.proxy_spider.proxy_spiders.Ip66Spider',
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.KaiSpider',
    'core.proxy_spider.proxy_spiders.ProxylistplusSpider',
    'core.proxy_spider.proxy_spiders.XiciSpider',
    'core.proxy_spider.proxy_spiders.Free89ipSpider',
]

#配置爬虫运行时间间隔,单位为小时
RUN_SPIDERS_INTERVAL = 2
#配置检测代理ip的异步数量
TEST_PROXIES_ASYNC_COUNT = 24
#检测代理ip的时间间隔,单位为小时
TEST_PROXIES_INTERVAL = 2

#配置获取随机代理Ip最大数量；这个值越小可用性就越高；随机性就越差
PROXIES_MAX_COUNT = 50


