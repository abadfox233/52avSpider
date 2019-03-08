# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import re
import copy

import scrapy
import MySQLdb

from project_av.items import Av52ItemLoader, Av52Item, Av52BigImageItem, Av52VideoItem
from project_av.utils.common import extract_num, get_md5, pass_url, get_time, get_page_num
from project_av.settings import GET_PAGE_MESSAGE

START_PAGE_NUM = 0
END_PAGE_NUM = 5


def update_start_end_num():
    global START_PAGE_NUM, END_PAGE_NUM
    conn = MySQLdb.connect("localhost", '52av', '52av', '52av', charset='utf8', use_unicode=True)
    cursor = conn.cursor()
    cursor.execute(GET_PAGE_MESSAGE)
    page_message = cursor.fetchall()
    for item in page_message:
        if item[0] == "start_page":
            START_PAGE_NUM = int(item[1])
        elif item[0] == 'end_page':
            END_PAGE_NUM = int(item[1])
    cursor.close()


update_start_end_num()


class Www52avTvSpider(scrapy.Spider):
    name = 'www_52av_tv'
    allowed_domains = ['www.52av.tv', 'video1.yocoolnet.com']
    start_urls = ['http://www.52av.tv']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    headers = {

        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.99 Safari/537.36"
    }

    def parse(self, response):
        self.logger.info('process %s ' % response.url)
        num = get_page_num(response.url)
        if num is not None and num > END_PAGE_NUM:
            return
        next_end_url = response.css('div.pgbtn a::attr(href)').extract_first()
        next_url = urljoin('http://www.52av.tv', next_end_url)
        movie_list = response.css('ul.ml.waterfall.cl li')
        for movie in movie_list:
            item_loader = Av52ItemLoader(item=Av52Item(), selector=movie)
            movie_end_url = movie.css('div.c.cl a::attr(href)').extract_first("").split('&extra')[0]
            movie_object_id = get_md5(movie_end_url)
            # if not pass_url(cursor, movie_object_id):
            #     print('pass_url', movie_object_id)
            #     continue
            item_loader.add_value('movie_html_url', urljoin('http://www.52av.tv', movie_end_url))
            cover_image = [urljoin('http://www.52av.tv', movie.css('div.c.cl a img::attr(src)').extract_first())]
            item_loader.add_value('cover_image', cover_image)
            item_loader.add_css('title', 'div.c.cl a img::attr(alt)')
            item_loader.add_value('movie_object_id', movie_object_id)
            yield scrapy.Request(urljoin('http://www.52av.tv', movie_end_url), headers=self.headers,
                                 callback=self.parse_js_url, meta={"video_object_id": get_md5(movie_end_url)})
            yield item_loader.load_item()
        yield scrapy.Request(next_url, headers=self.headers, callback=self.parse)

    def parse_js_url(self, response):
        video_object_id = copy.deepcopy(response.meta.get('video_object_id'))
        big_image_item = Av52BigImageItem()
        issue_time = get_time(response.css('div.authi em::text').extract_first(""))
        if not issue_time:
            issue_time = response.css('div.authi em span::attr(title)').extract_first()
        big_image_item['issue_time'] = issue_time
        big_image_item['cover_image'] = [response.css('ignore_js_op img::attr(file)').extract_first("")]
        big_image_item['movie_object_id'] = video_object_id
        yield big_image_item
        js_url = response.xpath('//iframe[contains(@src,"yocoolnet")]/@src').extract_first("")
        if js_url.startswith('//'):
            js_url = "https:" + js_url
        js_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) '
                          'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
            'Host': 'video1.yocoolnet.com',
            'Proxy - Connection': 'keep - alive',
            'Referer': js_url
        }
        yield scrapy.Request(js_url, headers=js_headers, callback=self.parse_m3u8_url,
                             meta={"movie_object_id": video_object_id}, )

    def parse_m3u8_url(self, response):
        item = Av52VideoItem()
        movie_object_id = copy.deepcopy(response.meta.get('movie_object_id'))
        html = response.text
        pattern = re.compile('a:"(https://.*\.yocoolnet.com.*\.m3u8)",')
        result = pattern.findall(html)
        if len(result) >= 1 and isinstance(result[0], str):
            item['m3u8_url'] = result[0]
            item['movie_object_id'] = movie_object_id
            yield item

    def start_requests(self):
        url = 'http://www.52av.tv/forum.php?mod=forumdisplay&fid=67&filter=typeid&typeid=128&page=%d' % START_PAGE_NUM
        yield scrapy.Request(url, headers=self.headers, dont_filter=True)
