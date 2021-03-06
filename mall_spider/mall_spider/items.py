# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MallSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

"""
类别数据模型类：用于存储类别信息（Category)-字段：
b_category_name:大类别名称
b_category_url:大类别url
m_category_name:中类别名称
m_category_url:中类别名称
s_category_name:小类别名称
s_category_url:小类别名称
"""

class Category(scrapy.Item):
    b_category_name = scrapy.Field()
    b_category_url = scrapy.Field()
    m_category_name = scrapy.Field()
    m_category_url = scrapy.Field()
    s_category_name = scrapy.Field()
    s_category_url = scrapy.Field()

"""
端口数据模型类：用于存储商品信息（Product)
字段：
product_category: 商品类别
product_sku_id: 商品id
product_name: 商品名称
product_img_url: 商品图片URL
product_book_into: 图书信息，作者，出版社
product_option: 商品选项
product_shop: 商品店铺
product_comments: 商品评论数量
product_ad: 商品促销
product_price: 商品价格
"""

class Product(scrapy.Item):
    product_category = scrapy.Field()
    product_sku_id = scrapy.Field()
    product_name = scrapy.Field()
    product_img_url = scrapy.Field()
    product_book_info = scrapy.Field()
    product_option = scrapy.Field()
    product_shop = scrapy.Field()
    product_comments = scrapy.Field()
    product_ad = scrapy.Field()
    product_price = scrapy.Field()
    product_category_id = scrapy.Field()