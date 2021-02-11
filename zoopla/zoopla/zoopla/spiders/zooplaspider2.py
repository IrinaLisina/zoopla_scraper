import scrapy, time

from zoopla.items import ZooplaItems

class zooplaspider2(scrapy.Spider):
    name = "ZooplaSpider2"
    allowed_domains = ["zoopla.co.uk"]
    start_urls = ("https://www.zoopla.co.uk/house-prices/london/courtfield-road/sw7-4da/?q=sw7%204da",)

    def parse(self, response):
        for href in response.xpath('//div[@class="hp-card-list"]/section[@class="hp-card"]/a[@class="hp-card__content"]/@href').extract():
            url = response.urljoin(href)
            print(url)
            req = scrapy.Request(url, callback=self.parse_titles)
            req.meta['proxy'] = "https://yourproxy.com:80"
            time.sleep(10)
            yield req
            

    def parse_titles(self, response):
        item = ZooplaItems()
        item['address'] = response.xpath('//div{@class="pdp-summary__details"]/h1/text()').extract
        item['price_estimate'] = response.xpath('//div[@class="pdp-estimate__results"]/h5/text()').extract
        item['price_history'] = response.xpath('//span{@class="pdp-history__details"]/span{@class="pdp-history__price"]/text()').extract

        yield item

