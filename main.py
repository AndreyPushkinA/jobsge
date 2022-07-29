import scrapy
from scrapy import Request
from scrapy.item import Item, Field
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess

def clean_spaces(substr: str) -> str:
    if not substr:
        return ''
    return substr.replace('\n', '').replace('\t', '')


class RowItem(Item):
    title = Field()
    company_name = Field()
    link = Field()


class PricePipeline:

    def process_item(self, item, spider):
        item['title'] = clean_spaces(item['title'])
        item['company_name'] = clean_spaces(item['company_name'])
        item['link'] = clean_spaces(item['link'])
        return item

class FindJobsSpider(Spider):
    name = 'findjobs'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'ITEM_PIPELINES': {
            'main.PricePipeline': 300
        }
    }
    def start_requests(self):
        yield Request('https://jobs.ge/en/?page=1/')
    def parse(self, response):
        for row in response.xpath('//table[@id="job_list_table"]/tr')[1:]:
            title = row.xpath('./td/a/text()').extract_first('')
            company_name = row.xpath('./td/a[contains(@href, "client")]/text()').extract_first('')
            link = row.xpath('./td/a/@href').extract_first('')
            yield RowItem(title=title,
                          company_name=company_name,
                          link=link)


def main():
    process = CrawlerProcess(settings={
    "FEEDS": {
        "items.csv": {"format": "csv"},
    }})

    process.crawl(FindJobsSpider)
    process.start()



if __name__ == '__main__':
    main()