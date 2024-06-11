'''
This is a unit test of a scraper.
It will use Pytest to execute the test code 

It will draw from the saved html page to 
'''

import scrapy

class AxeCountersSpider(scrapy.Spider):
    name = 'axe_counters'
    start_urls = ['https://www.dotabuff.com/heroes/axe/counters']

    def parse(self, target_response):
        disadvantages = {}
        win_rates = {}
        matches_played = {}

        for row in target_response.css('table.sortable tbody tr'):
            hero_name = row.css('td.cell-xlarge a::text').get()
            disadvantage = row.css('td:nth-child(3)::attr(data-value)').get()
            win_rate = row.css('td:nth-child(4)::attr(data-value)').get()
            matches = row.css('td:nth-child(5)::attr(data-value)').get()

            disadvantages[hero_name] = float(disadvantage) if disadvantage else 0.0
            win_rates[hero_name] = float(win_rate) if win_rate else 0.0
            matches_played[hero_name] = int(matches.replace(',', '')) if matches else 0
            

        yield {
            'disadvantages': disadvantages,
            'win_rates': win_rates,
            'matches_played': matches_played
        }