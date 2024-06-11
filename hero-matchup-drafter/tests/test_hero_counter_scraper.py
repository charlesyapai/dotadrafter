'''
This is a test function to do a unit test on the file found in:

scraper_hero_scraper\scraper_hero_scraper\spiders\unit_test_spider.py


To test the scrapy spider function to ensure that it works. 
'''

import pytest
import sys
from scrapy.http import HtmlResponse, Request


sys.path.append(r'C:\Users\chaaa\Documents\GitHub\dotadrafter\hero-matchup-drafter\scraper_hero_scraper\scraper_hero_scraper\spiders')
from unit_test_spider import AxeCountersSpider

@pytest.fixture
def html_response():
    '''Loads HTML content from the file for Axe'''
    with open('data/Axe - Counters - DOTABUFF - Dota 2 Stats.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Create a Scrapy HtmlResponse object
    return HtmlResponse(url='https://www.dotabuff.com/heroes/axe/counters',
                        body=html_content,
                        encoding='utf-8')

def test_axe_counters_print(html_response):
    '''Tests and asserts the unit test to check for the correct css elements being called.
       Checks that the created keys are correct in the created dictionary called "results", and also
       asserts that the correct values are parsed from the HTML. 
    '''
    # Instantiate the spider
    spider = AxeCountersSpider()
    # Parse the response using the spider's parse method
    results = list(spider.parse(html_response))

    # Check the presence of data and print results
    assert 'disadvantages' in results[0], "Disadvantages key is missing"
    assert 'win_rates' in results[0], "Win rates key is missing"
    assert 'matches_played' in results[0], "Matches played key is missing"

    # Print extracted data for checking
    print("Disadvantages:", results[0]['disadvantages'])
    print("Win Rates:", results[0]['win_rates'])
    print("Matches Played:", results[0]['matches_played'])

    # Example: Check if specific hero data is as expected
    assert results[0]['disadvantages']['Timbersaw'] == 3.4911, f"Expected disadvantage for Timbersaw: 4.31, Got: {results[0]['disadvantages']['Timbersaw']}"
    assert results[0]['win_rates']['Timbersaw'] == 52.6658, f"Expected win rate for Timbersaw: 52.93, Got: {results[0]['win_rates']['Timbersaw']}"
    assert results[0]['disadvantages']['Leshrac'] == 3.613, f"Expected win rate for Leshrac: 3.613, Got: {results[0]['win_rates']['Leshrac']}"
    assert results[0]['disadvantages']['Venomancer'] == 3.0722, f"Expected win rate for Venomancer: 3.0722, Got: {results[0]['win_rates']['Venomancer']}"

    assert results[0]['matches_played']['Timbersaw'] == 37493, f"Expected matches played for Timbersaw: 37493, Got: {results[0]['matches_played']['Timbersaw']}"
    assert results[0]['matches_played']['Terrorblade'] == 10730, f"Expected matches played for Terrorblade: 10730, Got: {results[0]['matches_played']['Terrorblade']}"
    assert results[0]['matches_played']['Ogre Magi'] == 70602, f"Expected matches played for Ogre Magi: 70602, Got: {results[0]['matches_played']['Ogre Magi']}"



