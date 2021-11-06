import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape_mars():
	executable_path = {"executable_path": ChromeDriverManager().install()}
	browser = Browser("chrome", **executable_path, headless=False)

	# Scrape Mars news
	news_url = 'https://redplanetscience.com'
	browser.visit(news_url)

	time.sleep(1)

	news_html = browser.html
	news_soup = BeautifulSoup(news_html, 'html.parser')

	headline = news_soup.find('div', {'class': 'content_title'}).text
	teaser = news_soup.find('div', {'class': 'article_teaser_body'}).text

	# Scrape Mars images
	images_url = 'https://spaceimages-mars.com'
	browser.visit(images_url)

	time.sleep(1)

	images_html = browser.html
	images_soup = BeautifulSoup(images_html, 'html.parser')

	images_path = images_soup.find('img', {'class': 'headerimage fade-in'}).get('src')
	featured_image_url = f'{images_url}/{images_path}'
	featured_image_alt = images_soup.find('h1', {'class': 'media_feature_title'}).text

	# Scrape Mars facts
	facts_url = 'https://galaxyfacts-mars.com'
	browser.visit(facts_url)

	time.sleep(1)

	tables = pd.read_html(facts_url)
	mars_facts_df = tables[0]
	mars_facts_df.columns = mars_facts_df.iloc[0]
	mars_facts_df = mars_facts_df.iloc[1:].reset_index(drop=True)
	mars_html = mars_facts_df.to_html(index=False, index_names=False)

	# Scrape Mars hemispheres
	hemisphere_url = 'https://marshemispheres.com'
	browser.visit(hemisphere_url)

	time.sleep(1)

	hemisphere_html = browser.html
	hemisphere_soup = BeautifulSoup(hemisphere_html,'html.parser')

	results = hemisphere_soup.find_all('div', {'class': 'description'})

	hemisphere_images = []

	for result in results:
		hemisphere_dict = {}
	
		items = result.find('div', {'class': 'description'})
		header = result.find('h3').text
		item_link = result.find('a', {'class': 'itemLink product-item'})['href']
	
		browser.links.find_by_partial_text(header).click()
	
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')
	
		rel_path = soup.find('img', {'class': 'wide-image'})['src']
		abs_path = f'{hemisphere_url}/{rel_path}'
	
		browser.visit(hemisphere_url)
	
		hemisphere_dict['title'] = header
		hemisphere_dict['img_url'] = abs_path
	
		hemisphere_images.append(hemisphere_dict)
	
	mars_info = {
		'news_headline': headline,
		'news_teaser': teaser,
		'mars_image': featured_image_url,
		'mars_alt': featured_image_alt,
		'mars_facts': mars_html,
		'mars_hemisphere': hemisphere_images
	}

	browers.quit()

	return mars_info
	