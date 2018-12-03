# -*- coding: utf-8 -*-
import scrapy


class ScumbagSteveSpider(scrapy.Spider):
    name = 'scumbagSteve'
    allowed_domains = ['knowyourmeme.com']
    start_urls = ['https://knowyourmeme.com/memes/scumbag-steve/photos']
    base = 'https://knowyourmeme.com'

    def parse(self, response):
        base = 'http://knowyourmeme.com'
        for item in response.css('.item'):
            imLink = item.xpath('a/@href').extract_first()
            yield response.follow(imLink, self.parseImLink)


    def parseImLink(self, response):

            imLink = response.xpath('//div[@id="photo_wrapper"]').xpath('a/@href').extract_first()
            scraped_imlinks = {
                'image_urls' : [imLink],
            }

            yield scraped_imlinks
