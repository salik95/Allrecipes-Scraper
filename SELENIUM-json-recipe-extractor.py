import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

data = {}

driver = webdriver.Chrome()
categ_name = 'macaroni-and-cheese'
data[categ_name] = []

with open('JSON Recipe URL/' + categ_name +'.json') as jsonfile:
	url_list = json.load(jsonfile)[categ_name]
	print('Total enteries: ', len(url_list))
	print('======================')
	for index, item in enumerate(url_list):
		print('Entry Number ', index+1)
		print('----------------------')
		while 1:
			try:
				driver.get(item)
				break
			except TimeoutException as ex:
				continue
		rest_data = {}
		
		try:
			recipe_name = driver.find_element_by_css_selector('[id = "recipe-main-content"]').text
		except:
			recipe_name = 'N/A'
			continue
		rest_data['Recipe Name'] = recipe_name

		try:
			categories_raw = driver.find_elements_by_css_selector('ol.breadcrumbs li a span.toggle-similar__title')
			categories = []
			for cat in categories_raw:
				categories.append(cat.text)
		except:
			categories = "N/A"
		rest_data['Recipe Tags'] = categories

		time.sleep(3)

		nutritional_information = {}
		nutritions = []
		try:
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
			driver.refresh()
		time.sleep(4)

		try:
			ingredients_raw = driver.find_elements_by_css_selector('[itemprop="recipeIngredient"]')
			ingredients = []
			for item in ingredients_raw:
				ingredients.append(item.text.strip())
		except:
			ingredients = 'N/A'
		rest_data['Ingredients'] = ingredients

		try:
			servings = driver.find_element_by_css_selector('[id="servings-button"] [ng-bind="adjustedServings"]').text
		except:
			servings = 'N/A'
		rest_data['Servings'] = servings

		try:
			directions_raw = driver.find_elements_by_css_selector('[itemprop="recipeInstructions"] .recipe-directions__list--item')
			directions = []
			for item in directions_raw:
				directions.append(item.text)
		except:
			directions = 'N/A'
		rest_data['Directions'] = directions

		try:
			if 'itemprop="prepTime"' in driver.find_element_by_css_selector('ul.prepTime').get_attribute('innerHTML'):
				directions_prep_time = driver.find_element_by_css_selector('[itemprop="prepTime"]').text
			else:
				directions_prep_time = 'N/A'
		except:
			directions_prep_time = 'N/A'
		try:
			if 'itemprop="cookTime"' in driver.find_element_by_css_selector('ul.prepTime').get_attribute('innerHTML'):
				directions_cook_time = driver.find_element_by_css_selector('[itemprop="cookTime"]').text
			else:
				directions_cook_time = 'N/A'
		except:
			directions_cook_time = 'N/A'
		try:
			if 'itemprop="totalTime"' in driver.find_element_by_css_selector('ul.prepTime').get_attribute('innerHTML'):
				directions_readyin_time = driver.find_element_by_css_selector('[itemprop="totalTime"]').text
			else:
				directions_readyin_time = 'N/A'
		except:
			directions_readyin_time = 'N/A'
		time_required_to_cook = {'Prep Time':directions_prep_time, 'Cook Time':directions_cook_time, 'Ready In Time':directions_readyin_time}
		rest_data['Time Required to Cook'] = time_required_to_cook

		try:
			chef_name = driver.find_element_by_css_selector('.submitter__name').text
		except:
			chef_name = 'N/A'
		rest_data['Chef Name'] = chef_name

		try:
			chef_remarks = driver.find_element_by_css_selector('.submitter__description').text
		except:
			chef_remarks = 'N/A'
		rest_data['Chef Remarks'] = chef_remarks

		try:
			total_ratings = driver.find_element_by_css_selector('[id="reviews"] ol li .helpful-header').text
		except:
			total_ratings = 'N/A'
		try:
			star_ratings_raw = driver.find_elements_by_css_selector('[id="reviews"] ol li div')
			star_ratings = {}
			for item in star_ratings_raw:
				if 'loved it' in item.get_attribute('title'):
					star_ratings['5 stars (cooks loved it!)'] = item.get_attribute('title').split(' ')[0]
				elif 'liked it' in item.get_attribute('title'):
					star_ratings['4 stars (cooks liked it!)'] = item.get_attribute('title').split(' ')[0]
				elif 'it was OK' in item.get_attribute('title'):
					star_ratings['3 stars (cooks thought it was OK)'] = item.get_attribute('title').split(' ')[0]
				elif 'didn\'t like it' in item.get_attribute('title'):
					star_ratings['2 stars (cooks didn\'t like it)'] = item.get_attribute('title').split(' ')[0]
				elif 'couldn\'t eat it' in item.get_attribute('title'):
					star_ratings['1 star (cooks couldn\'t eat it)'] = item.get_attribute('title').split(' ')[0]
		except:
			star_ratings = 'N/A'
		ratings = {'Total Number of Ratings' : total_ratings.split(" ")[0], 'Cook Ratings' : star_ratings}
		rest_data['Ratings'] = ratings

		rest_data['Recipe URL'] = driver.current_url
		print(rest_data['Recipe Name'])
		print('----------------------')
		data[categ_name].append(rest_data)

with open(categ_name + '.json', 'w') as fp:
	json.dump(data, fp)