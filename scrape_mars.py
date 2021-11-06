import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_news(browser):
	news_url = 'https://redplanetscience.com'
	browser.visit(news_url)

	time.sleep(1)

	news_html = browser.html
	news_soup = BeautifulSoup(news_html, 'html.parser')

	date = news_soup.find('div', {'class': 'list_date'}).text
	title = news_soup.find('div', {'class': 'content_title'}).text
	teaser = news_soup.find('div', {'class': 'article_teaser_body'}).text

	return date, title, teaser

def scrape_image(browser):
	images_url = 'https://spaceimages-mars.com'
	browser.visit(images_url)

	time.sleep(1)

	images_html = browser.html
	images_soup = BeautifulSoup(images_html, 'html.parser')

	images_path = images_soup.find('img', {'class': 'headerimage fade-in'}).get('src')
	featured_image_url = f'{images_url}/{images_path}'
	
	return featured_image_url

def scrape_facts(browser):
	facts_url = 'https://galaxyfacts-mars.com'
	browser.visit(facts_url)

	time.sleep(1)

	tables = pd.read_html(facts_url)
	tables

	mars_facts_df = tables[0]
	mars_facts_df.columns = mars_facts_df.iloc[0]
	mars_facts_df = mars_facts_df.iloc[1:].reset_index(drop=True)
	mars_facts_df

	return mars_facts_df.to_html(index=False, index_names=False, classes='table table-striped')

def scrape_hemisphere(browser):
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

	return hemisphere_images

def scrape_all():
	executable_path = {"executable_path": ChromeDriverManager().install()}
	browser = Browser("chrome", **executable_path, headless=False)

	news_date, news_headline, news_teaser = mars_news(browser)
	img_urls = scrape_hemisphere(browser)
	
	mars_info = {
		'news_date': 'date',
		'news_headline': 'title',
		'news_teaser': 'teaser',
		'mars_image': scrape_image(browser),
		'mars_facts': scrape_facts(),
		'mars_hemispheres': img_urls	
	}

	browser.quit()

	return mars_info

if __name__ == "__main__":
	print(scrape_all())