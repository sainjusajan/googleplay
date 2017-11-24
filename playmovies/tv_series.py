# -*- coding: utf-8 -*-
import time
import requests
import os
import csv
import traceback
import sys
import json
import random
import sel_utils
from proxy import generateProxy
from bs4 import BeautifulSoup
# Import selenium reqs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains




def getSeriesList(driver):
	'''Returns a list of all the series with their metadata
	tvseries = [
		{'url':'abc.com',
		 'details': 'lorem ipsum',
		 'title': 'GOT', (not yet)
		},
		...
	]
	'''
	time.sleep(random.randint(4,8))
	sel_utils.scrollToBottom(driver)
	tvseries = []
	tvseries_elements = driver.find_elements_by_xpath("//div[@class='id-card-list card-list two-cards']/div")
    # print(movies_elements)
	try:
		for i in tvseries_elements:
			series = {}
			content = i.find_element_by_xpath(".//div")
			url = content.find_element_by_tag_name('a').get_attribute('href')
			details = content.find_element_by_xpath(".//div[@class='details']")
			description_element = details.find_element_by_class_name('description')
			# description = description_element.get_attribute('textContent')
			description = driver.execute_script("return arguments[0].textContent", description_element)
			series['url'] = url
			series['details'] = description
			tvseries.append(series)
	except Exception as e:
		print(e)
	else:
		print(str(len(tvseries)) + " tv series found")
		return tvseries

    

def getSeriesInfo(driver):
	info_container = driver.find_element_by_class_name("info-container")
	poster = info_container.find_element_by_tag_name("img").get_attribute("src")
	print(poster)
	title = info_container.find_element_by_class_name("document-title").text
	print(title)
	rating_text = info_container.find_element_by_xpath(".//div[@class='tiny-star star-rating-non-editable-container']").get_attribute("aria-label")
	rating = rating_text[6:10]
	print(rating)
	n_raters = info_container.find_element_by_class_name("rating-count").text
	print(n_raters)

	left_div = info_container.find_element_by_class_name("left-info")
	genre_element = left_div.find_element_by_tag_name("a")
	genres = {genre_element.text:genre_element.get_attribute('href')}
	release_date = left_div.find_element_by_xpath(".//div").text 

	return poster, title, rating, n_raters, genres, release_date



def getSeasonCost(driver):
	try:
		if len(driver.find_elements_by_class_name("season-buy-button-container"))>0:
			season_container = driver.find_element_by_class_name("season-buy-button-container")
			button = season_container.find_elements_by_tag_name("button")
			cost = button.text
			print("Cost is: {}".format(cost))
			return cost
		else:
			return ""
	except Exception as e:
		return ""



def getSeriesFullDict(driver, series_dict):
	'''
	Returns the full dictionary with series, season, and episodes details
	dict = {
			'title'        : 'GOT',
			'poster'       : 'abc.com',
			'rating'       : '4.9',
			'n_raters'     : '10000',
			'genres'       : ['Drama'], 
			'release_date  : '2010',
			'description'  : 'GOT is awesome',
			'url'          : 'abc.com',
			'genres'       : ['Drama',],
			'seasons':{
				'season 1': {
					'cost': '30$',
					'url': 'abc.com',
					'episodes': 
						{
						'episode1':{
							'name'         : 'Dragonstone', 
                            'cost'         : '1.99$',
							'description'  : 'alksjfdsd ldsfj',
							'poster'       : 'jsdlfjlks',
							'releaseDate'  : '12 Jan 2013',
							'url'          : 'alsdjkf.dslfjk',
						},...
					}
				},...
			}
	}

	'''
	# Goto series page and extract all information from there
	SeriesDict = series_dict
	
	season_elements = driver.find_elements_by_xpath("//div[@class='tv-seasons-container']/div")
	seasons = {}
	for season_element in season_elements:
		# make visible
		driver.execute_script("arguments[0].setAttribute('style','visibility:visible;');",season_element)
		season_title = season_element.get_attribute("data-season-title")

		season = {}
		# season['cost'] = getSeasonCost(driver)
		# season['url'] = series_dict['url'] + '&cdid=' + season_element.get_attribute("data-season-id")
		
		season['cost'] = getSeasonCost(driver)
		season['url']  = series_dict['url'] + '&cdid=' + season_element.get_attribute("data-season-id")
		season['title'] = season_title

		print("Season details: {} {}".format(season['cost'], season['title']))
	

		# Get the episodes for each season
		episodes = {}
		episode_elements = season_element.find_elements_by_xpath(".//div[@class='id-card-list card-list two-cards']/div")
		print("{} episodes found..".format(len(episode_elements)))

		for episode_element in episode_elements:
			episode = {}
			content = episode_element.find_element_by_xpath(".//div")

			url = content.find_element_by_tag_name('a').get_attribute('href')

			cover_element = content.find_element_by_xpath(".//div[@class='cover']")
			cover_image = cover_element.find_element_by_tag_name("img").get_attribute("src")

			details = content.find_element_by_class_name("details")
			description_element = details.find_element_by_class_name('description')
			description = driver.execute_script("return arguments[0].textContent", description_element)

			episode_title = details.find_element_by_class_name("epname-number").text
			
			number_element = details.find_element_by_class_name("title-season-episode-num")
			number = driver.execute_script("return arguments[0].textContent", number_element)
			release_date = details.find_element_by_class_name("subtitle-releasedate").text
			

			reason_set = content.find_element_by_class_name("reason-set")
			if len(reason_set.find_elements_by_class_name("display-price"))>0:
				cost_element = reason_set.find_element_by_class_name("display-price")
				cost = cost_element.text
			else:
				cost = ""

			print(url, cover_image, description, episode_title, number, release_date, cost)

			episode['url'] = url
			episode['cover_image'] = cover_image
			episode['description'] = description
			episode['title'] = episode_title
			episode['release_date'] = release_date
			episode['cost'] = cost
			episodes[episode['title']] = episode

		season['episodes'] = episodes
		seasons[season['title']] = season

	SeriesDict['seasons'] = seasons

	print(SeriesDict.values())
	return SeriesDict





