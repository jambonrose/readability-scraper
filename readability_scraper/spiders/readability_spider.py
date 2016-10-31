import scrapy


class ReadabilitySpider(scrapy.Spider):
    name = "readability"

    login_url = 'https://www.readability.com/login/'
    reading_list_url = 'https://www.readability.com/reading-list?page={0}'
    archive_list_url = (
        'https://www.readability.com/reading-list/archives?page={0}'
    )

    # Utility Functions

    def make_readability_list_link(self, number=1):
        return self.reading_list_url.format(number)

    def make_readability_archive_link(self, number=1):
        return self.archive_list_url.format(number)

    def get_page_number_from_url(self, url):
        return int(url.split('=')[1])

    def make_page_json_name(self, url):
        current_page_number = self.get_page_number_from_url(url)
        if 'archive' in url:
            return 'archive_page_{}_links'.format(current_page_number)
        else:
            return 'page_{}_links'.format(current_page_number)

    def get_next_page_link(self, response):
        next_page_query = (
            response
            .xpath('//a[contains(@class, "page-older")]/@href')
            .extract_first()
        )
        if next_page_query is not None:
            page_number = self.get_page_number_from_url(next_page_query)
            if 'archive' in response.url:
                return self.make_readability_archive_link(page_number)
            else:
                return self.make_readability_list_link(page_number)
        return None

    # Spider Functionality

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.submit_login_form)

    def submit_login_form(self, response):
        # login to response form
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'username': self.username,
                'password': self.password,
            },
            callback=self.start_crawl,
        )

    def start_crawl(self, response):
        yield scrapy.Request(self.make_readability_list_link())
        yield scrapy.Request(self.make_readability_archive_link())

    def parse(self, response):
        reading_list = (
            response
            .xpath('//a[contains(@class, "article-origin")]/@href')
            .extract()
        )
        yield {
            self.make_page_json_name(response.url): reading_list,
        }
        next_page_url = self.get_next_page_link(response)
        if next_page_url is not None:
            yield scrapy.Request(next_page_url)
