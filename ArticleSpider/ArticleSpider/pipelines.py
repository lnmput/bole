# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonExportPipeline(object):
    def __init__(self):
        self.file = open('haha.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

class DbMysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'test', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
        pass

    def process_item(self, item, spider):
        sql = """
            insert into bole (title, url, url_id, image, image_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (item['title'], item['url'], item['url_id'], item['image'][0], item['image_path']))
        self.conn.commit()

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        sql = """
                   insert into bole (title, url, url_id, image, image_path)
                   VALUES (%s, %s, %s, %s, %s)
               """
        cursor.execute(sql, (item['title'], item['url'], item['url_id'], item['image'][0], item['image_path']))

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)


class JsonEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('item.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    # 重写这个方法
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_path = value['path']
        item['image_path'] = image_path

        return item