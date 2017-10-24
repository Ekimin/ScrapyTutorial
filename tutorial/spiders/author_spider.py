import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author page
        quotes = response.css('div.quote')
        for quote in quotes:
            author_name = quote.css('small.author::text').extract_first()
            author_url = quote.xpath('span[2]/a/@href').extract_first()
            if author_url is not None:
                yield response.follow(author_url, callback=self.parse_author)

        # next page
        next_page = response.css('ul.pager a::attr(href)').extract_first()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        birthday = response.css('span.author-born-date::text').extract_first()
        born_location = response.css('span.author-born-location::text').extract_first()
        description = response.css('div.author-description::text').extract_first()
        yield {
            'birthday': birthday,
            'born_location': born_location,
            'description': description
        }
