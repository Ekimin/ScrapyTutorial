# coding=utf-8
import scrapy

'''
传递参数的爬虫
scrapy crawl quotes-arg -o arg.json -a tag=humor
'''


class QuotesSpider(scrapy.Spider):
    name = "quotes-arg"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
            print('url=' + url)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
