import scrapy
from scrapy.http import HtmlResponse
from unsplash.items import UnsplashItem


class GoodimagesSpider(scrapy.Spider):
    name = "goodimages"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://www.unsplash.com/"]

    def parse(self, response):
        links = response.xpath("//div[@class='qaAX1']//a[@class='wuIW2 R6ToQ']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_image)

    def parse_image(self, response: HtmlResponse):
        title = response.xpath("//div[@class='wdUrX']//img[@itemprop='thumbnailUrl']/@alt").get()
        image = response.xpath("//div[@class='wdUrX']//img[@itemprop='thumbnailUrl']/@srcset").get().split()[12]
        category = response.url.split('/')[-1]
        yield UnsplashItem(title=title, image=image, category=category)
        print()

