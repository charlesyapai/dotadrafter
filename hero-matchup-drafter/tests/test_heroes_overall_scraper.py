import pytest # type: ignore
import sys
from scrapy.http import HtmlResponse
import datetime
import yaml
from unittest.mock import mock_open, patch, MagicMock
import logging
import pandas as pd

sys.path.append(r'C:/Users/chaaa/Documents/GitHub/dotadrafter/hero-matchup-drafter/scraper_hero_scraper/scraper_hero_scraper/spiders')
from heroes_overall_scraper import Overall_Hero_List_Spider

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


'''
Unit Test 1:
    This check checks the 'parse' method of the Overall_Hero_List_Spider, to ensure that the css selectors are extracting the expected information from the file.

    It uses a fixture of the saved html file saved in 'data\Hero stats - DOTABUFF - Dota 2 Stats.html', to check that the extracted information is correct.

    The assert checks if the output data matches exactly what should be returned, which is a list of dictionaries, each dictionary containing the information for a single dota hero. 
'''

@pytest.fixture
def html_response():
    '''Loads HTML content from a local fixture file for Dota heroes'''
    with open('data\Hero stats - DOTABUFF - Dota 2 Stats.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return HtmlResponse(url='https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick&date=7d&rankTier=immortal',
                        body=html_content,
                        encoding='utf-8')

