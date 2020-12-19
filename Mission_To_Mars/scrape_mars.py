# importing dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests


def init_browser():
    executable_path = {
        "executable_path": "/Users/sashadahir/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}

    # Mars News URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    title = soup.find_all('div', class_='content_title')[0].text
    p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image to be scraped
    jpl_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(images_url)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_url + relative_image_path

    # Mars facts to be scraped, converted into html table
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Category', 'Values']
    html_table = df.to_html()
    html_table.replace('\n', '')

    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    # Mars hemispheres products data
    all_hemispheres = hemisphere_soup.find('div', class_='collapsible results')
    mars_hemisphere = all_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []

    # Iterate through each hemisphere data
    for x in mars_hemisphere:
        # Collect Title
        hemisphere = x.find('div', class_="description")
        title = hemisphere.h3.text

        # Image collection
        hemisphere_link = hemisphere.a["href"]
        browser.visit(usgs_url + hemisphere_link)

        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        hemisphere_image_urls.append(image_dict)

    # Mars
    mars_dict = {
        "news_title": title,
        "news_p": p,
        "featured_image_url": featured_image_url,
        "fact_table": str(html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
