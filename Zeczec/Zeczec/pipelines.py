# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import redis

class ZeczecPipeline:
    def process_item(self, item, spider):
        return item

class RedisPipeline(object):
    def open_spider(self, spider):
        host = spider.settings.get("REDIS_HOST")
        port = spider.settings.get("REDIS_PORT")
        db_index = spider.settings.get("REDIS_DB_INDEX")
        #de_psd =
        self.db_conn = redis.StrictRedis(host=host, port=port, db=db_index) 
        
    def process_item(self, item, spider):
        item_dict = dict(item)
        self.db_conn.rpush("Ｚeczec", item_dict)
        return item
    
    def close_spider(self, spider):
        self.db_conn.connection_pool.disconnect()

class CSVPipline(object):
    index = 0
    file = None
    
    def open_spider(self, spider):
        self.file = open("Zeczec.csv", "a", encoding="utf-8")
        
    def process_item(self, item, spider):
        
        if self.index == 0:
            column_name = "編號,案件名稱,strUrl,募資開始時間,募資結束時間,backer數,已募資金(原始貨幣),目標金額,SF,台經院大分類\n"
            self.file.write(column_name)
            self.index = 1
            
        Zeczec_str = item["number"]+","+\
                    item["title"]+","+\
                    item["url"]+","+\
                    item["start_time"]+","+\
                    item["end_time"]+","+\
                    item["backer"]+","+\
                    item["current_funds"]+","+\
                    item["target"]+","+\
                    item["SF"]+","+\
                    item["classify"]+"\n"
        self.file.write(Zeczec_str)
        return item
    
    def close_spider(self, spider):
        self.file.close()