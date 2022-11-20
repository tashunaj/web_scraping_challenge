# Import Splinter, BeautifulSoup, and Pandas
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd 
import datetime as dt 
import time




## > SCRAPE MARS NEWS <

def mars_news(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}


    # Initiate headless driver
    browser = Browser('chrome', **executable_path, headless=True)


    #  NASA website 
    url= 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # HTML Parser. Convert the brpwser html to a soup object and then quit the browser
    html= browser.html 
    news_soup= soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        
        slide_element= news_soup.select_one('ul.item_list li.slide')

      
        news_title=slide_element.find('div', class_= 'content_title').get_text()
        # Get article body
        news_p= slide_element  .find('div', class_='article_teaser_body').get_text()

    except AttributeError:                    
        return None,None

    return news_title, news_p


## > SCRAPE FEATURED IMAGES <

def featured_image(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}


    # Initiate headless driver
    browser = Browser('chrome', **executable_path, headless=True)
    # Visit URL 
    url= 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full_image button
    full_image_elements= browser.find_by_tag('button')[1]
    full_image_elements.click()

    

    # Parse the resulting html with soup
    html=browser.html
    image_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        
        image_url_rel= image_soup.find('img', class_='fancybox-image').get("src")
    
    except AttributeError:
        return None
 
    image_url= f'https://www.jpl.nasa.gov{image_url_rel}'

    return image_url


## > SCRAPE FACTS ABOUT MARS <

def mars_facts():
    executable_path = {'executable_path': ChromeDriverManager().install()}


    # Initiate headless driver
    browser = Browser('chrome', **executable_path, headless=True)
   
    try:
        #  look for first html table in site 
        Mars_df=pd.read_html('https://galaxyfacts-mars.com/')[0]

    # BaseException, catches multiple types of errors
    except BaseException:
        return None
    
   
    Mars_df.columns=['description', 'mars','earth']
    Mars_df.set_index('description', inplace=True)

    #Convert back to HTML format, add bootstrap
    return Mars_df.to_html()


## > SCRAPE HEMISPHERE <

def hemisphere(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}


    # Initiate headless driver
    browser = Browser('chrome', **executable_path, headless=True)
    url='https://marshemispheres.com/'
    browser.visit(url)


    hemisphere_image_urls = []

    img_links= browser.find_by_css("a.product-item img")

    for x in range(len(img_links)):
        hemisphere={}

        # Find elements going to click link 
        browser.find_by_css("a.product-item img")[x].click()

        # Find sample Image link
        sample_image= browser.find_by_text("Sample").first
        hemisphere['img_url']=sample_image['href']

        # Get hemisphere Title
        hemisphere['title']=browser.find_by_css("h2.title").text

        #Add Objects to hemisphere_img_urls list
        hemisphere_image_urls.append(hemisphere)

        # Go Back
        browser.back()
    return hemisphere_image_urls

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}


    # Initiate headless driver
    browser = Browser('chrome', **executable_path, headless=True)


    news_title, news_paragraph= mars_news(browser)
    hemisphere_image_urls=hemisphere(browser)
 
    time.sleep(1)


    #  dictionary 
    data={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data
   
if __name__ == "__main__":
    print(scrape_all())
