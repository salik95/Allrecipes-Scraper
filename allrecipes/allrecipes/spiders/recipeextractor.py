# -*- coding: utf-8 -*-
import scrapy
import locale
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http.request import Request
from selenium import webdriver

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 

driver = webdriver.Chrome()

recipe_url = []

category_name = 'bread'

data = {}
data[category_name] = []

class RecipeextractorSpider(scrapy.Spider):
	name = 'recipeextractor'
	start_urls = recipe_url

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open('JSON Recipe URL/'+ category_name +'.json') as jsonfile:
			for item in json.load(jsonfile)[category_name]:
				recipe_url.append(item)

	def parse(self, response):
		rest_data = {}
		try:
			recipe_name = response.css('[id = "recipe-main-content"]::text').extract_first()
		except:
			recipe_name = 'N/A'
			return
		rest_data['Recipe Name'] = recipe_name

		try:
			categories_raw = response.css('ol.breadcrumbs li a span.toggle-similar__title::text').extract()
			categories = []
			for cat in categories_raw:
				categories.append(cat.strip())
		except:
			categories = "N/A"
		rest_data['Recipe Tags'] = categories

		nutritional_information = {}
		nutritions = []
		try:
			driver.get(response.url)
			driver.find_element_by_class_name('see-full-nutrition').click()
			driver.implicitly_wait(50)
			nutrition_raw = driver.find_elements_by_css_selector('div.recipe-nutrition div.nutrition-body div.nutrition-row')
			for nu in nutrition_raw:
				try:
					nu_name = nu.find_element_by_css_selector('.nutrient-name').text
					try:
						nu_value = nu_name.split(":")[1].strip()
					except:
						nu_value = '-'
					nu_name = nu_name.split(":")[0].strip()
				except:
					nu_name = 'None'
					nu_value = 'None'
				try:
					if "daily-value" in nu.get_attribute('innerHTML'):
						nu_daily_value = nu.find_element_by_css_selector('.daily-value').text
					else:
						nu_daily_value = 'None'
				except:
					nu_daily_value = 'None'
				nutritions.append([nu_name, nu_value, nu_daily_value])
		except:
			nutritions = 'N/A'
		try:
			cals = driver.find_element_by_css_selector('[id = "nutrition-button"] span.calorie-count span').text
		except:
			cals = 'N/A'
		nutritional_information['calories'] = cals
		nutritional_information['nutritions'] = nutritions
		rest_data['Nutritional Information'] = nutritional_information
		try:
			driver.find_element_by_css_selector("div.ngdialog-header .close-button").click()
		except:
			pass

		try:
			ingredients_raw = response.css('[itemprop="recipeIngredient"]::text').extract()
			ingredients = []
			for ingr in ingredients_raw:
				ingredients.append(ingr.strip())
		except:
			ingredients = 'N/A'
		rest_data['Ingredients'] = ingredients

		try:
			servings = response.css('[id="servings-button"] [ng-bind="adjustedServings"]::text').extract_first()
		except:
			servings = 'N/A'
		rest_data['Servings'] = servings

		try:
			directions_raw = response.css('[itemprop="recipeInstructions"] .recipe-directions__list--item::text').extract()
			directions = []
			for dirc in directions_raw:
				directions.append(dirc.strip())
		except:
			directions = 'N/A'
		rest_data['Directions'] = directions

		try:
			directions_prep_time = "".join(response.css('[itemprop="prepTime"] *::text').extract()).strip()
		except:
			directions_prep_time = 'N/A'

		try:
			directions_cook_time = "".join(response.css('[itemprop="cookTime"] *::text').extract()).strip()
		except:
			directions_cook_time = 'N/A'

		try:			
			directions_readyin_time = "".join(response.css('[itemprop="totalTime"] *::text').extract()).strip()
		except:
			directions_readyin_time = 'N/A'

		time_required_to_cook = {'Prep Time':directions_prep_time, 'Cook Time':directions_cook_time, 'Ready In Time':directions_readyin_time}
		rest_data['Time Required to Cook'] = time_required_to_cook

		try:
			chef_name = response.css('.submitter__name::text').extract_first().strip()
		except:
			chef_name = 'N/A'
		rest_data['Chef Name'] = chef_name

		try:
			chef_remarks = response.css('.submitter__description::text').extract_first().strip()
		except:
			chef_remarks = 'N/A'
		rest_data['Chef Remarks'] = chef_remarks

		try:
			total_ratings = response.css('[id="reviews"] ol li .helpful-header::text').extract_first()
		except:
			total_ratings = 'N/A'
		try:
			star_ratings_raw = response.css('[id="reviews"] ol li div::attr(title)').extract()
			star_ratings = {}
			for item in star_ratings_raw:
				if 'loved it' in item:
					star_ratings['5 stars (cooks loved it!)'] = item.split(' ')[0]
				elif 'liked it' in item:
					star_ratings['4 stars (cooks liked it!)'] = item.split(' ')[0]
				elif 'it was OK' in item:
					star_ratings['3 stars (cooks thought it was OK)'] = item.split(' ')[0]
				elif 'didn\'t like it' in item:
					star_ratings['2 stars (cooks didn\'t like it)'] = item.split(' ')[0]
				elif 'couldn\'t eat it' in item:
					star_ratings['1 star (cooks couldn\'t eat it)'] = item.split(' ')[0]
		except:
			star_ratings = 'N/A'
		ratings = {'Total Number of Ratings' : total_ratings.split(" ")[0], 'Cook Ratings' : star_ratings}
		rest_data['Ratings'] = ratings

		rest_data['Recipe URL'] = response.url
		print('=============================')
		print(rest_data)
		print('=============================')
		data.append(rest_data)

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		with open(category_name + '.json', 'w') as fp:
			json.dump(data, fp)
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')