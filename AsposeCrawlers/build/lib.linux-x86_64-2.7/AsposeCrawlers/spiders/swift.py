from scrapy import Spider
from scrapy import  Request
import copy

from AsposeCrawlers.items import SwiftCodeItem

class SwiftCodes(Spider):
    name = 'theswiftcodes'
    start_url = 'https://www.theswiftcodes.com/'
    custom_settings = {'DOWNLOAD_DELAY': 10,
                       'CONCURRENT_REQUESTS': 30,
                       'CONCURRENT_REQUESTS_PER_IP': 10,
                       'FEED_URI': 'swift.json'
                       }

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_home_page)

    def parse_home_page(self, response):
        alphabet_links = response.css('.alphabets a')
        for link in alphabet_links:
            alphabet =  link.xpath('text()').extract()[0]
            url =  response.urljoin(link.xpath('@href').extract()[0])
            if 'iban' in url:
                continue

            meta = dict()
            meta['initial'] = alphabet
            yield Request(url=url, callback=self.parse_country_page,
                          meta=meta)

    def parse_country_page(self, response):
        countries = response.css('.country a')
        for country in countries:
            country_name =  country.xpath('text()').extract()[0]
            url =  response.urljoin(country.xpath('@href').extract()[0])

            meta = copy.deepcopy(response.meta)
            meta['country'] = country_name
            yield Request(url=url, callback=self.parse_banks,
                          meta=meta)

    def parse_banks(self, response):

        swift_code_links = response.css('.swift a')
        for link in swift_code_links:
            link = response.urljoin(link.xpath('@href').extract()[0])

            meta = copy.deepcopy(response.meta)
            meta['referer_url'] = response.url
            yield Request(url=link, meta=meta,
                          callback=self.parse_swift_code)

        # Pagination
        next_page = response.css('.next>a').xpath('@href').extract()
        if next_page:
            url = response.urljoin(next_page[0])

            meta = copy.deepcopy(response.meta)
            yield Request(url=url, meta=meta, callback=self.parse_banks)

    def parse_swift_code(self, response):

        branch_name = response.xpath('.//*[@id="swift"][1]//tr[4]//td[2]//text()').extract()
        post_code = response.xpath('.//*[@id="swift"][1]//tr[7]//td[2]//text()').extract()
        address = response.xpath('.//*[@id="swift"][1]//tr[5]//td[2]//text()').extract()

        item = SwiftCodeItem()
        item['code'] = ''.join(response.xpath('.//*[@id="swift"][1]//tr[2]//td[2]//text()').extract()).strip()
        item['url'] = response.url
        item['referer_url'] = response.meta['referer_url']
        item['country'] = response.meta['country']
        item['bank'] = response.xpath('.//*[@id="swift"][1]//tr[3]//td[2]//text()').extract()[0].strip()
        item['city'] = response.xpath('.//*[@id="swift"][1]//tr[6]//td[2]//text()').extract()[0].strip()
        item['branch_name'] = branch_name[0].strip() if branch_name else  ''
        item['post_code'] = post_code[0].strip() if post_code else ''
        item['address'] = address[0].strip() if address else ''
        yield item

