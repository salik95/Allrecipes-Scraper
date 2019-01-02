import csv
from selenium import webdriver
import time
import json

dishes = []

driver = webdriver.Chrome()
# Give category name in the get function below, and scraper will get all the recipes in the categor and produce a JSON file.
driver.get('https://www.allrecipes.com/recipes/17031/side-dish/sauces-and-condiments/')

lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
prev_len = lenOfPage
current_position = 1000
checker = 0
while 1:
	try:
		more_results = driver.find_element_by_id('btnMoreResults')
		more_results.click()
		current_position = current_position + lenOfPage
	except:
		more_results = None
		
	lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	driver.execute_script("window.scrollTo(0, " + str(current_position)+ ")")
	current_position = lenOfPage
	time.sleep(5)
	lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	
	if prev_len == lenOfPage:
		checker = checker + 1
	
	if prev_len != lenOfPage:
		prev_len = lenOfPage
		checker = 0

	if checker > 12 and checker < 25:
		driver.execute_script("window.scrollTo(0, " + str(current_position-1000)+ ")")

	if checker > 25 and checker < 40:
		driver.execute_script("window.scrollTo(0, " + str(current_position-5000)+ ")")

	if checker > 40 and checker < 49:
		driver.execute_script("window.scrollTo(0, " + str(0)+ ")")

	if checker > 50:
		break
	print(checker)

while 1:
	try:
		current_dishes = driver.find_elements_by_css_selector('article.fixed-recipe-card div.fixed-recipe-card__info a')
		for item in current_dishes:
			if 'https://www.allrecipes.com/recipe' in item.get_attribute('href'):
				dishes.append(item.get_attribute('href').split('?')[0])
		break
	except:
		continue
print(len(set(dishes)))
# Change the json file name here
with open('sauces-and-condiments.json', 'w') as fp:
	json.dump(list(set(dishes)), fp)
