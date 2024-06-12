#!/bin/bash

# Navigate to the spider directory
cd "/c/Users/chaaa/Documents/GitHub/dotadrafter/hero-matchup-drafter/scraper_hero_scraper/scraper_hero_scraper/spiders"

# Read parameters from the YAML file
date_range=$(yq '.date_range' ../config/params_hero_list_spider.yaml)
rankTier=$(yq '.rankTier' ../config/params_hero_list_spider.yaml)
role_position=$(yq '.role_position' ../config/params_hero_list_spider.yaml)

# Get today's date in YYYYMMDD format
today=$(date +%Y%m%d)

# Define the output file name
output_file="hero_stats_${date_range}_${rankTier}_${role_position}_${today}.csv"

# Run the Scrapy spider
scrapy crawl dota_hero_data -o "../../${output_file}"

# Return to the original directory
cd -

echo "Scrapy spider executed successfully. Data saved in ${output_file}"
