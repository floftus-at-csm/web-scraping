import os
import time
import datetime
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException        
from webdriver_manager.chrome import ChromeDriverManager
from htmldate import find_date

USRNME = 'BocarBa'

def selenium_driver_helper(main_url: str):
    """
    Create driver object using chrome driver and selenium.
    :param main_url: string with link to main website
    :return driver: selenium driver object
    """
    # path to the chromedriver executable
    chromedriver = "C:/Users/robal/Downloads/chromedriver_win32chromedriver/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--incognito")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(main_url)
    
    return driver

def enter_text_helper(driver: webdriver.Chrome, xpath: str, text: str):
    """
    Helper function to enter text into a web field using selenium
    :param driver: selenium driver object
    :param xpath: the xpath of the element to enter text into
    :param text: the text to be entered
    :result: enters text into element
    """
    inp = driver.find_element_by_xpath(xpath)
    inp.send_keys(USRNME)

def click_button_helper(driver: webdriver.Chrome, xpath: str):
    """
    Helper function to click web element using selenium
    :param driver: selenium driver object
    :param xpath: the xpath of the element to enter text into
    :return bool: whether clicking the element was successful
    :result: clicks web element
    """
    try:
        element = driver.find_element_by_xpath(xpath)
        element.click()  
        return True
    except:
        return False

def download_fsearch_page_csv(driver: webdriver.Chrome, main_page_window):
    """
    Handles downloading a single page from foundation search as csv
    :param driver: selenium driver object
    :param main_page_window: the window_handle of the main page 
    :return bool: whether clicking the next page was successful
    :result: downloads csv of data in page, and clicks to next page if possible
    """
    export_csv_xpath = '//*[@id="ctl00_ctl00_TabContentPlaceHolder_FindFundersContentPlaceHolder_ExportLink"]/span'
    click_button_helper(driver, export_csv_xpath)
    
    popup_window = driver.window_handles[1]
    driver.switch_to.window(popup_window)

    time.sleep(2)

    select_all_xpath = '/html/body/form/div[4]/table[2]/tbody/tr/td[1]/a[1]'
    download_csv_xpath = '/html/body/form/div[4]/div[2]/table/tbody/tr/td[1]/a[1]'
    exit_popup_xpath = '/html/body/form/div[3]/div/a/span[1]'

    # download csv in popup window
    click_button_helper(driver, select_all_xpath)
    click_button_helper(driver, download_csv_xpath)

    # close popup window and return to main page
    time.sleep(2)
    click_button_helper(driver, exit_popup_xpath)
    driver.switch_to.window(main_page_window)

    # click next page - DOES NOT CURRENTLY WORK
    time.sleep(10)

    return click_button_helper(driver, '//*[@id="ctl00_ctl00_TabContentPlaceHolder_FindFundersContentPlaceHolder_ctl00_listView_ctl01_btnNext"]')

def scrape_foundations_search():
    """
    Handles downloading data from foundations search
    :result: downloads csvs of from each page of data
    """
    url = 'https://www.foundationsearch.com/FindFunders/GrantVisualizer.aspx?searchid=5430205' 
    driver = selenium_driver_helper(url)

    usrnme_xpath =  '/html/body/form/div[3]/main/div[4]/div/div/div/div[1]/div/div/div[1]/div[2]/input'
    pwrd_xpath = '/html/body/form/div[3]/main/div[4]/div/div/div/div[1]/div/div/div[2]/div[2]/input'   
    submit_xpath = '/html/body/form/div[3]/main/div[4]/div/div/div/div[1]/div/div/div[4]/div[2]/a/span'

    # login page
    time.sleep(2)
    enter_text_helper(driver, usrnme_xpath, USRNME)
    enter_text_helper(driver, pwrd_xpath, USRNME)
    time.sleep(2)
    click_button_helper(driver, submit_xpath)

    main_page_window = driver.window_handles[0]

    # download csvs
    new_page = True
    while new_page:
        new_page = download_fsearch_page_csv(driver, main_page_window)



