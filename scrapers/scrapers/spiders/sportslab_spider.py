from scrapy.spiders import CrawlSpider


class SportsLabSpider(CrawlSpider):
    name = 'sportslab_crawl'
    allowed_domains = ['sportslab.pk']
    start_urls = ['https://www.sportslab.pk/']

    def parse_start_url(self, response, **kwargs):
        for link in response.css('.menu-item.main-menu-item.drop-menu.dropdown:nth-child(n+2) > div > ul > li > a::attr(href)').getall():
            yield response.follow(url=link, callback=self.parse_main_categories)

    def parse_main_categories(self, response, **kwargs):
        for link in response.css('.product-layout > div > div > a::attr(href)').getall():
            yield response.follow(url=link, callback=self.parse_products)

    def parse_products(self, response, **kwargs):
        item = {
            'url': response.url,
            'category': response.css('ul.breadcrumb>li:nth-child(3) > a::text').get(),
            'title': response.css('h1.title>span::text').get(),
            'info': response.css('div.info-block-title::text').get(),
            'price': response.css('div.product-price::text').get(),
            'images': [x for x in response.css('div.main-image > div > div > div.swiper-slide>img::attr(data-largeimg)').getall()],
            'manufacturer-logo': response.css('div.product-manufacturer.brand-image>a>img::attr(src)').get(),
        }
        for ele in response.css('div.product-stats>ul>li'):
            item[ele.css('b::text').get().replace(':', '')] = ele.css('span::text').get()
        for ele in response.css('div.product-options > div'):
            item[ele.css('label::text').get()] = [x.strip() for x in ele.css('select > option:nth-child(n+2)::text').getall()]
        for ele in response.css('.product_extra .tab-content > div:nth-child(1) > div > div > div'):
            item['description'] = '\n\n'.join(ele.css('span::text').getall()) + '\n' + '\n'.join(ele.css('ul > li::text').getall())
        yield item