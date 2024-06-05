from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

def googleRating(location):
    res = {
        'rating':'',
        'no of people':''
    }
    options = Options()
    options.add_argument("--headless")
    url = "https://www.google.com/maps"
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(6)
    search = driver.find_element(By.ID, 'searchboxinput')
    search.send_keys(location)
    time.sleep(6)
    search = driver.find_element(By.ID, 'searchbox-searchbutton')
    search.click()
    time.sleep(6)
    try:
        ratingDiv = driver.find_element(By.CLASS_NAME,'F7nice')
        # print(ratingDiv.text)
        temp = ratingDiv.text
        temp = temp.split()
        res['rating'] = temp[0]
        temp = temp[1].split('(')
        temp = temp[1].split(')')
        res['no of people'] = temp[0]   
    except: 
        # print("Not found")
        pass

    time.sleep(1)
    driver.quit()
    return res

def description(location):
    res = ''
    url = "https://www.google.com"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(6)
    search = driver.find_element(By.ID, 'APjFqb')
    search.send_keys('give me a short description of ' + location)
    search.send_keys(Keys.ENTER)
    time.sleep(6)
    try:
        description = driver.find_element(By.CLASS_NAME,'hgKElc')
        # print(description.text)
        res = description.text   
    except: 
        # print("Not found")
        pass

    time.sleep(1)
    driver.quit()
    return res

def tripadvisorRating(location):
    res = {
        'rating':'',
        'no of people':''
    }
    url = "https://www.google.com"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(6)
    search = driver.find_element(By.ID, 'APjFqb')
    search.send_keys('what is the rating of ' + location + ' by tripadvisor?')
    search.send_keys(Keys.ENTER)
    time.sleep(6)
    try:
        rating = driver.find_element(By.XPATH,"//*[@id='rso']/div[1]/div/div/div/div[4]/div")
        # print(rating.text)
        temp = rating.text
        temp = temp.split()
        res['rating'] = temp[1]
        res['no of people'] = temp[3]   
    except: 
        # print("Not found")
        pass

    time.sleep(1)
    driver.quit()
    return res

def getRatingAndDescription(location):
    ans = {
        'google':{},
        'description':'',
        'tripadvisor':{}
    }
    ans['google'] = googleRating(location)
    ans['description'] = description(location)
    ans['tripadvisor'] = tripadvisorRating(location)
    print(ans)
    return ans

getRatingAndDescription('cn tower')