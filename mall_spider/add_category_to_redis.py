from pymongo import MongoClient
from redis import StrictRedis
import pickle
from mall_spider.settings import MONGODB_URL, REDIS_URL
from mall_spider.spiders.jd_product import JdProductSpider


def add_category_to_redis():
    # 链接MongoDB
    mongo = MongoClient(MONGODB_URL)
    # 链接Redis
    redis = StrictRedis.from_url(REDIS_URL)
    # 读取MongoDB中分类信息，序列化后，添加到商品爬虫redis_key指定的list
    collection = mongo['jd']['category']
    # 读取分类信息
    cursor = collection.find()
    # 遍历分类信息
    for category in cursor:
        # 请发字典数据
        data = pickle.dumps(category)
        # 添加到商品爬虫redis_key指定的list
        redis.lpush(JdProductSpider.redis_key, data)
    # 关闭MongoDB
    mongo.close()


if __name__ == '__main__':
    add_category_to_redis()
