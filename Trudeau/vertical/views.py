from django.shortcuts import render
from django.utils.text import slugify
from time import sleep
import os, re
import requests, bs4

# Create your views here.
def index(request):
    context = {
        'title': 'Home Page',
        'heading': 'Welcome to Home page!',
        'content': 'This is some content for Home page.',
    }
    return render(request, 'index.html', context)

def blog(request):
    # basepath = os.path.realpath(__name__)
    basepath = "vertical"
    results_path = os.path.join(basepath, "Results")
    os.makedirs(results_path, exist_ok=True)
    results = os.listdir(results_path)
    # print(results)
    context = {
        "files": results,
    }
    return render(request, "blog.html", context)

def get_link(query: str):
    BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
    }
    query = query.replace(" ", "+")
    query = f"toronto+{query}+tripadvisor"
    target_url = f"https://www.google.com/search?q={query}"
    response = requests.get(target_url, headers=BASE_HEADERS)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    url = None
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}): 
        # display the actual urls
        # print(link.get('href'))
        if link.get('href').startswith("https://www.tripadvisor.com") and link.get('href') != "https://www.tripadvisor.com":
            url = link.get('href')
            break
    return url

def blog_details(request, filename):
    basepath = "vertical"
    results_path = os.path.join(basepath, "Results")
    os.makedirs(results_path, exist_ok=True)
    results = os.listdir(results_path)
    print(filename)
    file = None
    for i in range(len(results)):
        if slugify(results[i]) == filename:
            file = results[i]
            break
    context = {
        "data": "",
    }
    if file:
        try:
            with open(os.path.join(results_path, file), "r") as f:
                # print("HEREEEEEEEEEEEEEEEEEEEEEEEE")
                lines = [line.strip() for line in f.readlines()]
                index = lines.index("Named Entities:")
                transcribed_text = lines[1:index]
                named_entities = lines[index + 1:]
                named_entities = [ne for ne in named_entities if ne.split()[-1] == "'Location'" and ne.split()[1].replace("'","").istitle()]
                named_entity_links = []
                for ne in named_entities:
                    # location = ne.split()[1].replace("'","")
                    location = ne.split("'")[1]
                    url = get_link(location)
                    if url:
                        print(url)
                    named_entity_links.append({"url": url, "named_entity": ne})

                context = {
                    "transcribed_text": " ".join(transcribed_text),
                    "named_entities": named_entity_links,
                    # "named_entites": " ".join(named_entites),
                }
        except:
            pass
    return render(request, "blog-details.html", context)