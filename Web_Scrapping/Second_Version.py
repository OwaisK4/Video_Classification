from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def googleRating(location,driver):
    res = {
        'rating':'',
        'no of people':''
    }
    url = "https://www.google.com/maps"
    try:
        driver.get(url)
        element_locator = (By.ID,'searchboxinput')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(element_locator)
        )
        search = driver.find_element(By.ID, 'searchboxinput')
        search.send_keys(location)
        search = driver.find_element(By.ID, 'searchbox-searchbutton')
        search.click()
        element_locator = (By.CLASS_NAME,'F7nice')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(element_locator)
        )
        ratingDiv = driver.find_element(By.CLASS_NAME,'F7nice')
        # print(ratingDiv.text)
        temp = ratingDiv.text
        temp = temp.split()
        res['rating'] = temp[0]
        temp = temp[1].split('(')
        temp = temp[1].split(')')
        res['no of people'] = temp[0]
    except:
        print('No rating found on google or network issue')
    return res

def description(location,driver):
    res = ''
    url = "https://www.google.com"
    try:
        driver.get(url)
        element_locator = (By.ID,'APjFqb')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(element_locator)
        )
        search = driver.find_element(By.ID, 'APjFqb')
        search.send_keys('give me a short description of ' + location)
        search.send_keys(Keys.ENTER)
        element_locator = (By.CLASS_NAME,'hgKElc')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(element_locator)
        )
        description = driver.find_element(By.CLASS_NAME,'hgKElc')
        # print(description.text)
        res = description.text   
    except:
        print('No Description on google or network issue')
    return res

def tripadvisorRating(location,driver):
    res = {
        'rating':'',
        'no of people':''
    }
    url = "https://www.google.com"
    try:
        driver.get(url)
        element_locator = (By.ID,'APjFqb')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(element_locator)
        )
        search = driver.find_element(By.ID, 'APjFqb')
        search.send_keys(location + ' tripadvisor')
        search.send_keys(Keys.ENTER)
        element_locator = (By.XPATH,"//*[@id='rso']/div[1]/div/div/div/div[4]/div")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(element_locator)
        )
        rating = driver.find_element(By.XPATH,"//*[@id='rso']/div[1]/div/div/div/div[4]/div")
        # print(rating.text)
        temp = rating.text
        temp = temp.split()
        res['rating'] = temp[1]
        res['no of people'] = temp[3]
    except: 
        print('No rating found on tripadvisor or network issue')
        pass
    return res

def getRatingAndDescription(location):
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    ans = {
        'google':{},
        'description':'',
        'tripadvisor':{}
    }
    ans['google'] = googleRating(location,driver)
    ans['description'] = description(location,driver)
    ans['tripadvisor'] = tripadvisorRating(location,driver)
    print(ans)
    driver.quit()
    return ans

locations = [
    "Chinatown", "art gallery", "New York", "city halls", "contemporary Art Museum", "building", 
    "fast food joint", "bike lanes", "Canada", "town", "castle", "corridors", "LA", "Distillery District", 
    "subway", "harbor", "Vancouver", "U.S.", "museums", "Toronto", "Queen St. West", "historic homes", 
    "history museums", "restaurant", "subway line", "outside", "galleries", "ATM", "Presto", "OK", 
    "Chicago", "crate city", "Koreatown", "neighborhood", "city", "metro", "Casa Loma", "Union Station", 
    "Cabbagetown", "shops", "Greektown", "hallways", "waterfront", "downtown", "hotel", "sand tower", 
    "working area", "valet", "boutiques", "home", "Kensington Market", "Toronto, Canada", "bike lane", 
    "dry land", "boardwalk", "CN Tower", "jungle", "malls", "Hockey Hall of Fame", "kiosks", "ocean", 
    "Yorkville", "St", "block", "residential area", "Roger Center", "Ripley's Aquarium", "Toronto Railway Museum", 
    "Union", "lake", "Film Cafe", "buildings", "halls", "hiking trails", "Nathan Phillips Square", "stores", 
    "New York City", "dogs off leash area", "Bang Bang Ice Cream Shop", "elevator", "city limits", "City Hall", 
    "Film Cafe", "Saint Lawrence Market", "Kensington Market", "Eaton Center", "gift shop", "Italy", "restaurants", 
    "rooftop bar", "Montreal", "Trophy Hall", "observation deck", "street", "Canadas", "restaurant", "temple", 
    "High Park", "sports facilities", "aisles", "stalls", "zoo", "city", "gardens", "Beaches", "U.S.", 
    "coffee shops", "closet", "America", "coffee shops", "Kensington", "overseas", "townhouses", "restaurants", 
    "neighborhood", "Boston", "Cape", "alleyways", "shower", "balcony room", "Hotel Toronto", "Japanese", 
    "little bar area", "Thrift stores", "Subway", "underground", "beauty store", "park area", "coffee shop", 
    "Trinity Melwood", "Toronto Light Rd.", "W Toronto", "Nut Bar", "bars", "Times Square", "park", 
    "hotel room", "Korean", "shopping area", "Wilford"
]

getRatingAndDescription("cn tower toronto")
