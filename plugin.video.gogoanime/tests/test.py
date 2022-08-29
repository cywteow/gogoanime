from requests import Session
# from bs4 import BeautifulSoup
import re
import requests
# import urlparse
import json
import string

# digs = string.digits + string.ascii_letters

# session = Session()

# domain = 'https://www2.gogoanime.video'

# def request(path):
#     response = session.get(domain + path)

#     if response.status_code == 200:
#         response.encoding = 'utf-8'
#         return response

# def request2(path):
#     headers = {'Referer': 'https://gogoplay1.com/'}
#     response = session.get(path, headers=headers, allow_redirects=False)

#     if response.status_code == 302:
#         return response
#     if response.status_code == 200:
#         response.encoding = 'utf-8'
#         return response

# Recent release
# response = request("/?page=1")
# document = BeautifulSoup(response.text, 'html.parser').find('div', class_="last_episodes loaddub")
# items = []
# for li in document.find_all('li'):
#     a = li.find('a')
#     print(a['href'])
#     it = re.search("^(/.+)-episode-([0-9/-]+)$", a['href'].encode('utf-8'), flags=0)
#     path = "/category"+it.group(1).encode('utf-8')
    # print("Title: "+ a['title'].encode('utf-8'))
    # print("Img: "+ li.find('img')['src'])
    # response2 = request(a['href'])
    # document2 = BeautifulSoup(response2.text, 'html.parser').find('div', class_="anime-info").find('a')
    # print("Path: "+ document2['href'])
    # response3 = request(document2['href'])
    # document3 = BeautifulSoup(response3.text, 'html.parser').find('div', class_="anime_info_body_bg")
    # print("Plot: "+ document3.find_all('p', class_="type")[1].contents[1].encode('utf-8'))

# Category
# response = request("/category/black-clover-tv")
# document = BeautifulSoup(response.text, 'html.parser')
# for script in document.find_all('script'):
#     if script.string is not None:
#         it = re.search("var base_url_cdn_api = \'(.+)\'", script.string, flags=0)
#         if it is not None:
#             base_url_cdn_api = it.group(1)
#             break
# episode_page = document.find('ul', id='episode_page')
# for episode_page_a in reversed(episode_page.find_all('a')):  
#     id = document.find('input', id="movie_id")['value']
#     default_ep = document.find('input', id="default_ep")['value']
#     alias = document.find('input', id="alias_anime")['value']
#     a = document.find('ul', id="episode_page").find('a')
#     ep_start = episode_page_a['ep_start']
#     ep_end = episode_page_a['ep_end']

#     getEpsUrl = base_url_cdn_api + "ajax/load-list-episode?ep_start=" + ep_start + '&ep_end=' + ep_end + '&id=' + id + '&default_ep=' + default_ep + '&alias=' + alias

#     response2 = session.get(getEpsUrl)
#     document2 = BeautifulSoup(response2.text, 'html.parser')
#     for li in document2.find_all('li'):
#         a = li.find('a')
#         print(a['href'].strip())
#         div = a.find('div', class_="name")
#         name = div.contents[0].string + div.contents[1]
#         print(name)

#Resolve vidstreaming
# response = requests.get("https://vidstreaming.io/streaming.php?id=MTQ2MDEy&title=Mewkledreamy+episode+22&typesub=SUB")
# document = BeautifulSoup(response.text, 'html.parser')
# id = document.find('input', id="id")['value']
# title = document.find('input', id="title")['value']
# typesub = document.find('input', id="typesub")['value']
# parsed_url = urlparse.urlparse(response.url)
# response2 = requests.get(parsed_url.scheme+"://"+parsed_url.hostname+ "/ajax.php?id=" + id+ "&title=" + title +"&typesub=" + typesub)
# jsonObj = json.loads(response2.text)
# print(jsonObj['source_bk'][0]['file'])

#resolve gogoserver
# response = requests.get("https://gogo-stream.com/load.php?id=MTQ2MDY0&title=Rail+Romanesque+episode+1&typesub=SUB")
# document = BeautifulSoup(response.text, 'html.parser')
# script = document.find('div', class_="videocontent").find('script', type="text/JavaScript")
# it = re.search("sources:\[{file: \'(.+)\',label:", script.string, flags=0)
# if it is not None:
#     url = it.group(1)

# response2 = requests.get(url, allow_redirects=False)
# print(response2.status_code)
# print(response2.url)
# print(response2.headers['Location'])

#resolve xstreamcdn
# url = "https://fcdn.stream/v/60p78c0k0ey862w"
# parsedUrl = urlparse.urlparse(url).path.split("/")[-1:][0]

