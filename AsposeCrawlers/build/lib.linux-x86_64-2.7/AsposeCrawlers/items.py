# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SwiftCodeItem(Item):

    code = Field(type='str')
    country = Field(type="str")
    bank = Field(type='str')
    branch_name = Field(default="", type="str")
    post_code = Field(default="", type="str")
    address = Field(default="", type="str")
    city = Field(default="", type="str")
    url = Field(type='str')
    referer_url = Field(type='str')