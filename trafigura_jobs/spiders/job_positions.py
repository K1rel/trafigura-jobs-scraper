from datetime import datetime, timedelta
import re
import scrapy
from scrapy_playwright.page import PageMethod

def parse_posted_date(text):
    final = ""
    if "30+ Days Ago" in text:
        
        posted_date = datetime.now() - timedelta(days=30)
        final = f"Before {posted_date}"
    if "Today" in text:
        posted_date = datetime.now() 
    else:
        
        match = re.search(r"(\d+)\s+Days? Ago", text, re.IGNORECASE)
        if not match:
            return None  

        days_ago = int(match.group(1))
        posted_date = datetime.now() - timedelta(days=days_ago)

    return final if final else  posted_date.strftime("%Y-%m-%d") 

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
                    'title': job.css("a[data-automation-id='jobTitle']::text").get(),
                    'location': job.css("div[data-automation-id='locations'] dd::text").get(),
                    'posted_date': parse_posted_date(job.css("div[data-automation-id='postedOn'] dd::text").get())
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



        
       


