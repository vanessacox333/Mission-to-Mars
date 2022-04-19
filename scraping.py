# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


def scrape_all():
    
    browser = Browser('firefox', headless=False)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data



def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

def hemisphere(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')


    # Results returned as an iterable list
    items = hemisphere_soup.find_all('div', class_='item')

    # Loop through items
    for i in items:
        
        
        # Create empty hemispheres dictionary
        hemispheres = {}  
        
        # Retrieve the titles
        title = i.find('h3').get_text()
        print(title)
        
        
        # Get the link to go the full image site
        img_url = i.find('a')['href']
        print(img_url)
        
        # Creating the full_img_url
        full_img_url = url + img_url
        
        # Use browser to go to the full image url and set up the HTML parser
        browser.visit(full_img_url)
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        # Retrieve the full image urls
        hemisphere_img = img_soup.find('div', class_='downloads')
        hemisphere_full_img = hemisphere_img.find('a')['href']
        hemi_url = url + hemisphere_full_img
        
        # Printing hemisphere_full_img
        print(hemi_url)
        
        
        # Creating hemispheres dict
        hemispheres['img_url'] = hemi_url
        hemispheres['title'] = title
    
        #Append the hemisphere_image_urls list
        hemisphere_image_urls.append(hemispheres)
        browser.back() 
        


    # 4. Print the list that holds the dictionary of each image url and title.
        return(hemisphere_image_urls)


    # # 5. Quit the browser
    # browser.quit()