# response = requests.post("https://fcdn.stream/api/source/"+ parsedUrl)
# jsonObj = json.loads(response.text)
# requestUrl = jsonObj['data'][0]['file']
# response2 = requests.get(requestUrl, allow_redirects=False)
# print(response2.headers['Location'])

#Popular ongoing
# response = requests.get("https://ajax.apimovie.xyz/ajax/page-recent-release-ongoing.html?page=12")
# document = BeautifulSoup(response.text, 'html.parser').find('div', class_="added_series_body popular")
# for li in document.find_all('li'):
#         a = li.find('a')
#         print(a['title'])
#         style = li.find('div', class_="thumbnail-popular")['style']
#         print(re.search("^background: url\(\'(.+)\'\);$", style, flags=0).group(1))

#popular
# response = requests.get("https://www2.gogoanime.video/popular.html?page=1")
# document = BeautifulSoup(response.text, 'html.parser').find('div', class_="last_episodes")
# for li in document.find_all('li'):
#         a = li.find('a')
#         print(a['title'])
#         print(a['href'])
#         print(a.find('img')['src'])

#genre
# response = requests.get("https://www2.gogoanime.video/genre/action?page=1")
# document = BeautifulSoup(response.text, 'html.parser').find('div', class_="last_episodes")

# #category
# response = requests.get("https://www2.gogoanime.video/category/boruto-naruto-next-generations")
# document = BeautifulSoup(response.text, 'html.parser').find('div', class_="anime_info_body_bg")
# img = document.find('img')['src'].encode('utf-8').strip()
# title = document.find('h1').string.encode('utf-8').strip()
# pList = document.find_all('p', class_="type")
# plot = pList[1].contents[1].encode('utf-8').strip()

# genre = ""
# for a in pList[2].find_all('a'):
#     genre += a.string.encode('utf-8')
# try:
#     year = pList[3].contents[1].encode('utf-8').strip()
#     year = int(year) if year.isdigit() else None
# except IndexError:
#     year = None
# status = pList[4].contents[1].encode('utf-8').strip()

# def int2base(x, base):
#     if x < 0:
#         sign = -1
#     elif x == 0:
#         return digs[0]
#     else:
#         sign = 1

#     x *= sign
#     digits = []

#     while x:
#         digits.append(digs[int(x % base)])
#         x = int(x / base)

#     if sign < 0:
#         digits.append('-')

#     digits.reverse()

#     return ''.join(digits)

# response = requests.get("https://www.mp4upload.com/embed-m380e4rz6c19.html")
# document = BeautifulSoup(response.text, 'html.parser').find_all('script', type="text/javascript")
# for script in document:
#     if script.string is not None and "eval(function(p,a,c,k,e,d)" in script.string:
#         it = re.search(r"^eval\(function\(p,a,c,k,e,d\)(.+)\('(.+)',([0-9]+),([0-9]+),'(.+)'\.split\('\|'\)\)\)", script.string, flags=0)
#         p = it.group(2)
#         a = int(it.group(3))
#         c = int(it.group(4))
#         k = it.group(5).split("|")
#         c-=1
#         while c > 0:
#             if k[c] is not None:
#                 p = re.sub("\\b"+int2base(c, a)+"\\b", k[c], p)
#             c-=1
#         print(p)
#         it = re.search(r'player.src\("([^)]+)"\)', p, flags=0)
#         print(it.group(1))

# response = request("/boruto-naruto-next-generations-episode-111")
# document = BeautifulSoup(response.text, 'html.parser')
# for server in document.find('div', class_="anime_muti_link").find_all('a'):
#         if server.contents[1].name == 'i':
#             title = server.contents[2]
#         else:
#             title = server.contents[1]
#         print(server["data-video"])


# response = request2('https://gogo-cdn.com/download.php?url=aHR0cHM6LyAdeqwrwedffryretgsdFrsftrsvfsfsr9jZG4yMyAawehyfcghysfdsDGDYdgdsfsdfwstdgdsgtert5hbmljZG4uc3RyZWFtL3VzZXIxMzQyL2RlNDhhMGViNjBmZmUwMGQ4YmMyNTM5YTg3NWEzNjVkL0VQLjIyNC52MC40ODBwLm1wND90b2tlbj1ZLVFnRHByQW5BRHZ2Xzc4NWdoTU9nJmV4cGlyZXM9MTYzNjkwNjIyNyZpZD0xNzQ1NDQ=')
# print(response.headers['Location'])

response = requests.get('https://consumet-api.herokuapp.com/anime/gogoanime/watch/dragon-quest-dai-no-daibouken-2020-episode-90')
data = response.json()
if "sources" in data and len(data["sources"]) > 0:
    print(len(data["sources"]))