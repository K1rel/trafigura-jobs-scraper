from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod

class JobPositionsSpider(scrapy.Spider):
    name = 'job_positions'
    start_urls = ['https://trafigura.wd3.myworkdayjobs.com/en-US/TrafiguraCareerSite/jobs']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], meta=dict(
            playwright=True,
            playwright_include_page=True, 
            playwright_page_methods=[
                PageMethod("wait_for_selector", "section[data-automation-id='jobResults'] ul[role='list']"),
                
            ]
        ))

    async def parse(self, response):
        # page = response.meta["playwright_page"]
        # await page.screenshot(path="example.png", full_page=True)
        # await page.close()
        for job in response.css("section[data-automation-id='jobResults'] ul[role='list'] > li"):
            yield {
                'title': job.css("a[data-automation-id='jobTitle']::text").get()
            }
