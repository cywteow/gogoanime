# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import Session
from rerouting import Rerouting
from resources.lib.database import InternalDatabase, ExternalDatabase
from xbmc import Keyboard
from xbmcaddon import Addon
from xbmcgui import Dialog, ListItem

import json
from urllib.parse import urlparse
import requests
import os
import re
import xbmc
import xbmcplugin
import resolveurl
import xbmcvfs

__plugins__ = os.path.join(xbmcvfs.translatePath(Addon().getAddonInfo('path')), 'resources/lib/resolveurl/plugins')
domain = 'https://www2.gogoanime.video'
domain2 = 'https://ajax.apimovie.xyz'
plugin = Rerouting()
session = Session()
attrs = vars(plugin)
print(', '.join("%s: %s" % item for item in attrs.items()))


@plugin.route('/')
def index():
    items = [
        (plugin.url_for('/recently-viewed'), ListItem("Recently viewed"), True),
        (plugin.url_for('/?page=1'), ListItem("Recent Release"), True),
        (plugin.url_for('/ajax/page-recent-release-ongoing.html?page=1'), ListItem("Popular Ongoing Update"), True),
        (plugin.url_for('/popular.html?page=1'), ListItem("Popular Anime"), True),
        (plugin.url_for('/list_genres'), ListItem("View By Genres"), True),
        (plugin.url_for('/season'), ListItem("View By Year-Season"), True),
        (plugin.url_for('/search.html?page=1'), ListItem("Search"), True),
    ]

    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route(r'/recently-viewed(\?delete=(?P<delete>[^&]+))?')
def recently_viewed(delete=None):
    ExternalDatabase.connect()
    InternalDatabase.connect()

    if delete is not None:
        ExternalDatabase.remove(delete)
        xbmc.executebuiltin('Container.Refresh')
    else:
        items = []

        for path in ExternalDatabase.fetchall():
            anime = get_anime_detail(path)
            item = ListItem(anime['title'])
            item.addContextMenuItems([
                ("Remove", 'RunPlugin(plugin://plugin.video.gogoanime/recently-viewed?delete=' + path + ')'),
                ("Remove all", 'RunPlugin(plugin://plugin.video.gogoanime/recently-viewed?delete=%)')
            ])
            item.setArt({'poster': anime.pop('poster')})
            item.setInfo('video', anime)
            items.append((plugin.url_for(path), item, True))

        xbmcplugin.setContent(plugin.handle, 'videos')
        xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
        xbmcplugin.endOfDirectory(plugin.handle)

    ExternalDatabase.close()
    InternalDatabase.close()

@plugin.route(r'^/season\?year=[0-9]+$')
@plugin.route('^/season$')
def year():
    if "year" in plugin.query:
        items = [
            (plugin.url_for('/sub-category/'+"spring-"+plugin.query['year'][0]+"-anime?page=1"), ListItem("Spring"), True),
            (plugin.url_for('/sub-category/'+"summer-"+plugin.query['year'][0]+"-anime?page=1"), ListItem("Summer"), True),
            (plugin.url_for('/sub-category/'+"fall-"+plugin.query['year'][0]+"-anime?page=1"), ListItem("Fall"), True),
            (plugin.url_for('/sub-category/'+"winter-"+plugin.query['year'][0]+"-anime?page=1"), ListItem("Winter"), True),
        ]
    else:
        items = [
            (plugin.url_for('/season?year=2020'), ListItem("2020"), True),
            (plugin.url_for('/season?year=2019'), ListItem("2019"), True),
            (plugin.url_for('/season?year=2018'), ListItem("2018"), True),
            (plugin.url_for('/season?year=2017'), ListItem("2017"), True),
            (plugin.url_for('/season?year=2016'), ListItem("2016"), True),
            (plugin.url_for('/season?year=2015'), ListItem("2015"), True),
            (plugin.url_for('/season?year=2014'), ListItem("2014"), True),
        ]
        
    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route("/list_genres")
