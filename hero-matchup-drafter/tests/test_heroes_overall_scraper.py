import pytest
import sys
from scrapy.http import HtmlResponse

# Add the directory containing your spider to the path
sys.path.append(r'C:/Users/chaaa/Documents/GitHub/dotadrafter/hero-matchup-drafter/scraper_hero_scraper/scraper_hero_scraper/spiders')
from heroes_overall_scraper import Overall_Hero_List_Spider  # Import your spider here

@pytest.fixture
def html_response():
    '''Loads HTML content from a local fixture file for Dota heroes'''
    with open('data/Axe - Counters - DOTABUFF - Dota 2 Stats.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return HtmlResponse(url='https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick&date=7d&rankTier=immortal',
                        body=html_content,
                        encoding='utf-8')

def test_dota_hero_data(html_response):
    '''Tests and asserts the spider's parsing logic on the Dota hero data page.'''
    # Instantiate the spider
    spider = Overall_Hero_List_Spider()
    # Parse the response using the spider's parse method
    results = list(spider.parse(html_response))

    # Assert and check the extracted data
    assert len(results) > 0, "No results parsed. The fixture may be empty or incorrect."

    for hero_data in results:
        # Check for required keys and print which ones are missing or empty
        required_keys = ['Name', 'URL', 'Tier', 'Win Rate', 'Change', 'Pick Rate']
        missing_keys = [key for key in required_keys if key not in hero_data or not hero_data[key]]
        if missing_keys:
            print(f"Missing or empty data for hero: {hero_data.get('Name', 'Unknown')} - Missing keys: {missing_keys}")
        assert not missing_keys, f"Missing keys in hero data: {missing_keys}"

        # Print extracted data for each hero
        print(f"Extracted Data - Hero: {hero_data['Name']}, Tier: {hero_data['Tier']}, Win Rate: {hero_data['Win Rate']}, Change: {hero_data['Change']}, Pick Rate: {hero_data['Pick Rate']}")

