from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": r"\Users\z0042xeh\.wdm\drivers\chromedriver\win32\96.0.4664.45\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_img(search_url):
    # Retrieve page with the requests module
    response = requests.get(search_url)
    # create soup object
    soup = bs(response.text, "html5lib")
    # store high-res img URL in variable 'hem_img_url' & then add to the 'hem_url' to create a complete URL
    hem_img_url = soup.find('img', class_='wide-image')['src']
    final_img_url = hem_url + hem_img_url
    # store the image_url information into dictionary
    title_img_dicts['image_url'] = final_img_url
    
    return (title_img_dicts['image_url'])
            
            
def dict_to_list(dict):
    new_dict = {}
    
    copy_dict = dict.copy()
    new_dict.update(copy_dict)
    
    return new_dict

######################################## News ##########################################################
def scrape_data():
    browser = init_browser()
    news_url = "https://redplanetscience.com/"

    # setup browser for each url
    browser.visit(news_url)

    time.sleep(1)
    
    #Scrape page
    news_html = browser.html
    news_soup = bs(news_html, "lxml")

    # Get most recent news stories and assign to variable
    news_title = news_soup.find('div', 'content_title').text
    print(news_title)

    # Get most recent news story article text and assign to variable
    news_p = news_soup.find('div', 'article_teaser_body').text
    print(news_p)
####################################### Featured Image #################################################

    # URL to Mars Space Images
    image_url = "https://spaceimages-mars.com/"

    # setup browser for each url
    browser.visit(image_url)

    time.sleep(1)

    image_html = browser.html
    image_soup = bs(image_html, "lxml")

    # Locate the featured image using image_soup(bs)
    featured_image = image_soup.find("img", class_="headerimage fade-in")['src']

    # Create a url out of the url for the index.html & the featured image location
    featured_image_url = image_url + featured_image
    print(featured_image_url)

####################################### Facts ###########################################################

    facts_url = 'https://galaxyfacts-mars.com'

    # use pandas to read url for mars facts
    facts_table = pd.read_html(facts_url)
    # convert table into a pandas table to make easier to read
    facts_df = facts_table[0]
    # save the facts_tab as .html doc & save into variable for final results at end of scrape function
    html_table = facts_df.to_html('templates/facts_tab_html.html')

####################################### Hemisphere ########################################################

    hem_url = 'https://marshemispheres.com/'

    browser.visit(hem_url)

    time.sleep(1)
    
    hem_html = browser.html
    hem_soup = bs(hem_html, "lxml")

    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys `img_url` and `title`.

    # The location of all img and title information that's needed
    img_containers = hem_soup.find_all('div', class_='item')

    # list to hold the 'thumb' img reference links
    img_url = []

    # dictionary that holds both the title information & full url to img
    title_img_dicts = {}

    # list that will hold each dictionary of title and full img url
    hemisphere_img_urls = []

    # for loop to go through each of the img_containers and extract the title and full img_url
    for img in img_containers:
        title_img_dicts['title'] = img.find('h3').text

        # store img 'href' in variable 'img_link' and then append that to the 'img_url_list'
        img_link = img.find('a', class_='itemLink product-item')['href']
        img_url.append(img_link)

        # store the full URL to the image, so that the program knows where to get the information
        img_url_list = [hem_url + url for url in img_url]
        
        for search_url in img_url_list:
            scrape_img(search_url)
        
        # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary 
        # for each hemisphere.
        hemisphere_img_urls.append(dict_to_list(title_img_dicts))

    # Store all data into a single dictionary
    mars_data = {
        "Most Recent Headline": news_title,
        "Recent Headline Teaser": news_p,
        "Featured Image": featured_image_url,
        "Mars Facts": html_table,
        "Mars Hemispheres": hemisphere_img_urls
    }
    # quit the browser after scraping
    browser.quit()
    
    # return results
    return mars_data

