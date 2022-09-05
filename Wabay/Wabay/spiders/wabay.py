from operator import itemgetter
from scrapy import Request
from scrapy.spiders import Spider
from Wabay.items import WabayItem
import re 

class WabaySpider(Spider):
    name = 'wabay'
    #allowed_domains = ['evample.com']
    #start_urls = ['http://evample.com/']
    page = 1
    count = 0
    basic_url = "https://wabay.tw"

    def __init__(self,target_page):
        self.target_page = int(target_page)
        
    def start_requests(self):
        url = 'https://wabay.tw/projects?locale=zh-TW&page=1&sort=all&type=' 
        yield Request(url)

    def parse(self, response):
        all_title = response.xpath("//div[@class='d-flex flex-column col-12 sm:col-6 md:col-4 px-4']/article")
        for i in all_title:
            project_type = i.xpath("div/div[@class='d-flex justify-content-between']/span/text()").extract_first()
            item = WabayItem()
            item['number'] = project_type.strip()
            title = i.xpath("div/div/h1/a/text()").extract_first()
            item['title'] = title

            add_url = i.xpath("div/a/@href").extract_first()
            check = "https"
            if add_url.count(check) == 0:
                url = self.basic_url + add_url
            else:
                url = add_url

            item['url'] = url
            meta = {"item":item}
            #yield item
            cookies = {'restricted_passed':'rumi3d'}
            yield Request(url, meta=meta, cookies=cookies, callback=self.parse_content, errback=self.errback_httpbin)
        
        if self.page < self.target_page:
            self.page += 1
            next_url = "https://wabay.tw/projects?locale=zh-TW&page=" + str(self.page) + "&sort=all&type="
            yield Request(next_url, callback=self.parse, errback=self.errback_httpbin)
        

    def parse_content(self, response):
        try:
            item = response.meta["item"]
            time_1 = response.xpath("//div[@class='row mb-4 font-size-4 sm:font-size-3']/div[@class='font-size-3']/text()").extract_first()
            time_2 = time_1.strip()
            time_3 = time_2.split(" ~ ")
            item['start_time'] = time_3[0]
            item['end_time'] = time_3[1]
            rate_1 = response.xpath("//div[@class='d-flex align-items-center mb-4']/span/text()").extract_first()
            rate_2 = rate_1.strip()
            rate = int(re.search('\d+', rate_2).group())
            
            if rate >= 100:
                item['SF'] = "S"
            else:
                item['SF'] = "F"
            classify = response.xpath("//div[@class='d-flex flex-wrap lg:justify-content-center mt-2 sm:mt-0']/a/text()").extract_first()
            item['classify'] = classify

            item['backer'] = ""
            item['current_funds'] = ""
            item['target'] = ""

        except:
            item = response.meta["item"]
            item['start_time'] = ""
            item['end_time'] = ""
            item['SF'] = ""
            item['classify'] = ""
            item['backer'] = ""
            item['current_funds'] = ""
            item['target'] = ""

        yield item


    def errback_httpbin(self, failure, response):
        url = failure.value.response.url
        print("求取錯誤")




    
