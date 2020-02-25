# -*- coding: utf-8 -*-
import scrapy
from mall_spider.items import Product
import json
from jsonpath import jsonpath
from scrapy_redis.spiders import RedisSpider
import pickle


class JdProductSpider(RedisSpider):
    name = 'jd_product'
    allowed_domains = ['jd.com', '3.cn']
    #用于指定起始url列表，在redis数据库中key
    redis_key = 'jd_product:category'
    # start_urls = ['http://jd.com/']

    # def start_requests(self):
    #     category = {"b_category_name": "家用电器",
    #                 "b_category_url": "https://jiadian.jd.com",
    #                 "m_category_name": "电视",
    #                 "m_category_url": "https://list.jd.com/list.html?cat=737,794,798",
    #                 "s_category_name": "曲面电视",
    #                 "s_category_url": "https://list.jd.com/list.html?cat=737,794,798&ev=4155_92263&sort=sort_rank_asc&trans=1&JL=6_0_0"
    #
    #     }
    #     yield scrapy.Request(category['s_category_url'],callback=self.parse,meta={'category': category})
    def make_request_from_data(self, data):
        category = pickle.loads(data)
        #根据小分类的URL，构建列表页的请求
        #注意：要使用return来返回一个请求，不能使用yield
        return scrapy.Request(category['s_category_url'], callback=self.parse, meta={'category': category})


    def parse(self, response):
        category = response.meta['category']
        # print(category)
        sku_ids = response.xpath('//div[contains(@class," j-sku-item")]/@data-sku').extract()
        for sku_id in sku_ids:
            item = Product()
            item['product_category'] = category
            item['product_sku_id'] = sku_id
            #构建商品详情页请求
            product_base_url = 'https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.0/{}.json'.format(sku_id)
            yield scrapy.Request(product_base_url, callback=self.parse_product_base, meta={'item': item})

        #获取商品下一页的URL
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_url:
            #补全url
            next_url = response.urljoin(next_url)
            # print(next_url)
            #构建下一页的请求
            yield scrapy.Request(next_url, callback=self.parse, meta={'category': category})


    def parse_product_base(self, response):
        #取出传递过来的数据
        item = response.meta['item']
        # print(item)
        # print(response.text)
        #把json字符串转换成字典
        result = json.loads(response.text)
        item['product_name'] = result['wareInfo']['basicInfo']['name']
        item['product_img_url'] = result['wareInfo']['basicInfo']['wareImage'][0]['small']
        item['product_book_info'] = result['wareInfo']['basicInfo']['bookInfo']
        color_size = jsonpath(result, '$..colorSize')
        if color_size:
            color_size = color_size[0]
            product_option = {}
            for option in color_size:
                title = option['title']
                value = jsonpath(option, '$..text')
                product_option[title] = value
            item['product_option'] = product_option

        #商品店铺
        shop = jsonpath(result, '$..shop')
        if shop:
            shop = shop[0]
            if shop:
                item['product_shop'] = {
                    'shop_id': shop['shopId'],
                    'shop_name': shop['name'],
                    'shop_score': shop['score']
                }
            else:
                item['product_shop'] = {
                    'shop_name': '京东自营',
                }

        #商品类别ID
        item['product_category_id'] = result['wareInfo']['basicInfo']['category']
        item['product_category_id'] = item['product_category_id'].replace(';',',')
        # print(item)
        #商品促销信息URL
        ad_url = 'https://cd.jd.com/promotion/v2?skuId={}&area=1_72_4137_0&cat={}'\
            .format(item['product_sku_id'], item['product_category_id'])
        yield scrapy.Request(ad_url, callback=self.parse_product_ad, meta={'item': item})


    def parse_product_ad(self, response):
        item = response.meta['item']
        # print(item)
        # print(response.body.decode('GBK'))
        result = json.loads(response.body.decode('utf-8'))
        item['product_ad'] = jsonpath(result, '$..ad')[0] if jsonpath(result, '$..ad') else ''
        # print(item)
        #构建评价信息
        comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.\
            format(item['product_sku_id'])
        yield scrapy.Request(comments_url, callback=self.parse_product_comments,meta={'item': item})


    def parse_product_comments(self, response):
        item = response.meta['item']
        # print(item)
        # print(response.text)
        result = json.loads(response.text)
        item['product_comments'] = {
            'CommentCount': jsonpath(result, '$..CommentCount')[0],
            'GoodCount': jsonpath(result, '$..GoodCount')[0],
            'PoorCount': jsonpath(result, '$..PoorCount')[0],
            'GoodRate': jsonpath(result, '$..GoodRate')[0],
        }
        # print(item)
        #构建价格请求
        price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['product_sku_id'])
        yield scrapy.Request(price_url, callback=self.parse_product_price, meta={'item': item})


    def parse_product_price(self, response):
        item = response.meta['item']
        # print(response.text)
        result = json.loads(response.text)
        item['product_price'] = result[0]['p']
        #把商品数据交给引擎
        yield item