# def getSeasons(driver, series):
# 	seasons_dropdown = driver.find_element_by_xpath("//div[@class='season-selector-dropdown']")
# 	driver.execute_script("arguments[0].setAttribute('style','visibility:visible;');",seasons_dropdown)

# 	season_elements = seasons_dropdown.find_elements_by_xpath(".//div")
# 	seasons = {}
# 	for season in season_elements:
# 		name = season.text
# 		season_id = season.get_attribute('data-season-id')
# 		url = series['url'] + '&cdid=' + season_id
# 		seasons[name] = url
# 	print(seasons)
# 	return seasons




# def getAllEpisodes(driver, season):
# 	print("Scraping all episodes for season")
# 	time.sleep(random.randint(2,4))
# 	episode_elements = driver.find_elements_by_xpath("//div[@class='id-card-list card-list two-cards']/div")
# 	print("{} episodes found..".format(len(episode_elements)))
# 	allEpisodes = {}
# 	try:
# 		for i in episode_elements:
# 			episode = {}
# 			content = i.find_element_by_xpath(".//div")

# 			url = content.find_element_by_tag_name('a').get_attribute('href')

# 			cover_element = content.find_element_by_xpath("//div[@class='cover']")
# 			cover_image = cover_element.find_element_by_tag_name("img").get_attribute("src")

# 			details = content.find_element_by_xpath(".//div[@class='details']")
# 			description_element = details.find_element_by_class_name('description')
# 			description = driver.execute_script("return arguments[0].textContent", description_element)

# 			title = details.find_element_by_xpath(".//span[@class='epname-number']").text
# 			number_element = driver.find_element_by_xpath(".//span[@class='title-season-episode-num']")
# 			number = driver.execute_script("return arguments[0].textContent", number_element)
# 			release_date = details.find_element_by_xpath(".//span[@class='subtitle-releasedate']").text
			

# 			if sel_utils.isPresent(driver, By.XPATH, "//span[@class='movies is-price-tag buy-button-container']/button"):
# 				button = driver.find_element_by_xpath("//span[@class='movies is-price-tag buy-button-container']/button")
# 				cost = button.text
# 			else:
# 				cost = ""

# 			print(url, cover_image, description, title, number, release_date, cost)

# 			episode['url'] = url
# 			episode['cover_image'] = cover_image
# 			episode['description'] = description
# 			episode['title'] = title
# 			episode['release_date'] = release_date
# 			episode['cost'] = cost

# 			allEpisodes[number] = episode
# 		print(allEpisodes)

# 	except Exception as e:
# 		print(e)
# 	else:
# 		print(str(len(allEpisodes)) + " episodes found")
# 		return allEpisodes