def test_parse_hero_data(html_response):
    # Create an instance of the spider
    spider = Overall_Hero_List_Spider()
    
    # Store the output from the spider
    results = []
    for item in spider.parse(html_response):
        results.append(item)
    print(results)  # Print results to debug

    # Define the expected results
    expected_results = [
        {'Name': 'Lifestealer', 'URL': 'https://www.dotabuff.com/heroes/lifestealer', 'Tier': 'S', 'Win Rate': '54.96', 'Change': '0.25', 'Pick Rate': '18.87'}, 
        {'Name': 'Enigma', 'URL': 'https://www.dotabuff.com/heroes/enigma', 'Tier': 'S', 'Win Rate': '57.84', 'Change': '4.57', 'Pick Rate': '3.70'}, 
        {'Name': 'Arc Warden', 'URL': 'https://www.dotabuff.com/heroes/arc-warden', 'Tier': 'S', 'Win Rate': '55.20', 'Change': '1.33', 'Pick Rate': '3.17'}, 
        {'Name': 'Axe', 'URL': 'https://www.dotabuff.com/heroes/axe', 'Tier': 'S', 'Win Rate': '51.57', 'Change': '-3.59', 'Pick Rate': '19.10'}, 
        {'Name': 'Night Stalker', 'URL': 'https://www.dotabuff.com/heroes/night-stalker', 'Tier': 'S', 'Win Rate': '53.69', 'Change': '1.65', 'Pick Rate': '11.71'}, 
        {'Name': 'Templar Assassin', 'URL': 'https://www.dotabuff.com/heroes/templar-assassin', 'Tier': 'S', 'Win Rate': '52.23', 'Change': '-0.75', 'Pick Rate': '17.20'}, 
        {'Name': 'Pudge', 'URL': 'https://www.dotabuff.com/heroes/pudge', 'Tier': 'S', 'Win Rate': '51.41', 'Change': '2.86', 'Pick Rate': '31.66'}, 
        {'Name': 'Shadow Fiend', 'URL': 'https://www.dotabuff.com/heroes/shadow-fiend', 'Tier': 'S', 'Win Rate': '51.61', 'Change': '0.67', 'Pick Rate': '25.17'}, 
        {'Name': 'Weaver', 'URL': 'https://www.dotabuff.com/heroes/weaver', 'Tier': 'S', 'Win Rate': '52.69', 'Change': '0.38', 'Pick Rate': '21.91'}, 
        {'Name': 'Dark Willow', 'URL': 'https://www.dotabuff.com/heroes/dark-willow', 'Tier': 'S', 'Win Rate': '53.26', 'Change': '-0.64', 'Pick Rate': '17.66'}, 
        {'Name': 'Shadow Shaman', 'URL': 'https://www.dotabuff.com/heroes/shadow-shaman', 'Tier': 'S', 'Win Rate': '52.19', 'Change': '-3.18', 'Pick Rate': '16.59'}, 
        {'Name': 'Legion Commander', 'URL': 'https://www.dotabuff.com/heroes/legion-commander', 'Tier': 'S', 'Win Rate': '50.99', 'Change': '-0.16', 'Pick Rate': '13.55'}, 
        {'Name': 'Oracle', 'URL': 'https://www.dotabuff.com/heroes/oracle', 'Tier': 'S', 'Win Rate': '53.56', 'Change': '-0.88', 'Pick Rate': '8.47'}, 
        {'Name': 'Visage', 'URL': 'https://www.dotabuff.com/heroes/visage', 'Tier': 'S', 'Win Rate': '54.05', 'Change': '-1.95', 'Pick Rate': '3.80'}, 
        {'Name': 'Witch Doctor', 'URL': 'https://www.dotabuff.com/heroes/witch-doctor', 'Tier': None, 'Win Rate': '52.34', 'Change': '3.68', 'Pick Rate': '18.23'}, 
        {'Name': 'Dark Seer', 'URL': 'https://www.dotabuff.com/heroes/dark-seer', 'Tier': None, 'Win Rate': '53.84', 'Change': '3.15', 'Pick Rate': '7.04'}, 
        {'Name': 'Ursa', 'URL': 'https://www.dotabuff.com/heroes/ursa', 'Tier': None, 'Win Rate': '51.86', 'Change': '-0.23', 'Pick Rate': '17.35'}, 
        {'Name': 'Spirit Breaker', 'URL': 'https://www.dotabuff.com/heroes/spirit-breaker', 'Tier': None, 'Win Rate': '51.74', 'Change': '1.12', 'Pick Rate': '16.23'}, 
        {'Name': 'Leshrac', 'URL': 'https://www.dotabuff.com/heroes/leshrac', 'Tier': None, 'Win Rate': '52.99', 'Change': '-1.11', 'Pick Rate': '8.33'}, 
        {'Name': 'Winter Wyvern', 'URL': 'https://www.dotabuff.com/heroes/winter-wyvern', 'Tier': None, 'Win Rate': '52.94', 'Change': '-0.56', 'Pick Rate': '9.36'}, 
        {'Name': 'Treant Protector', 'URL': 'https://www.dotabuff.com/heroes/treant-protector', 'Tier': None, 'Win Rate': '53.55', 'Change': '-0.83', 'Pick Rate': '6.72'}, 
        {'Name': 'Abaddon', 'URL': 'https://www.dotabuff.com/heroes/abaddon', 'Tier': None, 'Win Rate': '53.06', 'Change': '0.42', 'Pick Rate': '6.73'}, 
        {'Name': 'Brewmaster', 'URL': 'https://www.dotabuff.com/heroes/brewmaster', 'Tier': None, 'Win Rate': '53.40', 'Change': '4.26', 'Pick Rate': '3.09'}, 
        {'Name': 'Chaos Knight', 'URL': 'https://www.dotabuff.com/heroes/chaos-knight', 'Tier': None, 'Win Rate': '52.23', 'Change': '0.25', 'Pick Rate': '11.96'}, 
        {'Name': 'Broodmother', 'URL': 'https://www.dotabuff.com/heroes/broodmother', 'Tier': None, 'Win Rate': '51.92', 'Change': '-0.23', 'Pick Rate': '4.30'}, 
        {'Name': 'Windranger', 'URL': 'https://www.dotabuff.com/heroes/windranger', 'Tier': None, 'Win Rate': '52.31', 'Change': '3.49', 'Pick Rate': '12.75'}, 
        {'Name': 'Venomancer', 'URL': 'https://www.dotabuff.com/heroes/venomancer', 'Tier': None, 'Win Rate': '50.85', 'Change': '-3.41', 'Pick Rate': '19.56'}, 
        {'Name': 'Clockwerk', 'URL': 'https://www.dotabuff.com/heroes/clockwerk', 'Tier': None, 'Win Rate': '51.92', 'Change': '-0.67', 'Pick Rate': '13.88'}, 
        {'Name': 'Elder Titan', 'URL': 'https://www.dotabuff.com/heroes/elder-titan', 'Tier': None, 'Win Rate': '53.47', 'Change': '-2.43', 'Pick Rate': '2.18'}, 
        {'Name': 'Lone Druid', 'URL': 'https://www.dotabuff.com/heroes/lone-druid', 'Tier': None, 'Win Rate': '52.67', 'Change': '-2.57', 'Pick Rate': '2.25'}, 
        {'Name': 'Tiny', 'URL': 'https://www.dotabuff.com/heroes/tiny', 'Tier': None, 'Win Rate': '49.70', 'Change': '-0.94', 'Pick Rate': '22.92'}, 
        {'Name': 'Phoenix', 'URL': 'https://www.dotabuff.com/heroes/phoenix', 'Tier': None, 'Win Rate': '51.01', 'Change': '-2.13', 'Pick Rate': '17.19'}, 
        {'Name': 'Bounty Hunter', 'URL': 'https://www.dotabuff.com/heroes/bounty-hunter', 'Tier': None, 'Win Rate': '52.66', 'Change': '0.24', 'Pick Rate': '6.26'}, 
        {'Name': 'Vengeful Spirit', 'URL': 'https://www.dotabuff.com/heroes/vengeful-spirit', 'Tier': None, 'Win Rate': '51.53', 'Change': '0.51', 'Pick Rate': '17.37'}, 
        {'Name': 'Zeus', 'URL': 'https://www.dotabuff.com/heroes/zeus', 'Tier': None, 'Win Rate': '50.18', 'Change': '-3.84', 'Pick Rate': '17.22'}, 
        {'Name': 'Storm Spirit', 'URL': 'https://www.dotabuff.com/heroes/storm-spirit', 'Tier': None, 'Win Rate': '50.44', 'Change': '-1.79', 'Pick Rate': '16.41'}, 
        {'Name': 'Io', 'URL': 'https://www.dotabuff.com/heroes/io', 'Tier': None, 'Win Rate': '51.27', 'Change': '-1.46', 'Pick Rate': '5.78'}, 
        {'Name': 'Wraith King', 'URL': 'https://www.dotabuff.com/heroes/wraith-king', 'Tier': None, 'Win Rate': '50.43', 'Change': '-0.14', 'Pick Rate': '12.97'}, 
        {'Name': 'Outworld Destroyer', 'URL': 'https://www.dotabuff.com/heroes/outworld-destroyer', 'Tier': None, 'Win Rate': '50.68', 'Change': '3.13', 'Pick Rate': '5.93'}, 
        {'Name': 'Ember Spirit', 'URL': 'https://www.dotabuff.com/heroes/ember-spirit', 'Tier': None, 'Win Rate': '51.48', 'Change': '2.45', 'Pick Rate': '9.50'}, 
        {'Name': 'Marci', 'URL': 'https://www.dotabuff.com/heroes/marci', 'Tier': None, 'Win Rate': '51.27', 'Change': '3.79', 'Pick Rate': '6.81'}, 
        {'Name': 'Meepo', 'URL': 'https://www.dotabuff.com/heroes/meepo', 'Tier': None, 'Win Rate': '49.25', 'Change': '-2.75', 'Pick Rate': '2.99'}, 
        {'Name': 'Troll Warlord', 'URL': 'https://www.dotabuff.com/heroes/troll-warlord', 'Tier': None, 'Win Rate': '51.22', 'Change': '-0.70', 'Pick Rate': '6.67'}, 
        {'Name': 'Lich', 'URL': 'https://www.dotabuff.com/heroes/lich', 'Tier': None, 'Win Rate': '51.13', 'Change': '0.97', 'Pick Rate': '9.05'}, 
        {'Name': 'Underlord', 'URL': 'https://www.dotabuff.com/heroes/underlord', 'Tier': None, 'Win Rate': '51.31', 'Change': '4.24', 'Pick Rate': '6.14'}, 
        {'Name': 'Centaur Warrunner', 'URL': 'https://www.dotabuff.com/heroes/centaur-warrunner', 'Tier': None, 'Win Rate': '50.14', 'Change': '-1.22', 'Pick Rate': '14.07'}, 
        {'Name': 'Undying', 'URL': 'https://www.dotabuff.com/heroes/undying', 'Tier': None, 'Win Rate': '51.01', 'Change': '0.65', 'Pick Rate': '5.88'}, 
        {'Name': 'Rubick', 'URL': 'https://www.dotabuff.com/heroes/rubick', 'Tier': None, 'Win Rate': '49.58', 'Change': '2.97', 'Pick Rate': '18.45'}, 
        {'Name': 'Dragon Knight', 'URL': 'https://www.dotabuff.com/heroes/dragon-knight', 'Tier': None, 'Win Rate': '49.72', 'Change': '-0.40', 'Pick Rate': '13.16'}, 
        {'Name': 'Clinkz', 'URL': 'https://www.dotabuff.com/heroes/clinkz', 'Tier': None, 'Win Rate': '50.48', 'Change': '-0.07', 'Pick Rate': '5.04'}, 
        {'Name': 'Primal Beast', 'URL': 'https://www.dotabuff.com/heroes/primal-beast', 'Tier': None, 'Win Rate': '50.41', 'Change': '4.44', 'Pick Rate': '5.27'}, 
        {'Name': 'Disruptor', 'URL': 'https://www.dotabuff.com/heroes/disruptor', 'Tier': None, 'Win Rate': '49.45', 'Change': '-0.79', 'Pick Rate': '9.49'}, 
        {'Name': 'Phantom Lancer', 'URL': 'https://www.dotabuff.com/heroes/phantom-lancer', 'Tier': None, 'Win Rate': '49.92', 'Change': '2.48', 'Pick Rate': '5.60'}, 
        {'Name': 'Keeper of the Light', 'URL': 'https://www.dotabuff.com/heroes/keeper-of-the-light', 'Tier': None, 'Win Rate': '50.25', 'Change': '-0.83', 'Pick Rate': '3.10'}, 
        {'Name': 'Ogre Magi', 'URL': 'https://www.dotabuff.com/heroes/ogre-magi', 'Tier': None, 'Win Rate': '49.84', 'Change': '1.43', 'Pick Rate': '8.52'}, 
        {'Name': 'Earthshaker', 'URL': 'https://www.dotabuff.com/heroes/earthshaker', 'Tier': None, 'Win Rate': '49.80', 'Change': '3.13', 'Pick Rate': '8.41'}, 
        {'Name': 'Alchemist', 'URL': 'https://www.dotabuff.com/heroes/alchemist', 'Tier': None, 'Win Rate': '50.05', 'Change': '0.10', 'Pick Rate': '3.89'}, 
        {'Name': 'Ancient Apparition', 'URL': 'https://www.dotabuff.com/heroes/ancient-apparition', 'Tier': None, 'Win Rate': '49.68', 'Change': '-1.58', 'Pick Rate': '5.45'}, 
        {'Name': 'Silencer', 'URL': 'https://www.dotabuff.com/heroes/silencer', 'Tier': None, 'Win Rate': '49.20', 'Change': '1.79', 'Pick Rate': '8.11'}, 
        {'Name': 'Hoodwink', 'URL': 'https://www.dotabuff.com/heroes/hoodwink', 'Tier': None, 'Win Rate': '48.63', 'Change': '0.44', 'Pick Rate': '14.00'}, 
        {'Name': 'Naga Siren', 'URL': 'https://www.dotabuff.com/heroes/naga-siren', 'Tier': None, 'Win Rate': '50.05', 'Change': '-1.99', 'Pick Rate': '1.25'}, 
        {'Name': 'Shadow Demon', 'URL': 'https://www.dotabuff.com/heroes/shadow-demon', 'Tier': None, 'Win Rate': '49.83', 'Change': '-0.74', 'Pick Rate': '3.76'}, 
        {'Name': 'Huskar', 'URL': 'https://www.dotabuff.com/heroes/huskar', 'Tier': None, 'Win Rate': '48.48', 'Change': '3.84', 'Pick Rate': '2.65'}, 
        {'Name': 'Skywrath Mage', 'URL': 'https://www.dotabuff.com/heroes/skywrath-mage', 'Tier': None, 'Win Rate': '49.50', 'Change': '1.16', 'Pick Rate': '6.54'}, 
        {'Name': 'Juggernaut', 'URL': 'https://www.dotabuff.com/heroes/juggernaut', 'Tier': None, 'Win Rate': '47.77', 'Change': '-0.70', 'Pick Rate': '14.51'}, 
        {'Name': 'Slardar', 'URL': 'https://www.dotabuff.com/heroes/slardar', 'Tier': None, 'Win Rate': '48.45', 'Change': '-0.18', 'Pick Rate': '10.60'}, 
        {'Name': 'Warlock', 'URL': 'https://www.dotabuff.com/heroes/warlock', 'Tier': None, 'Win Rate': '49.10', 'Change': '-0.36', 'Pick Rate': '7.26'}, 
        {'Name': 'Nyx Assassin', 'URL': 'https://www.dotabuff.com/heroes/nyx-assassin', 'Tier': None, 'Win Rate': '48.01', 'Change': '0.44', 'Pick Rate': '7.44'}, 
        {'Name': 'Sand King', 'URL': 'https://www.dotabuff.com/heroes/sand-king', 'Tier': None, 'Win Rate': '46.99', 'Change': '-8.69', 'Pick Rate': '10.24'}, 
        {'Name': 'Bane', 'URL': 'https://www.dotabuff.com/heroes/bane', 'Tier': None, 'Win Rate': '49.33', 'Change': '2.56', 'Pick Rate': '3.77'}, 
        {'Name': 'Lycan', 'URL': 'https://www.dotabuff.com/heroes/lycan', 'Tier': None, 'Win Rate': '49.36', 'Change': '5.86', 'Pick Rate': '3.02'}, 
        {'Name': 'Earth Spirit', 'URL': 'https://www.dotabuff.com/heroes/earth-spirit', 'Tier': None, 'Win Rate': '49.41', 'Change': '0.58', 'Pick Rate': '4.18'}, 
        {'Name': 'Void Spirit', 'URL': 'https://www.dotabuff.com/heroes/void-spirit', 'Tier': None, 'Win Rate': '48.78', 'Change': '0.30', 'Pick Rate': '9.10'}, 
        {'Name': 'Medusa', 'URL': 'https://www.dotabuff.com/heroes/medusa', 'Tier': None, 'Win Rate': '49.29', 'Change': '-2.54', 'Pick Rate': '2.21'}, 
        {'Name': 'Chen', 'URL': 'https://www.dotabuff.com/heroes/chen', 'Tier': None, 'Win Rate': '49.29', 'Change': '1.29', 'Pick Rate': '0.95'}, 
        {'Name': 'Necrophos', 'URL': 'https://www.dotabuff.com/heroes/necrophos', 'Tier': None, 'Win Rate': '48.32', 'Change': '0.23', 'Pick Rate': '7.82'}, 
        {'Name': 'Lina', 'URL': 'https://www.dotabuff.com/heroes/lina', 'Tier': None, 'Win Rate': '48.34', 'Change': '1.83', 'Pick Rate': '7.95'}, 
        {'Name': 'Puck', 'URL': 'https://www.dotabuff.com/heroes/puck', 'Tier': None, 'Win Rate': '48.33', 'Change': '2.98', 'Pick Rate': '4.69'}, 
        {'Name': 'Monkey King', 'URL': 'https://www.dotabuff.com/heroes/monkey-king', 'Tier': None, 'Win Rate': '48.10', 'Change': '0.99', 'Pick Rate': '9.63'}, 
        {'Name': 'Invoker', 'URL': 'https://www.dotabuff.com/heroes/invoker', 'Tier': None, 'Win Rate': '48.02', 'Change': '3.03', 'Pick Rate': '10.55'}, 
        {'Name': 'Omniknight', 'URL': 'https://www.dotabuff.com/heroes/omniknight', 'Tier': None, 'Win Rate': '48.93', 'Change': '0.46', 'Pick Rate': '1.17'}, 
        {'Name': 'Dawnbreaker', 'URL': 'https://www.dotabuff.com/heroes/dawnbreaker', 'Tier': None, 'Win Rate': '48.64', 'Change': '0.41', 'Pick Rate': '4.38'}, 
        {'Name': 'Faceless Void', 'URL': 'https://www.dotabuff.com/heroes/faceless-void', 'Tier': None, 'Win Rate': '48.09', 'Change': '0.96', 'Pick Rate': '6.78'}, 
        {'Name': 'Crystal Maiden', 'URL': 'https://www.dotabuff.com/heroes/crystal-maiden', 'Tier': None, 'Win Rate': '48.07', 'Change': '0.96', 'Pick Rate': '9.78'}, 
        {'Name': 'Jakiro', 'URL': 'https://www.dotabuff.com/heroes/jakiro', 'Tier': None, 'Win Rate': '48.11', 'Change': '1.00', 'Pick Rate': '8.10'}, 
        {'Name': 'Beastmaster', 'URL': 'https://www.dotabuff.com/heroes/beastmaster', 'Tier': None, 'Win Rate': '48.07', 'Change': '3.90', 'Pick Rate': '6.08'}, 
        {'Name': 'Lion', 'URL': 'https://www.dotabuff.com/heroes/lion', 'Tier': None, 'Win Rate': '47.33', 'Change': '2.39', 'Pick Rate': '11.85'}, 
        {'Name': 'Razor', 'URL': 'https://www.dotabuff.com/heroes/razor', 'Tier': None, 'Win Rate': '47.51', 'Change': '1.92', 'Pick Rate': '6.96'}, 
        {'Name': 'Pugna', 'URL': 'https://www.dotabuff.com/heroes/pugna', 'Tier': None, 'Win Rate': '48.09', 'Change': '2.72', 'Pick Rate': '3.79'}, 
        {'Name': 'Mars', 'URL': 'https://www.dotabuff.com/heroes/mars', 'Tier': None, 'Win Rate': '47.19', 'Change': '3.45', 'Pick Rate': '9.62'}, 
        {'Name': 'Dazzle', 'URL': 'https://www.dotabuff.com/heroes/dazzle', 'Tier': None, 'Win Rate': '47.72', 'Change': '-0.17', 'Pick Rate': '4.44'}, 
        {'Name': 'Slark', 'URL': 'https://www.dotabuff.com/heroes/slark', 'Tier': None, 'Win Rate': '46.66', 'Change': '1.96', 'Pick Rate': '7.42'}, 
        {'Name': 'Sven', 'URL': 'https://www.dotabuff.com/heroes/sven', 'Tier': None, 'Win Rate': '47.68', 'Change': '-1.70', 'Pick Rate': '2.39'}, 
        {'Name': 'Doom', 'URL': 'https://www.dotabuff.com/heroes/doom', 'Tier': None, 'Win Rate': '46.87', 'Change': '3.03', 'Pick Rate': '4.53'}, 
        {'Name': 'Grimstroke', 'URL': 'https://www.dotabuff.com/heroes/grimstroke', 'Tier': None, 'Win Rate': '47.14', 'Change': '-2.25', 'Pick Rate': '5.04'}, 
        {'Name': 'Riki', 'URL': 'https://www.dotabuff.com/heroes/riki', 'Tier': None, 'Win Rate': '46.89', 'Change': '0.19', 'Pick Rate': '2.28'}, 
        {'Name': 'Timbersaw', 'URL': 'https://www.dotabuff.com/heroes/timbersaw', 'Tier': None, 'Win Rate': '45.50', 'Change': '1.28', 'Pick Rate': '8.66'}, 
        {'Name': 'Gyrocopter', 'URL': 'https://www.dotabuff.com/heroes/gyrocopter', 'Tier': None, 'Win Rate': '46.50', 'Change': '-0.67', 'Pick Rate': '5.20'}, 
        {'Name': 'Queen of Pain', 'URL': 'https://www.dotabuff.com/heroes/queen-of-pain', 'Tier': None, 'Win Rate': '46.12', 'Change': '0.46', 'Pick Rate': '6.71'}, 
        {'Name': 'Anti-Mage', 'URL': 'https://www.dotabuff.com/heroes/anti-mage', 'Tier': None, 'Win Rate': '44.68', 'Change': '2.32', 'Pick Rate': '5.22'}, 
        {'Name': 'Bloodseeker', 'URL': 'https://www.dotabuff.com/heroes/bloodseeker', 'Tier': None, 'Win Rate': '46.51', 'Change': '0.02', 'Pick Rate': '1.55'}, 
        {'Name': 'Luna', 'URL': 'https://www.dotabuff.com/heroes/luna', 'Tier': None, 'Win Rate': '46.11', 'Change': '0.88', 'Pick Rate': '4.48'}, 
        {'Name': 'Tinker', 'URL': 'https://www.dotabuff.com/heroes/tinker', 'Tier': None, 'Win Rate': '45.02', 'Change': '0.81', 'Pick Rate': '4.14'}, 
        {'Name': 'Drow Ranger', 'URL': 'https://www.dotabuff.com/heroes/drow-ranger', 'Tier': None, 'Win Rate': '45.87', 'Change': '5.51', 'Pick Rate': '5.03'}, 
        {'Name': 'Tusk', 'URL': 'https://www.dotabuff.com/heroes/tusk', 'Tier': None, 'Win Rate': '46.00', 'Change': '3.11', 'Pick Rate': '4.66'}, 
        {'Name': 'Tidehunter', 'URL': 'https://www.dotabuff.com/heroes/tidehunter', 'Tier': None, 'Win Rate': '46.03', 'Change': '0.23', 'Pick Rate': '3.22'}, 
        {'Name': 'Pangolier', 'URL': 'https://www.dotabuff.com/heroes/pangolier', 'Tier': None, 'Win Rate': '45.80', 'Change': '7.47', 'Pick Rate': '3.65'}, 
        {'Name': 'Batrider', 'URL': 'https://www.dotabuff.com/heroes/batrider', 'Tier': None, 'Win Rate': '45.47', 'Change': '0.32', 'Pick Rate': '3.23'}, 
        {'Name': 'Death Prophet', 'URL': 'https://www.dotabuff.com/heroes/death-prophet', 'Tier': None, 'Win Rate': '45.64', 'Change': '4.71', 'Pick Rate': '2.24'}, 
        {'Name': 'Viper', 'URL': 'https://www.dotabuff.com/heroes/viper', 'Tier': None, 'Win Rate': '44.99', 'Change': '3.17', 'Pick Rate': '3.26'}, 
        {'Name': 'Snapfire', 'URL': 'https://www.dotabuff.com/heroes/snapfire', 'Tier': None, 'Win Rate': '45.21', 'Change': '4.14', 'Pick Rate': '5.57'}, 
        {'Name': 'Muerta', 'URL': 'https://www.dotabuff.com/heroes/muerta', 'Tier': None, 'Win Rate': '45.37', 'Change': '-1.18', 'Pick Rate': '2.62'}, 
        {'Name': 'Magnus', 'URL': 'https://www.dotabuff.com/heroes/magnus', 'Tier': None, 'Win Rate': '44.79', 'Change': '1.01', 'Pick Rate': '6.12'}, 
        {'Name': 'Mirana', 'URL': 'https://www.dotabuff.com/heroes/mirana', 'Tier': None, 'Win Rate': '44.99', 'Change': '0.41', 'Pick Rate': '3.79'}, 
        {'Name': 'Spectre', 'URL': 'https://www.dotabuff.com/heroes/spectre', 'Tier': None, 'Win Rate': '45.03', 'Change': '-0.69', 'Pick Rate': '2.67'}, 
        {'Name': 'Phantom Assassin', 'URL': 'https://www.dotabuff.com/heroes/phantom-assassin', 'Tier': None, 'Win Rate': '44.57', 'Change': '1.72', 'Pick Rate': '3.94'}, 
        {'Name': 'Techies', 'URL': 'https://www.dotabuff.com/heroes/techies', 'Tier': None, 'Win Rate': '44.07', 'Change': '0.19', 'Pick Rate': '6.31'}, 
        {'Name': 'Enchantress', 'URL': 'https://www.dotabuff.com/heroes/enchantress', 'Tier': None, 'Win Rate': '44.19', 'Change': '-0.72', 'Pick Rate': '2.44'}, 
        {'Name': 'Sniper', 'URL': 'https://www.dotabuff.com/heroes/sniper', 'Tier': None, 'Win Rate': '43.42', 'Change': '5.21', 'Pick Rate': '4.52'}, 
        {'Name': 'Kunkka', 'URL': 'https://www.dotabuff.com/heroes/kunkka', 'Tier': None, 'Win Rate': '43.27', 'Change': '3.68', 'Pick Rate': '1.88'}, 
        {'Name': 'Bristleback', 'URL': 'https://www.dotabuff.com/heroes/bristleback', 'Tier': None, 'Win Rate': '42.98', 'Change': '5.40', 'Pick Rate': '1.92'}, 
        {'Name': 'Terrorblade', 'URL': 'https://www.dotabuff.com/heroes/terrorblade', 'Tier': None, 'Win Rate': '42.89', 'Change': '1.99', 'Pick Rate': '2.69'}, 
        {'Name': 'Morphling', 'URL': 'https://www.dotabuff.com/heroes/morphling', 'Tier': None, 'Win Rate': '42.12', 'Change': '2.10', 'Pick Rate': '3.83'}, 
        {'Name': "Nature's Prophet", 'URL': 'https://www.dotabuff.com/heroes/natures-prophet', 'Tier': None, 'Win Rate': '42.04', 'Change': '-0.50', 'Pick Rate': '3.59'}]

    
    # Check that all expected results are in the results
    for expected in expected_results:
        assert any([expected == result for result in results]), f"Expected {expected} not found in results"



