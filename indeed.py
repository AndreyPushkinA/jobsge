import scrapy
from scrapy import Request, Item, Field
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser

class RowItem(Item):
    name = Field()
    company_name = Field()
    desc = Field()
    link = Field()


class PricePipeline:
    def process_item(self, item, spider):
        return item

class FindJobsSpider(Spider):
    name = 'findjobs'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'ITEM_PIPELINES': {
            'main.PricePipeline': 300
        },
        "FEEDS": {
            'items.csv': {
                'fields': ['name', 'company_name', 'desc', 'link'],
                'format': 'csv',
            },
        }
    }
    def start_requests(self):
        yield Request('https://www.indeed.com/jobs?q=data%20engineer&fromage=1&vjk=066470271eb69553', callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//a[contains(@class, "jcs-JobTitle")]/@href').extract():
            yield Request(response.urljoin(link), callback=self.parse_details)


        page = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
        if page:
            yield Request(response.urljoin(page), callback=self.parse)

    def parse_details(self, response):
        name = response.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
        company_name = response.xpath('//div[contains(@class, "icl-u-lg-mr--sm icl-u-xs-mr--xs")]/a/text()').extract_first()
        # date = response.xpath('//div[contains(@class, "jobsearch-JobMetadataFooter")]/div[2]/text()').extract_first()
        desc = '\n'.join(response.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
        link = response.url
        yield RowItem(name=name,
                      company_name=company_name,
                      desc=desc,
                      link=link
                    )

def main():
    process = CrawlerProcess(settings={
    "FEEDS": {
        "items.csv": {"format": "csv"},
    }})

    process.crawl(FindJobsSpider)
    process.start()



if __name__ == '__main__':
    main()