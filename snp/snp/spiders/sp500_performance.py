import scrapy


class Sp500PerformanceSpider(scrapy.Spider):
    name = "sp500_performance"
    allowed_domains = ["www.slickcharts.com"]
    start_urls = ["https://www.slickcharts.com/sp500/performance"]

    def parse(self, response):
        for row in response.css('table.table tr'):
            yield {
                'number': row.css('td:nth-child(1)::text').get(),
                'company': row.css('td:nth-child(2) a::text').get(),
                'symbol': row.css('td:nth-child(3)::text').get(),
                'ytd_return': row.css('td:nth-child(4)::text').get()
            }
