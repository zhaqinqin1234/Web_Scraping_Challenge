from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import os
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # initiate browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    url ="https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")
    # Retrieve latest elements that contain title and paragraph
    slide = soup.select_one('li.slide')
    news_title = slide.find("div", class_="content_title").get_text()
    news_para= slide.find("div", class_="article_teaser_body").get_text()
    mars["news_title"] = news_title
    mars["news_para"] = news_para

    # featured image infor
    i_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(i_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    img_soup = bs(html, 'html.parser')
    imag = img_soup.find("figure", class_="lede").a['href']
    img_url = f'https://www.jpl.nasa.gov{imag}'
    mars["img_url"]= img_url

    # Mars facts
    url ="https://space-facts.com/mars/"
    browser.visit(url)

    mars_table = pd.read_html(url)[0]
    mars_table.columns=['Description', 'Value']
    mars_table.set_index('Description', inplace=True)
    mars["fact"]=mars_table.to_html(classes="table table-striped")
    


    # hemisphere infor
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(1)
    hemi_title_img =[]
    # get a litst of all the hemispheres
    links = browser.find_by_css("a.product-item h3")

# loop through the links, click the links and sample anchor and retrun href
    for i in range(len(links)):
        hemisphere ={}
        browser.find_by_css("a.product-item h3")[i].click()
        hemisphere['img_url']=browser.find_link_by_text('Sample').first['href']
        hemisphere['img_title']=browser.find_by_css("h2.title").text
        
        #Append hemisphere dictionay to hemi list
        hemi_title_img.append(hemisphere)
        # navigate backwards
        browser.back()

    mars["hemi_title_img"] = hemi_title_img

    return mars

  
