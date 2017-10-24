# Scrapy Tutorial
## 创建项目
```
scrapy startproject tutorial
```

## 目录结构

```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

## 第一个程序

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```
爬虫继承了scrapy.Spider 并且定义了以下属性和方法：
- name：爬虫唯一标识
- start_requests(): 必须包含可迭代的requests供爬虫去爬，称为初始url，后续url可以通过初始url获得。
- parse(): 通常从response中解析数据，存入dict，找到新url，创建新的request。此方法的request参数是TextResponse的实例。

## 启动爬虫

```
scrapy crawl quotes
```

start_requests 返回scrapy.Response，每当scrapy收到每个response，便实例化Response对象，并把它传给parse()回调方法。

## 另一种写法

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
```

parce()是scarpy的默认回调方法，所以即使不显式写出也能达到同样效果。

## scrapy shell 'xxx' 常用命令

```
$ scrapy shell 'http://quotes.toscrape.com/page/1/'
...
2017-10-22 00:53:11 [scrapy.core.engine] DEBUG: Crawled (404) <GET http://quotes.toscrape.com/robots.txt> (referer: None)
2017-10-22 00:53:12 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x10bde0c90>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x10bde0910>
[s]   spider     <DefaultSpider 'default' at 0x10c0acf50>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects 
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
```

常用命令

- css
```
response.css('title')
response.css('title::text').extract()
response.css('title::text').extract_first()  --不会IndexError
response.css('title::text')[0].extract() --可能会IndexError
>>> response.css('title::text').re(r'Quotes.*') -- 正则
['Quotes to Scrape'] 
>>> response.css('title::text').re(r'Q\w+')
['Quotes']
>>> response.css('title::text').re(r'(\w+) to (\w+)')
['Quotes', 'Scrape']

>>> response.css('li.next a::attr(href)').extract_first()
'/page/2/'
```

- xpath
```
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath('//title/text()').extract_first()
'Quotes to Scrape'
```

## 小结
```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```

另外写法：

```
for href in response.css('li.next a::attr(href)'):
    yield response.follow(href, callback=self.parse)
```

```
for a in response.css('li.next a'):
    yield response.follow(a, callback=self.parse)
```

