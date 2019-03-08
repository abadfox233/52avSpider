# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import copy


from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors


class ProjectAvPipeline(object):
    def process_item(self, item, spider):
        return item


class AVImagePipeline(ImagesPipeline):

    '''

        52av 封面图片下载图片

    '''

    def item_completed(self, results, item, info):
        image_file_path = "NULL"
        for ok, value in results:
            image_file_path = value["path"]
        try:
            item["image_path"] = image_file_path
        except KeyError:
            pass
        return item


class MysqlTwistedPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        db_parms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
             )
        dp_poll = adbapi.ConnectionPool("MySQLdb", **db_parms)
        return cls(dp_poll)

    def __init__(self, db_pool):
        self.db_pool = db_pool

    def process_item(self, item, spider):
        temp_item = copy.deepcopy(item)
        query = self.db_pool.runInteraction(self.do_insert, temp_item)
        query.addErrback(self.handle_error, item)
        return item

    def handle_error(self, failure, item):
        print(item)
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()

        cursor.execute(insert_sql, params)

