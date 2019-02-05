# -*- coding: utf-8 -*-
import scrapy

formats = ['DrakePosting', 'scumbag-steve', 'good-guy-greg', 'bad-luck-brian', 'pepe-the-frog']
thisRun = 4

class KYMSpider(scrapy.Spider):
    name = "KYMSpider"
    allowed_domains = ['knowyourmeme.com']
    start_urls = ['https://knowyourmeme.com/memes/{}/photos'.format(formats[thisRun])]
    base = 'https://knowyourmeme.com'

    def parse(self, response):
        base = 'http://knowyourmeme.com'
        for item in response.css('.item'):
            imLink = item.xpath('a/@href').extract_first()
            yield response.follow(imLink, self.parseImLink)

        next_page = response.css('.next_page').xpath('@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parseImLink(self, response):

            imLink = response.xpath('//div[@id="photo_wrapper"]').xpath('a/@href').extract_first()
            scraped_imlinks = {
                'image_urls' : [imLink],
            }

            yield scraped_imlinks
