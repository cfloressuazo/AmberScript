import scrapy


class MovieSpider(scrapy.Spider):
    name = "movies"
    start_urls = [
        "https://www.imdb.com/search/title/?groups=top_1000"
    ]

    def parse(self, response):
        links = response.css('h3.lister-item-header a::attr(href)').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_movie_page)

        for href in response.css('div.desc a::attr(href)'):
            yield response.follow(href, self.parse)

    @staticmethod
    def parse_movie_page(response):
        data = {}
        data['title'] = response.css('h1::text').extract_first().strip()
        data['year'] = response.css('#titleYear a::text').extract_first()
        genres = response.xpath(
            "//div[contains(.//h4, 'Genres')]/a/text()").extract()
        data['genre'] = [genre.strip() for genre in genres]
        data['story_line'] = response.css(
            '#titleStoryLine > div:nth-child(3) > p > span').xpath('normalize-space()').extract_first()
        data['description'] = response.css("div.summary_text").xpath('normalize-space()').extract_first()

        yield data

"""
//*[@id="main"]/div/div[4]/a[2]
#main > div > div.desc > a.lister-page-next.next-page

//*[@id="main"]/div/div[4]/a
#main > div > div.desc > a

#titleStoryLine > div:nth-child(3) > p > span
"""