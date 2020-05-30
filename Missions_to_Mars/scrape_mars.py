from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    
    # Visit visitcostarica.herokuapp.com
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape news title
    news_title = soup.find_all("div", class_="content_title")[1].text
    news_p = soup.find("div", class_="article_teaser_body").text
    
    browser.quit()
    
    return news_title, news_p

def scrape_featured_image():
    browser = init_browser()

    jpl_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    html = browser.html
    soup = bs(html, "html.parser")

    featured_image_url = 'http://www.jpl.nasa.gov' + soup.find("article").find('a')['data-fancybox-href']
    
    browser.quit()
    
    return featured_image_url


def scrape_mars_weather():
    twitter_url="https://twitter.com/marswxreport?lang=en"
# browser.visit(twitter_url)
    data = requests.get(twitter_url)

    soup = bs(data.text, "html.parser")
    tweets = soup.find_all('div', class_="js-tweet-text-container")

    for tweet in tweets:
        tweet.find('a', class_="twitter-timeline-link u-hidden").decompose()
        if "sol " in tweet.text:
            mars_weather = tweet.text.strip()
            break

    return mars_weather

def scrape_mars_facts():
    fact_url="https://space-facts.com/mars/"
#Use Pandas to scrape the table containing facts about the planet
    fact_table = pd.read_html(fact_url)
    fact_df = fact_table[0]
    fact_df.columns=['Mars','Facts']
    fact_df.columns=['Mars','Facts']
    fact_df.set_index('Mars', inplace=True)
    html_table = fact_df.to_html()
    html_table = html_table.replace('\n', '')
    return html_table


def scrape_mars_hemispheres():
#visit hemisphere website
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(h_url)

#Parsel url with Beautiful Soup
    soup = bs(response.text, 'html.parser')

#Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

#Create empty list for hemisphere urls
    h_image_urls =[]
    hemisphere_main_url = 'https://astrogeology.usgs.gov'

    #browser = init_browser()
    for i in items:
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        #browser.visit(hemisphere_main_url + partial_img_url)
        res = requests.get(hemisphere_main_url + partial_img_url)
        partial_img_html = res.text #browser.html
        soup = bs(partial_img_html, 'html.parser')
        img_url = hemisphere_main_url + soup.find('img', class_='wide-image')['src']
        h_image_urls.append({'title':title,'img_url':img_url})
        
    return h_image_urls

def scrape():
    mars_info = {}
    mars_info['News']  = scrape_info()
    mars_info['Image'] = scrape_featured_image()
    mars_info['Weather'] = scrape_mars_weather()
    mars_info['Facts'] = scrape_mars_facts()
    mars_info['Hemisphere'] = scrape_mars_hemispheres()
    return mars_info



if __name__ == '__main__': 
    print(scrape())