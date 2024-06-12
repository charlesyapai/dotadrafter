'''This code is for actually scraping, with logging statements included.'''
import scrapy
import yaml

class DotaHeroDataSpider(scrapy.Spider):
    name = 'dota_hero_data'

    def start_requests(self):
        # Load hero URLs from the YAML file
        with open('hero_urls.yaml', 'r') as file:
            hero_urls = yaml.safe_load(file)

        for url in hero_urls:
            yield scrapy.Request(url=url + '/counters', callback=self.parse_hero)

    def parse_hero(self, response):
        hero_name = response.url.split('/')[-2]
        self.log(f'Starting to scrape data for {hero_name}', level=scrapy.log.INFO)

        disadvantages = {}
        win_rates = {}
        matches_played = {}

        for row in response.css('table.sortable tbody tr'):
            opponent_hero_name = row.css('td.cell-xlarge a::text').get()
            disadvantage = row.css('td:nth-child(3)::attr(data-value)').get()
            win_rate = row.css('td:nth-child(4)::attr(data-value)').get()
            matches = row.css('td:nth-child(5)::attr(data-value)').get()

            disadvantages[opponent_hero_name] = float(disadvantage) if disadvantage else 0.0
            win_rates[opponent_hero_name] = float(win_rate) if win_rate else 0.0
            matches_played[opponent_hero_name] = int(matches.replace(',', '')) if matches else 0

        self.log(f'Finished scraping data for {hero_name}', level=scrapy.log.INFO)

        yield {
            'hero': hero_name,
            'disadvantages': disadvantages,
            'win_rates': win_rates,
            'matches_played': matches_played
        }
