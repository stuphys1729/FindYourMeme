# -*- coding: utf-8 -*-
import scrapy

formats = [
    'DrakePosting',# 0
    'scumbag-steve',
    'good-guy-greg',
    'bad-luck-brian',
    'pepe-the-frog',
    'but-thats-none-of-my-business',# 5
    'everyone-loses-their-minds',
    '10-guy',
    'actual-advice-mallard',
    'confession-bear',
    'sudden-clarity-clarence',
    'awkward-moment-seal',
    'seal-of-approval',
    'minor-mistake-marvin',
    'the-rent-is-too-damn-high-jimmy-mcmillan',
    'afraid-to-ask-andy',
    'first-world-problems',
    'pepperidge-farm-remembers',
    'you-know-what-really-grinds-my-gears',
    'matrix-morpheus',
    'that-would-be-great',
    'daily-struggle',
    'kevin-durant-mvp-speech',
    'is-this-a-pigeon',
    'annoyed-picard',
    'do-you-want-ants',
    'ultra-instinct-shaggy'
    ]
#thisRun = 9

class KYMSpider(scrapy.Spider):
    name = "KYMSpider"
    allowed_domains = ['knowyourmeme.com']
    start_urls = ['https://knowyourmeme.com/memes/{}/photos'.format(formats[-1])]
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
