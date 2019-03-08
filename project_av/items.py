# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose

from project_av.settings import SQL_DATETIME_FORMAT


class ProjectAvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Av52ItemLoader(ItemLoader):

    default_output_processor = TakeFirst()


def create_list_loader(value):
        return value


class Av52Item(scrapy.Item):

    movie_html_url = scrapy.Field()
    cover_image = scrapy.Field(
        output_processor=MapCompose(create_list_loader)
    )
    image_path = scrapy.Field()
    title = scrapy.Field()
    movie_object_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into movie(movie_url, image_url, image_path, title, movie_object_id) " \
                     "VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE image_path = VALUES(image_path)"

        params = (
                    self['movie_html_url'],
                    ','.join(self['cover_image']),
                    self['image_path'] if self['image_path'] else "NULL",
                    self['title'],
                    self['movie_object_id'],

                )

        return insert_sql, params


class Av52BigImageItem(scrapy.Item):
    movie_object_id = scrapy.Field()
    cover_image = scrapy.Field()
    image_path = scrapy.Field()
    issue_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into video_images(`issue_time`,`big_images`, `big_images_path`,`video_object_id`) " \
                     "VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE issue_time = VALUES(`issue_time`)"

        params = (
            self['issue_time'] if self['issue_time'] is not "" else datetime.datetime.now().strftime(SQL_DATETIME_FORMAT),
            self['cover_image'][0] if type(self['cover_image']) is list else self['cover_image'],
            self['image_path'] if self['image_path'] else "NULL",
            self['movie_object_id'],

        )

        return insert_sql, params


class Av52VideoItem(scrapy.Item):
    movie_object_id = scrapy.Field()
    m3u8_url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into video_url(`m3u8_url`, `video_object_id`) " \
                     "VALUES (%s,%s) ON DUPLICATE KEY UPDATE m3u8_url = VALUES(m3u8_url)"

        params = (
            self['m3u8_url'],
            self['movie_object_id'],

        )

        return insert_sql, params
