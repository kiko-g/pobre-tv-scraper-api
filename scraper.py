import re
import bs4
import sys
import requests
import aiohttp
import asyncio
from config import headers
from logger import log_tv_show


async def get_html(show_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(show_url) as resp:
            html = await resp.text()
    return html


async def scrape_tv_show(show_url):
    try:
        show_html = await get_html(show_url)
        mainDocument = bs4.BeautifulSoup(show_html, 'html.parser')
        seriesName = mainDocument.find('section').find('h1').text

        htmlTarget = mainDocument.find(id='seasonsList')
        seasonUrls = [f'{show_url}/season/1#seasons']
        for seasonHtml in htmlTarget.find_all(class_="item"):
            seasonUrls.append(seasonHtml['href'])

        seasons = []
        for seasonUrl in seasonUrls:
            episodes = []
            seasonHtml = requests.get(seasonUrl).text
            seasonDocument = bs4.BeautifulSoup(seasonHtml, 'html.parser')
            seasonTarget = seasonDocument.find(id='episodesList')
            for episodeHtml in seasonTarget.find_all('a'):
                episodes.append({
                    "name": episodeHtml.text.strip(),
                    "image": re.search('url\\((.*)\\)', episodeHtml.find(class_="img")['style']).group(1)
                })
            if len(episodes) > 0:
                seasons.append(episodes)

        return seriesName, seasons

    except requests.exceptions.ConnectionError:
        print("You've got problems with connection.", file=sys.stderr)


if __name__ == '__main__':
    show_url = 'https://www3.pobre.wtf/tvshows/tt11198330'
    seriesName, seasons = asyncio.run(scrape_tv_show(show_url))

    log_tv_show(seriesName, seasons)