def list_genres():
    items = [
        (plugin.url_for('/genre/action?page=1'), ListItem("Action"), True),
        (plugin.url_for('/genre/adventure?page=1'), ListItem("Adventure"), True),
        (plugin.url_for('/genre/cars?page=1'), ListItem("Cars"), True),
        (plugin.url_for('/genre/comedy?page=1'), ListItem("Comedy"), True),
        (plugin.url_for('/genre/dementia?page=1'), ListItem("Dementia"), True),
        (plugin.url_for('/genre/demons?page=1'), ListItem("Demons"), True),
        (plugin.url_for('/genre/drama?page=1'), ListItem("Drama"), True),
        (plugin.url_for('/genre/dub?page=1'), ListItem("Dub"), True),
        (plugin.url_for('/genre/ecchi?page=1'), ListItem("Ecchi"), True),
        (plugin.url_for('/genre/fantasy?page=1'), ListItem("Fantasy"), True),
        (plugin.url_for('/genre/game?page=1'), ListItem("Game"), True),
        (plugin.url_for('/genre/harem?page=1'), ListItem("Harem"), True),
        (plugin.url_for('/genre/hentai?page=1'), ListItem("Hentai"), True),
        (plugin.url_for('/genre/historical?page=1'), ListItem("Historical"), True),
        (plugin.url_for('/genre/horror?page=1'), ListItem("Horror"), True),
        (plugin.url_for('/genre/josei?page=1'), ListItem("Josei"), True),
        (plugin.url_for('/genre/kids?page=1'), ListItem("Kids"), True),
        (plugin.url_for('/genre/magic?page=1'), ListItem("Magic"), True),
        (plugin.url_for('/genre/martial-arts?page=1'), ListItem("Martial Arts"), True),
        (plugin.url_for('/genre/mecha?page=1'), ListItem("Mecha"), True),
        (plugin.url_for('/genre/military?page=1'), ListItem("Military"), True),
        (plugin.url_for('/genre/music?page=1'), ListItem("Music"), True),
        (plugin.url_for('/genre/mystery?page=1'), ListItem("Mystery"), True),
        (plugin.url_for('/genre/parody?page=1'), ListItem("Parody"), True),
        (plugin.url_for('/genre/police?page=1'), ListItem("Police"), True),
        (plugin.url_for('/genre/psychological?page=1'), ListItem("Psychological"), True),
        (plugin.url_for('/genre/romance?page=1'), ListItem("Romance"), True),
        (plugin.url_for('/genre/samurai?page=1'), ListItem("Samurai"), True),
        (plugin.url_for('/genre/school?page=1'), ListItem("School"), True),
        (plugin.url_for('/genre/sci-fi?page=1'), ListItem("Sci-Fi"), True),
        (plugin.url_for('/genre/seinen?page=1'), ListItem("Seinen"), True),
        (plugin.url_for('/genre/shoujo?page=1'), ListItem("Shoujo"), True),
        (plugin.url_for('/genre/shoujo-ai?page=1'), ListItem("Shoujo Ai"), True),
        (plugin.url_for('/genre/shounen?page=1'), ListItem("Shounen"), True),
        (plugin.url_for('/genre/shounen-ai?page=1'), ListItem("Shounen Ai"), True),
        (plugin.url_for('/genre/slice-of-life?page=1'), ListItem("Slice of Life"), True),
        (plugin.url_for('/genre/space?page=1'), ListItem("Space"), True),
        (plugin.url_for('/genre/sports?page=1'), ListItem("Sports"), True),
        (plugin.url_for('/genre/super-power?page=1'), ListItem("Super Power"), True),
        (plugin.url_for('/genre/supernatural?page=1'), ListItem("Supernatural"), True),
        (plugin.url_for('/genre/thriller?page=1'), ListItem("Thriller"), True),
        (plugin.url_for('/genre/vampire?page=1'), ListItem("Vampire"), True),
        (plugin.url_for('/genre/yaoi?page=1'), ListItem("Yaoi"), True),
        (plugin.url_for('/genre/yuri?page=1'), ListItem("Yuri"), True),
    ]

    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route(r'^/\?page=[0-9]+$')
