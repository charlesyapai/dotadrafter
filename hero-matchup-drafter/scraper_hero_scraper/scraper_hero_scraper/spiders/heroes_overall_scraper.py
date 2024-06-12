'''This code is for extracting the urls, and the other statistics of the different dota heroes that I want to interact with.

Fields:

'Name', 'URL', 'Rank', 'Win Rate', 'Change', 'Pick Rate'


'''
import scrapy
import pandas as pd

class Overall_Hero_List_Spider(scrapy.Spider):
    name = 'dota_hero_data'
    start_urls = ['https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick&date=7d&rankTier=immortal']

    custom_settings = {
        'FEEDS': {
            'heroes_data.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': ['Name', 'URL', 'Rank', 'Win Rate', 'Change', 'Pick Rate'],
                'indent': 4,
            },
        },
        'LOG_LEVEL': 'DEBUG'  # Ensuring all debug logs are visible
    }

    def parse(self, response):
        self.logger.debug(f"Visited main page: {response.url}")
        base_url = 'https://www.dotabuff.com'
        # Extract data from each hero row on the page
        rows = response.css('tr:has(td)')
        for row in rows:
            name = row.css('a[href*="/heroes/"]::text').get()
            url = row.css('a[href*="/heroes/"]::attr(href)').get()
            tier = row.css('div.tw-bg-violet-600::text').get()
            win_rate = row.css('td:nth-child(3) > div > span::text').get()
            change = row.css('td:nth-child(4) > div > span::text').get()
            pick_rate = row.css('td:nth-child(5) > span::text').get()

            # Initialize full_url either to the concatenated URL or None if url is not found
            full_url = base_url + url if url else None

            hero_data = {
                'Name': name,
                'URL': full_url,
                'Tier': tier,
                'Win Rate': win_rate,
                'Change': change,
                'Pick Rate': pick_rate
            }

            yield hero_data

