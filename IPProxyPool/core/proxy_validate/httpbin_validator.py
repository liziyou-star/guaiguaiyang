import time
import requests
import json

from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy

def check_proxy(proxy):
    """
    用于检查指定 代理ip 响应速度，匿名程度，支持协议类型
    :param proxy: 代理ip模型对象
    :return: 检查后的代理ip模型对象
    """
    # 准备代理ip字典
    proxies = {
        'http':'http://{}:{}'.format(proxy.ip, proxy.port),
        'https':'http://{}:{}'.format(proxy.ip, proxy.port),
    }

    # 测试该代理ip
    http,http_nick_type, http_speed = __check_http_proxies(proxies)
    https,https_nick_type, https_speed = __check_http_proxies(proxies, False)

    #代理IP支持的协议类型，http是0，https是1，https和http都支持是2
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = http_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy


def __check_http_proxies(proxies,is_http=True):
    #匿名类型：高匿：0，匿名：1，透明：2
    nick_type = -1
    #响应速度
    speed = -1

    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url='https://httpbin.org/get'
    try:
         #获取开始时间
        start = time.time()
         #发送请求，获取响应数据
        response = requests.get(test_url,headers=get_request_headers(),proxies=proxies,timeout=TEST_TIMEOUT)

        if response.ok:
            # 计算响应速度
            speed = round(time.time() - start,2)
            #匿名程度
            #把响应的json字符串，转换为字典
            dic = json.loads(response.text)
            #获取来源的ip
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            if ',' in origin:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                # 否则就是高匿代理
                nick_type = 0

            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as ex:
        # logger.exception(ex)
        return False, nick_type, speed

if __name__ == '__main__':

    proxy = Proxy('218.14.109.42', port='44942')
    print(check_proxy(proxy))