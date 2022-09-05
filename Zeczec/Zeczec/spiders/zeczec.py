from scrapy import Request
from scrapy.spiders import Spider
from Zeczec.items import ZeczecItem
import re
class ZeczecSpider(Spider):
    name = 'zeczec'
    #allowed_domains = ['example.com']
    #start_urls = ['http://example.com/']
    count = 0 #修改600
    #page = 1 #修改51
    #target_page = 360 #修改100
    basic_url = "https://www.zeczec.com"
    
    def __init__(self,start_page,target_page):
        self.page = int(start_page)
        self.target_page = int(target_page)

    def start_requests(self):
        url = "https://www.zeczec.com/categories?page=" + str(self.page) + "&type=0"
        yield Request(url)
        
    def parse(self, response):
        all_title = response.xpath("//div[@class='w-full lg:w-1/4 mb-8 xs:w-1/2']/div")
        for i in all_title:
            self.count += 1
            item = ZeczecItem()
            title = i.xpath("a/h3/text()").extract_first()
            add_url = i.xpath("a/@href").extract_first()
            classify_1 = i.xpath("span/text()").extract_first()
            classify_2 = classify_1.strip()
            classify_3 = classify_2.split(" ")
            classify = classify_3[0]
            
            try:
                SF_1 = i.xpath("div/div/span/div/span/text()").extract_first()
                SF_2 = SF_1.strip()
        
                if SF_2 == "成功":
                    item["SF"] = "S"
                elif SF_2 == "集資失敗":
                    item["SF"] = "F"
                    
            except:
                item["SF"] = "募資尚未結束"
                
            item["classify"] = classify
            item["title"] = title
            item["number"] = str(self.count)#後續處理較方便
            url = self.basic_url + add_url
            item["url"] = url
            meta = {"item":item}
            #yield item
            cookies = {'age_checked_for':'12190'}#只針對單一項目有用
            yield Request(url, meta=meta, cookies=cookies, callback=self.parse_content, errback=self.error_back)#會出現18禁內容
            #但有些cookie不一樣
        
        if self.page < self.target_page:
            self.page += 1
            next_url = "https://www.zeczec.com/categories?page=" + str(self.page) + "&type=0"
            yield Request(next_url, callback=self.parse, errback=self.error_back)
        
    
    def parse_content(self, response):
        try:
            time_1 = response.xpath("//div[@class='mb-2 text-xs leading-relaxed']/text()").extract()[1]
            time_2 = time_1.strip()
            time_3 = time_2.split(" – ")
            item = response.meta["item"]
            item["start_time"] = time_3[0]
            item["end_time"] = time_3[1]
            backer = response.xpath("//div[@class='mb-1 text-xs leading-relaxed']/span[2]/text()").extract_first()
            item["backer"] = backer
            current_funds_1 = response.xpath("//div[@class='flex-auto']/div/text()").extract()[0]
            target_1 = response.xpath("//div[@class='flex-auto']/div/text()").extract()[1].strip()
            current_funds = re.search('(\d+,?)(\d+,?)(\d+,?)\d+', current_funds_1).group()
            target = re.search('(\d+,?)(\d+,?)(\d+,?)\d+', target_1).group()
            item["current_funds"] = current_funds.replace(',', '')
            item["target"] = target.replace(',', '')
            yield item
        except:
            #有時會碰到18禁頁面
            item = response.meta["item"]
            item["start_time"] = "需查詢"
            item["end_time"] = "需查詢"
            item["backer"] = "需查詢"
            item["current_funds"] = "需查詢"
            item["target"] = "需查詢"
            #item["number"] = "頁面錯誤" + str(self.count)
            yield item
            
        
    def error_back(self, response):
        print("求取錯誤")
            
    
            
        