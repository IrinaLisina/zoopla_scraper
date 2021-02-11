import scrapy, time

from zoopla.items import ZooplaItems

class zooplaspider(scrapy.Spider):
    name = "zooplaspider"
    allowed_domains = ["zoopla.co.uk"]
    start_urls = ("https://www.zoopla.co.uk/house-prices/london/courtfield-road/sw7-4da/?q=sw7%204da",)

    def parse(self, response):
        links = response.xpath('//div[@class="hp-card-list"]/section[@class="hp-card"]/a[@class="hp-card__content"]/@href').extract()
        i = 1
        for link in links:
            abs_url = response.urljoin(link)
            url_next = 'div[@class="hp-card-list"]/section[@class="hp-card"]/a/div{@class="hp-card__estimates"]/div/span[@class="hp-datum__value"]/text()'
            estimate = response.xpath(url_next).extract()
            if (i<= len(links)):
                i = i + 1
                time.sleep(10)
                yield scrapy.Requests(abs_url, callback = self.parse_indetail, meta={'estimate' : estimate})

    def parse_indetail(self, response):
        item = ZooplaItems()
        item['address'] = response.xpath('//div{@class="pdp-summary__details"]/h1/text()').extract
        item['price_estimate'] = response.xpath('//div[@class="pdp-estimate__results"]/h5/text()').extract
        item['price_history'] = response.xpath('//span{@class="pdp-history__details"]/span{@class="pdp-history__price"]/text()').extract

        return item
