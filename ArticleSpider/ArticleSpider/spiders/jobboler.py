# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import ArticleItem, CustomItemLoader



from ArticleSpider.utils.common import get_md5

class JobbolerSpider(scrapy.Spider):
    name = "jobboler"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #
    def parse(self, response):
        # 获取列表页的url,并交给具体的解析函数
        # 获取下一页的url, 并交给 parse(自己???)
        post_nodes = response.css("#archive .post .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            print(image_url)
            print(post_url)
            yield Request(url=parse.urljoin(response.url, post_url), meta={'image_url':image_url}, callback=self.parseDetail)


        #提起下一页的地址
        nexturl = response.css(".next.page-numbers::attr(href)").extract_first("")
        if nexturl:
            yield Request(url=nexturl, callback=self.parse)


    # 解析详情页
    def parseDetail(self, response):

        articleItem = CustomItemLoader()

        image_url = response.meta.get("image_url", "")
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # #date = response.xpath('//*[@id="post-111017"]/div[2]/p/text()').extract()[0].strip().replace('·', '').strip()
        # like = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0]
        # store = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*", store)
        # if match_re:
        #     store = int(match_re.group(1))
        # else:
        #     store = 0
        # comment = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        # match = re.match(".*?(\d+).*", comment)
        # if match:
        #     comment = int(match.group(1))
        # else:
        #     comment = 0
        # content = response.xpath('//div[@class="entry"]').extract()[0]

        # articleItem["title"] = title
        # articleItem["url"] = response.url
        # articleItem["image"] = [image_url]
        # articleItem["url_id"] = get_md5(response.url)

        item_loader = CustomItemLoader(item=ArticleItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('url_id', get_md5(response.url))
        item_loader.add_value('url', response.url)
        item_loader.add_value('image', [image_url])

        articleItem = item_loader.load_item()


        yield  articleItem









