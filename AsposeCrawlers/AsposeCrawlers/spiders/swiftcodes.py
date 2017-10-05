from scrapy import Spider
from scrapy import  Request
import copy

class SwiftCodes(Spider):
    name = 'swiftcodes'
    start_url = 'https://www.swiftcodes.info/'
    custom_settings = {'DOWNLOAD_DELAY': 10,
                       'CONCURRENT_REQUESTS': 30,
                       'CONCURRENT_REQUESTS_PER_IP': 10}

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_home_page)

    def parse_home_page(self, response):
        alphabet_links = response.css('.alphabets a')
        for link in alphabet_links:
            alphabet =  link.xpath('text()').extract()[0]
            url =  response.urljoin(link.xpath('@href').extract()[0])

            meta = dict()
            meta['initial'] = alphabet
            yield Request(url=url, callback=self.parse_country_page,
                          meta=meta)
            return

    def parse_country_page(self, response):
        countries = response.css('.country a')
        for country in countries:
            country_name =  country.xpath('text()').extract()[0]
            url =  response.urljoin(country.xpath('@href').extract()[0])

            meta = copy.deepcopy(response.meta)
            meta['country'] = country_name
            yield Request(url=url, callback=self.parse_country_page,
                          meta=meta)
            return

    def parse_banks(self, response):


        #Pagination
        next_page = response.css('.next>a').xpath('@href').extract()
        if next_page:
            url = response.urljoin(next_page)

            meta = copy.deepcopy(response.meta)
            yield Request(url=url, meta=meta, callback=self.parse_banks)