def recent_release():
    InternalDatabase.connect()
    pageNum = int(plugin.query['page'][0])
    response = request(plugin.pathqs)

    document = BeautifulSoup(response.text, 'html.parser').find('div', class_="last_episodes loaddub")
    items = []
    for li in document.find_all('li'):
        a = li.find('a')
        p = li.find('p', class_="episode")
        # it = re.search("^(/.+)-episode-([0-9/-]+)$", a['href'].encode('utf-8'), flags=0)
        response = request(a['href'])
        path = BeautifulSoup(response.text, 'html.parser').find('div', class_="anime-info").find('a')['href']
        # path = "/category"+it.group(1).encode('utf-8')
        anime = get_anime_detail(path)
        item = ListItem(anime['title'] + " " + p.string)
        item.setArt({'poster': anime.pop('poster')})
        item.setInfo("video", anime)
        items.append((plugin.url_for(path), item, True))
    
    item = ListItem("Next >>")
    items.append((plugin.url_for("/?page="+ str(pageNum + 1)), item, True))
    if pageNum != 1:
        item = ListItem("Back to main page")
        items.append((plugin.url_for("/"), item, True))

    InternalDatabase.close()
    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route(r'/ajax/page-recent-release-ongoing.html\?page=[0-9]+')
def on_going():
    InternalDatabase.connect()
    pageNum = int(plugin.query['page'][0])
    response = request2(plugin.pathqs)
    document = BeautifulSoup(response.text, 'html.parser').find('div', class_="added_series_body popular")
    items = []
    for li in document.find_all('li'):
        a = li.find_all('a')
        path = a[0]['href']
        anime = get_anime_detail(path)
        item = ListItem(anime['title'] + " " + a[len(a)-1].string)
        item.setArt({'poster': anime.pop('poster')})
        item.setInfo("video", anime)
        items.append((plugin.url_for(path), item, True))
        
    
    item = ListItem("Next >>")
    items.append((plugin.url_for("/ajax/page-recent-release-ongoing.html?page="+ str(pageNum + 1)), item, True))
    if pageNum != 1:
        item = ListItem("Back to main page")
        items.append((plugin.url_for("/"), item, True))

    InternalDatabase.close()
    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route(r"^/search.html\?((page=[0-9]+|keyword=[^&]+)&?)+")
@plugin.route(r"^/sub-category/([^&].+)\?page=[0-9]+$")
@plugin.route(r"^/genre/([^&].+)\?page=[0-9]+$")
@plugin.route(r'^/popular.html\?page=[0-9]+$')
def genericList():
    InternalDatabase.connect()
    if "/search.html" == plugin.path and "keyword" not in plugin.query:
        keyboard = Keyboard()
        keyboard.doModal()

        if keyboard.isConfirmed():
            keyword = keyboard.getText()
            response = request(plugin.pathqs + '&keyword=' + keyword)
        else:
            return
    else: 
        response = request(plugin.pathqs)

    pageNum = int(plugin.query['page'][0])
    document = BeautifulSoup(response.text, 'html.parser').find('div', class_="last_episodes").find('ul', class_="items")
    items = []
    for li in document.find_all('li'):
            a = li.find('a')
            path = a['href']
            anime = get_anime_detail(path)
            item = ListItem(anime['title'])
            item.setArt({'poster': anime.pop('poster')})
            item.setInfo("video", anime)
            items.append((plugin.url_for(path), item, True))
    
    item = ListItem("Next >>")
    if "/search.html" == plugin.path:
        if "keyword" in plugin.query:
            items.append((plugin.url_for(plugin.path + "?page="+ str(pageNum + 1) + '&keyword=' + plugin.query['keyword'][0]), item, True))
        else:
            items.append((plugin.url_for(plugin.path + "?page="+ str(pageNum + 1) + '&keyword=' + keyword), item, True))
    else:
        items.append((plugin.url_for(plugin.path + "?page="+ str(pageNum + 1)), item, True))
    if pageNum != 1:
        item = ListItem("Back to main page")
        items.append((plugin.url_for("/"), item, True))

    InternalDatabase.close()
    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/category/.+')
