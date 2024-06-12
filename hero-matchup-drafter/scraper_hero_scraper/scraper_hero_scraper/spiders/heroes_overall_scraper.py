'''This code is for extracting the urls, and the other statistics of the different dota heroes that I want to interact with.

Fields:

'Name', 'URL', 'Rank', 'Win Rate', 'Change', 'Pick Rate'

To run this spider, use the command:

```bash
scrapy crawl dota_hero_data -o heroes.csv
```

'''
import datetime
import scrapy
import yaml


class Overall_Hero_List_Spider(scrapy.Spider):
    name = 'dota_hero_data'
    
    def __init__(self, *args, **kwargs):
        super(Overall_Hero_List_Spider, self).__init__(*args, **kwargs)
        
        yaml_path = 'C:/Users/chaaa/Documents/GitHub/dotadrafter/hero-matchup-drafter/config/params_hero_list_spider.yaml'
        with open(yaml_path, 'r') as file:
            params = yaml.safe_load(file)
        
        if not params:
            raise ValueError("Parameters not found in the YAML file.")
        
        # Retrieve required parameters from the YAML file
        self.date_range = params['date_range']
        self.rankTier = params['rankTier']
        self.role_position = params['role_position']

        # Construct the URL using parameters from the YAML file
        base_url = 'https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick'
        
        # Set the start URL
        self.start_urls = [f'{base_url}&date={self.date_range}&rankTier={self.rankTier}&position={self.role_position}']


    def parse(self, response):
        self.logger.debug(f"Visited main page: {response.url}")
        base_url = 'https://www.dotabuff.com'
        # Extract data from each hero row on the page
        rows = response.css('tr:has(td)')
        for row in rows:
            name = row.css('a[href*="/heroes/"] div div::text').get()  # Extracting the text within the second div inside the anchor tag
            url = row.css('a[href*="/heroes/"]::attr(href)').get()  # Correct
            tier = row.css('div.tw-bg-violet-600::text').get()  # Extracts the tier if it consistently uses this specific background class
            win_rate = row.css('td:nth-child(3) span:first-child::text').get()  # Assuming the win rate is the first span inside the third td
            change = row.css('td:nth-child(4) span:last-child::text').get()  # Assuming the change is in the last span inside the fourth td
            pick_rate = row.css('td:nth-child(5) span:first-child::text').get()  # Assuming the pick rate is the first span inside the fifth td


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


    def close_spider(self, spider):
        # Get the current date in YYYYMMDD format
        today = datetime.datetime.now().strftime('%Y%m%d')
        # Form the filename with the date of scraping
        file_name = f'hero_stats_{self.date_range}_{self.rankTier}_{self.role_position}_{today}.csv'
        self.df.to_csv(file_name, index=False)
        self.logger.info(f"Saved data to {file_name}")


# class Overall_Hero_List_Spider(scrapy.Spider):
#     name = 'dota_hero_data'
#     start_urls = ['https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick&date=7d&rankTier=immortal']

#     custom_settings = {
#         'FEEDS': {
#             'heroes_data.csv': {
#                 'format': 'csv',
#                 'encoding': 'utf8',
#                 'store_empty': False,
#                 'fields': ['Name', 'URL', 'Tier', 'Win Rate', 'Change', 'Pick Rate'],
#                 'indent': 4,
#             },
#         },
#         'LOG_LEVEL': 'DEBUG'  # Ensuring all debug logs are visible
#     }