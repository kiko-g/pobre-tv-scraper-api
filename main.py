import re
import bs4
import sys
import requests
from config import hdr


def scrape_tv_show(show_url):
    try:
        mainHtml = requests.get(show_url, headers=hdr).text
        mainDocument = bs4.BeautifulSoup(mainHtml, 'html.parser')
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
            seasons.append(episodes)

        return seriesName, seasons

    except requests.exceptions.ConnectionError:
        print("You've got problems with connection.", file=sys.stderr)


if __name__ == '__main__':
    show_url = 'https://www3.pobre.wtf/tvshows/tt1190634'
    seriesName, seasons = scrape_tv_show(show_url)

    print(seriesName)
    for season in seasons:
        if len(season) > 0:
            print("---------------------------")
        for episode in season:
            print(episode)