def category():
    ExternalDatabase.connect()
    ExternalDatabase.add(plugin.path)
    ExternalDatabase.close()
    response = request(plugin.path)
    items = []
    # plot = document.find('div', class_="anime_info_body_bg").find_all('p', class_="type")[1].contents[1]
    document = BeautifulSoup(response.text, 'html.parser')
    title = document.find('div', class_="anime_info_body_bg").find('h1').string
    for script in document.find_all('script'):
        if script.string is not None:
            it = re.search("var base_url_cdn_api = \'(.+)\'", script.string, flags=0)
            if it is not None:
                base_url_cdn_api = it.group(1)
                break

    episode_page = document.find('ul', id='episode_page')

    for episode_page_a in reversed(episode_page.find_all('a')):     
        ep_start = episode_page_a['ep_start']
        ep_end = episode_page_a['ep_end']
        id = document.find('input', id="movie_id")['value']
        default_ep = document.find('input', id="default_ep")['value']
        alias = document.find('input', id="alias_anime")['value']
        a = document.find('ul', id="episode_page").find('a')
        getEpsUrl = base_url_cdn_api + "ajax/load-list-episode?ep_start=" + ep_start + '&ep_end=' + ep_end + '&id=' + id + '&default_ep=' + default_ep + '&alias=' + alias

        response2 = session.get(getEpsUrl)
        document2 = BeautifulSoup(response2.text, 'html.parser')
        for li in document2.find_all('li'):
            a = li.find('a')
            div = a.find('div', class_="name")
            name = div.contents[0].string + div.contents[1]
            epTitle = title + " " + name
            item = ListItem(epTitle)
            item.setInfo('video', {"title": epTitle})
            item.setProperty('IsPlayable', 'true')
            items.append((plugin.url_for(a['href'].strip()), item, False))

    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.addDirectoryItems(plugin.handle, items, len(items))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('^(/.+)-episode-([0-9]+)$')
def play_episode():
    response = request(plugin.path)
    document = BeautifulSoup(response.text, 'html.parser')
    resolveurl.add_plugin_dirs(__plugins__)
    sources = []
    sources.append(resolveurl.HostedMediaFile(url=domain + plugin.path, title="GoGoCdn"))
    for server in document.find('div', class_="anime_muti_link").find_all('a'):
        if server.contents[1].name == 'i':
            title = server.contents[2]
        else:
            title = server.contents[1]
    #     source = ListItem(title)
    #     source.setProperty("data-video", server['data-video'])
    #     # if not 'hydrax' in server['data-video'] and not 'mp4upload' in server['data-video']:
    #     print(server['data-video'])
    #     if 'streamani.net/load.php' in server['data-video'] or 'streamani.net/streaming.php' in server['data-video']:
    #         sources.append(source)
    # position = Dialog().select("Choose server", sources)

    # if position != -1:
    #     # resolvedUrl = resolveUrl(sources[position].getProperty("data-video"))
    #     resolveurl.add_plugin_dirs(__plugins__)
    #     url = resolveurl.resolve(sources[position].getProperty("data-video"))
    #     print(url)
    #     xbmcplugin.setResolvedUrl(plugin.handle, True, ListItem(path=url))
        if title != "Vidstreaming" and title != "Gogo server":
            sources.append(resolveurl.HostedMediaFile(url=server['data-video'], title=title))
    
    sources = resolveurl.filter_source_list(sources)
    source = resolveurl.choose_source(sources)
    if source:
            print("selectedSource")
            print(source)
            url = source.resolve()
            print(url)
            xbmcplugin.setResolvedUrl(plugin.handle, True, ListItem(path=url))