'''
Unit Test 2:
    This check simply checks the init to make sure that the parameters file is being called correctly:

    It will simply call the params file directly, and then see if it matches the base_url that is supposed to come out.

    It also ensures that the date is being checked correctly
'''


@pytest.fixture
def mock_good_yaml():
    params = {
        'date_range': '7d',
        'rankTier': 'immortal',
        'role_position': 'core'
    }
    with patch('builtins.open', mock_open(read_data=yaml.dump(params))) as mock_file:
        yield mock_file

@pytest.fixture
def mock_bad_yaml():
    # Simulate missing 'date_range' parameter
    params = {
        'rankTier': 'immortal',
        'role_position': 'core'
    }
    with patch('builtins.open', mock_open(read_data=yaml.dump(params))) as mock_file:
        yield mock_file

def test_yaml_loading_good(mock_good_yaml):
    spider = Overall_Hero_List_Spider()
    assert spider.date_range == '7d'
    assert spider.rankTier == 'immortal'
    assert spider.role_position == 'core'

def test_yaml_loading_bad(mock_bad_yaml):
    with pytest.raises(KeyError):
        spider = Overall_Hero_List_Spider()

def test_file_not_found_error():
    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            spider = Overall_Hero_List_Spider()

def test_url_construction(mock_good_yaml):
    spider = Overall_Hero_List_Spider()
    expected_url = "https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick&date=7d&rankTier=immortal&position=core"
    assert spider.start_urls[0] == expected_url

def test_output_file_creation(mock_good_yaml, mocker):
    mocker.patch('pandas.DataFrame.to_csv')
    spider = Overall_Hero_List_Spider()
    spider.df = MagicMock()  # Assuming `df` is a DataFrame instance in your spider
    spider.close_spider(spider)
    today = datetime.datetime.now().strftime('%Y%m%d')
    expected_filename = f'hero_stats_7d_immortal_core_{today}.csv'
    pd.DataFrame.to_csv.assert_called_once_with(expected_filename, index=False)
