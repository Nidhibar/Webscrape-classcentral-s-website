import scrapy
from scrapy.http import Request


class ClasscentralspiderSpider(scrapy.Spider):
    name = 'classcentralspider'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, subject=None):  # init function to provide cmd arguments
        self.subject = subject

    def parse(self, response):
        if(self.subject):
            subject_url = response.xpath(
                '//a[contains(@title,"' + self.subject + '")]/@href').extract_first()
            absolute_sub_url = response.urljoin(subject_url)
            yield Request(absolute_sub_url, callback=self.parse_subject)

        else:
            self.log('scraping all subjects')
            subjects = response.xpath('//h3/a[1]/@href').extract()
            for sub in subjects:
                absolute_sub_url = response.urljoin(sub)
                yield Request(absolute_sub_url, callback=self.parse_subject)

    def parse_subject(self, response):
        sub_name = response.xpath('//h1/text()').extract_first()
        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        for crse in courses:
            crse_name = crse.xpath(
                './/*[@itemprop="name"]/text()').extract_first()
            crse_url = crse.xpath(
                './/a[@itemprop="url"]/@href').extract_first()
            absolute_crse_url = response.urljoin(crse_url)
            yield{'subject_name': sub_name, 'course_name': crse_name, 'course_url': absolute_crse_url}
        next_pg=response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_pg:
        	absolute_nextpg=response.urljoin(next_pg)
        	yield Request(absolute_nextpg,callback=self.parse_subject)