# def resolveUrl(url):
#     servers = {
#         "VIDSTREAMING": "vidstreaming.io/streaming.php?id=NzEzMDM=&title=Hundred+Episode+1&typesub=SUB",
#         "GOGOSERVER": "vidstreaming.io/load.php?id",
#         "XSTREAMCDN": "fcdn.stream",
#         "MIXDROP": "mixdrop.co",
#         "CLOUD9": "cloud9.to",
#         "MP4UPLOAD": "mp4upload.com"
#     }
    

#     if servers["VIDSTREAMING"] in url:
#         response = requests.get(url)
#         document = BeautifulSoup(response.text, 'html.parser')
#         id = document.find('input', id="id")['value']
#         title = document.find('input', id="title")['value']
#         typesub = document.find('input', id="typesub")['value']
#         parsed_url = urlparse.urlparse(response.url)
#         url = parsed_url.scheme+"://"+parsed_url.hostname+ "/ajax.php?id=" + id+ "&title=" + title +"&typesub=" + typesub
#         response2 = requests.get(url)
#         jsonObj = json.loads(response2.text)
#         return jsonObj['source_bk'][0]['file']

#     elif servers["GOGOSERVER"] in url:
#         response = requests.get(url)
#         document = BeautifulSoup(response.text, 'html.parser')
#         script = document.find('div', class_="videocontent").find('script', type="text/JavaScript")
#         it = re.search("sources:\[{file: \'(.+)\',label:", script.string, flags=0)
#         if it is not None:
#             url = it.group(1)

#         response2 = requests.get(url, allow_redirects=False)
#         return response2.headers['Location']

#     elif servers["XSTREAMCDN"] in url:
#         parsedUrl = urlparse.urlparse(url).path.split("/")[-1:][0]
#         response = requests.post("https://fcdn.stream/api/source/"+ parsedUrl)
#         jsonObj = json.loads(response.text)
#         requestUrl = jsonObj['data'][0]['file']
#         response2 = requests.get(requestUrl, allow_redirects=False)
#         return response2.headers['Location']

#     elif servers["MP4UPLOAD"] in url:
#         response = requests.get(url)
#         document = BeautifulSoup(response.text, 'html.parser').find_all('script', type="text/javascript")
#         for script in document:
#             if script.string is not None and "eval(function(p,a,c,k,e,d)" in script.string:
#                 it = re.search(r"^eval\(function\(p,a,c,k,e,d\)(.+)\('(.+)',([0-9]+),([0-9]+),'(.+)'\.split\('\|'\)\)\)", script.string, flags=0)
#                 p = it.group(2)
#                 a = int(it.group(3))
#                 c = int(it.group(4))
#                 k = it.group(5).split("|")
#                 c-=1
#                 while c > 0:
#                     if k[c] is not None:
#                         p = re.sub("\\b"+int2base(c, a)+"\\b", k[c], p)
#                     c-=1
#                 it = re.search("sources:\[{src:\"(.+)\",type", p, flags=0)
#                 return it.group(1)

def get_anime_detail(path):
    anime = InternalDatabase.fetchone(path)

    if anime is None:
        response = request(path)
        document = BeautifulSoup(response.text, 'html.parser').find('div', class_="anime_info_body_bg")
        img = document.find('img')['src'].strip()
        title = document.find('h1').string.strip()
        pList = document.find_all('p', class_="type")
        plot = pList[1].contents[1].encode('utf-8').strip() if len(pList[1].contents) >= 2 else ''

        genre = ""
        for a in pList[2].find_all('a'):
            genre += a.string
        try:
            year = pList[3].contents[1].strip()
            year = int(year) if year.isdigit() else None
        except IndexError:
            year = None
        status = pList[4].contents[1].strip()

        InternalDatabase.add((path,
                              img,
                              title,
                              plot,
                              genre,
                              status,
                              year))
        anime = InternalDatabase.fetchone(path)

    return anime

def consumetRequest(episodeId):
    print(consumet + episodeId)
    response = requests.get(consumet + episodeId)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def request(path):
    response = session.get(domain + path)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response

def request2(path):
    response = session.get(domain2 + path)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response

if __name__ == '__main__':
    plugin.run()
