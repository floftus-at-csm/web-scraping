# file for learning beautiful soup by scraping ubu web

from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
import time
import json

def scrape_url(url):
    URL = url
    page = requests.get(URL)
    html = BeautifulSoup(page.content, "html.parser")
    return html

def filter_description_text(html_input):
    if html_input.findAll('a') is not None:
        a = html_input.findAll('a')
        # href = a[0]['href']
    else:
        href = ""
    # print(href)
    text = html_input.text
    if "RESOURCES:" in text:
        text = text[:text.index("RESOURCES")] 
    # print("input text", text)
    text = re.sub(' +', ' ', text) # remove excessive spaces
    text = text.replace('\t','') # remove tabs
    # text = text.replace('\n+','') # trying to remove excessive line breaks
    text = re.sub(r'\n\s*\n', '\n', text)
    # print("output text", text)
    # print(html_input.decode('utf-8'))
    return text

def filter_artist_page(body_html):
    table_body = body_html.findAll("td", {"class": "default"})
    artist_artwork_links = table_body[1].findAll('a')
    full_links = []
    sound_links = []
    for link in artist_artwork_links:
        if("../sound" not in link['href']):
            full_artwork_link = 'https://www.ubu.com/film/' + str(link['href'])
            full_links.append(full_artwork_link)
        else:
            sound_links.append(link)
    for link in table_body[1]("a"):
        link.decompose()
    for bold in table_body[1]("b"):
        bold.decompose()
    text = table_body[1].text
    text = re.sub(' +', ' ', text) # remove excessive spaces
    text = re.sub(r'\n\s*\n', '\n', text)
    # text = re.sub("[\(\[].*?[\)\]]", "", text)
    # print("the text is: ", text)
    # print("the full links are: ", full_links)
    return text, full_links, sound_links

def scrape_ubu_body(html, artist_desc):
    dictionary = {}
    # print(artist_page_link)
    # tag = artist_html.find("div", {"class": "ubucreator"}), dates, url,
    # print(html)
    artist = html.find("span", {"id": "ubucreator"})
    dictionary["artist"] = artist.text
    dates = html.find("span", {"id": "ububiodates"})
    dictionary["date"] = dates.text
    
    if artist_desc is not None:
        dictionary["artist_description"] = artist_desc
    else:
        dictionary["artist_description"] = ""
    dictionary["film_title"] = html.find("span", {"id": "ubuwork"}).text
    desc = filter_description_text(html.find("div", {"id": "ubudesc"}))
    dictionary["film_description"] = desc
    try:
        dictionary['url'] = html.find_all('iframe')[0]['src']
    except:
        dictionary['url'] = "find_this_one!"
    return dictionary


# =========================================================================
# Main Loop
if __name__ == "__main__":
    main_html = scrape_url("https://www.ubu.com/film/index.html")

    table = main_html.find('td')
    links = main_html.findAll('a')
    hrefs = []
    artist_pages = []
    for link in links:
        # print(type(link['href']))
        if "index" in link['href']:
            links.remove(link)
        else:
            href = "https://www.ubu.com/film/" + link['href'] 
            artist_pages.append(href)
            hrefs.append(link['href'])
        # potentially remove the dance pages
    print(artist_pages)
    full_dict = {}
    # for artist_page_link in artist_pages[0:10]:
    for artist_page_link in artist_pages:
        # full_dict = {}
        # check if page contains ububody
        # if it does run the scrape content function
        artist_html = scrape_url(artist_page_link)
        if artist_html.find("div", {"class": "ububody"}) is None:
            time.sleep(1)
            print(artist_page_link)
            print("Tag not Found")
            try:
                artist_description, artist_artwork_links, sound_links = filter_artist_page(artist_html)
                for link in artist_artwork_links:
                    artist_html2 = scrape_url(link)
                    # print(artist_html2.find("div", {"class": "ububody"}))
                    if artist_html2.find("div", {"class": "ububody"}) is not None:
                        the_html = scrape_url(link)
                        dict1 = scrape_ubu_body(the_html, artist_description)
                        print("-----------------------------")
                        print("the link is: ", link)
                        pprint(dict1)
                        full_dict[dict1['film_title']] = (dict1)
                        print("-----------------------------")
                        with open('result4.json', 'w') as fp:
                            json.dump(full_dict, fp, indent=4)

            except:
                pass
        else:
            print("artist page link is: ", artist_page_link)
            try: 
                dict1 = scrape_ubu_body(artist_html, None)
                print(dict1)
                full_dict[dict1['film_title']] = (dict1)
                with open('result4.json', 'w') as fp:
                    json.dump(full_dict, fp, indent=4)
            except:
                pass
    # print(full_dict)
  

    # https://www.ubu.com/film/averty_gainsbourg.html

    # html_output = scrape_url("https://www.ubu.com/film/averty_gainsbourg.html")
    # html_output2 = scrape_url("https://www.ubu.com/film/elsken_appel.html")
    # description = html_output.find("div", {"id": "ubudesc"})
    # filter_description_text(description)
    # # print(type(description))