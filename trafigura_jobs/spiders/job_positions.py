import random
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
            playwright_page_methods= [PageMethod("wait_for_selector","section[data-automation-id='jobResults'] ul[role='list'] > li:first-child"),
                                      PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                                      PageMethod("wait_for_selector", "section[data-automation-id='jobResults'] ul[role='list'] > li:last-child")
                                      ]
         
            )
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        while True:

            for job in response.css("section[data-automation-id='jobResults'] ul[role='list'] > li"):
                yield {
                    'title': job.css("a[data-automation-id='jobTitle']::text").get()
                }

            next_button_selector = "button[data-uxi-element-id='next']"
            next_button = await page.query_selector(next_button_selector)

            if not next_button:
                self.log("No more pages to scrape.")
                break

            await next_button.click()
            await page.wait_for_selector("section[data-automation-id='jobResults'] ul[role='list'] > li")

            
            content = await page.content()
            response = scrapy.http.HtmlResponse(
                url=page.url,
                body=content,
                encoding='utf-8',
                request=response.request
            )


        await page.close()


        


# page = response.meta["playwright_page"]
        # while True:

        #     for job in response.css("section[data-automation-id='jobResults'] ul[role='list'] > li"):
        #         yield {
        #             'title': job.css("a[data-automation-id='jobTitle']::text").get()
        #         }

        #     next_button_selector = "button[data-uxi-element-id='next']"
        #     next_button = await page.query_selector(next_button_selector)

        #     if not next_button:
        #         self.log("No more pages to scrape.")
        #         break

        #     await next_button.click()
        #     await page.wait_for_selector("section[data-automation-id='jobResults'] ul[role='list'] > li")

            
        #     content = await page.content()
        #     response = scrapy.http.HtmlResponse(
        #         url=page.url,
        #         body=content,
        #         encoding='utf-8',
        #         request=response.request
        #     )


        # await page.close()



        
       


