from scrapy import Request
from scrapy.spiders import Spider
from FV.items import FvItem
import re


class FvSpider(Spider):
    name = 'fv'
    #allowed_domains = ['example.py']
    #start_urls = ['http://example.py/']
    count = 0 
    page = 1 
    #target_page = 281 #281 
    basic_url = "https://www.flyingv.cc/projects?filter=all&sort=end&category=all&page="

    def __init__(self,target_page):
        self.target_page = int(target_page)

    def start_requests(self):
        url = "https://www.flyingv.cc/projects?filter=all&sort=end&category=all&page=1" 
        yield Request(url)
        
    def parse(self, response):
        all_title = response.xpath("//div[@class='col-md-4 col-sm-6']/div[@class='projectCard']")
        for i in all_title:
            item = FvItem()
            self.count += 1
            title = i.xpath("div/h2/text()").extract_first()
            item['title'] = title
            item['number'] = str(self.count)
            url = i.xpath("a/@href").extract_first()
            item['url'] = url
            meta = {"item":item}
            yield Request(url, meta=meta, callback=self.parse_content, errback=self.error_back)
            
        if self.page < self.target_page:
            self.page += 1
            next_url = self.basic_url + str(self.page)
            yield Request(next_url, callback=self.parse, errback=self.error_back)
            
    def parse_content(self, response):
        try:
            item = response.meta["item"]
            backer_1 = response.xpath("//div[@class='numberRow totalPeople']/h2/text()").extract_first()
            backer = re.search('\d+', backer_1).group()
            item['backer'] = backer
            target_1 = response.xpath("//div[@class='number-wrapper']/div/p/text()").extract_first()
            target = re.search('\d+', target_1).group()
            item['target'] = target
            current_funds = response.xpath("//div[@class='number-wrapper']/div/h2/text()").extract_first()
            item['current_funds'] = current_funds
            
            SF_check = response.xpath("//div[@class='numberRow totalDays']/p/text()").extract_first()
            if SF_check == "募資倒數":
                item['SF'] = "募資尚未結束"
                end_time_1 = response.xpath("//div[@class='col-sm-4 sidebar numberSidebar']/blockquote/text()").extract()[1]
                end_time_2 = end_time_1.strip()
                end_time_3 = re.search('(\d+)/(\d+)/(\d+)', end_time_2).group()
                item['end_time'] = end_time_3.strip()
                item['start_time'] = "需查詢"
            else:
                SF_1 = response.xpath("//div[@class='number-wrapper']/div/div/text()").extract_first()
                SF_2 = int(re.search('\d+', SF_1).group())
            
                if SF_2 >= 100:
                    item['SF'] = "S"
                else:
                    item['SF'] = "F"
                    
                start_time_1 = response.xpath("//div[@class='col-sm-4 sidebar numberSidebar']/blockquote/text()").extract()[0]
                start_time_2 = start_time_1.strip()
                start_time_3 = start_time_2.split(" - ")
                start_time = re.search('(\d+)/(\d+)/(\d+)', start_time_3[0]).group()
                item['start_time'] = start_time
                end_time = re.search('(\d+)/(\d+)/(\d+)', start_time_3[1]).group()
                item['end_time'] = end_time
                
            classify = response.xpath("//div[@class='projectTitle']/div/span/text()").extract_first()
            item['classify'] = classify
            
            yield item

        except:

            item = response.meta["item"]
            item["start_time"] = "需查詢"
            item["end_time"] = "需查詢"
            item["backer"] = "需查詢"
            item["current_funds"] = "需查詢"
            item["target"] = "需查詢"
            item['SF'] = "需查詢"
            item['classify'] = "需查詢"
            yield item
            
        
    def error_back(self, response):
        print("求取錯誤")
            
