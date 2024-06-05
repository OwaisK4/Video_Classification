import json, re
import requests, bs4

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
}
query = "toronto+chinatown"
target_url = f"https://www.google.com/search?q={query}"
# response = requests.get(target_url, headers=BASE_HEADERS)
# soup = bs4.BeautifulSoup(response.text, 'html.parser')
# for link in soup.find_all('a', attrs={'href': re.compile("^https://")}): 
#     # display the actual urls 
#     print(link.get('href'))
string = "Entity: 'Hockey Hall of Fame' has category 'Location'"
print(string.split("'"))

# hidden_data = re.findall(r"pageManifest:({.+?})};", response.text, re.DOTALL)[0]
# hidden_data = json.loads(hidden_data)['urqlCache']['results']
# review_data = json.loads(next(v["data"] for k, v in hidden_data.items() if '"reviewListPage"' in v["data"]))
# for review in review_data['locations'][0]['reviewListPage']['reviews']:
#     print(review)