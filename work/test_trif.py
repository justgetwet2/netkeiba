
from mysoup import get_soup

url = "https://race.netkeiba.com/odds/index.html?type=b8&race_id=202202011111&housiki=c0&rf=shutuba_submenu"

soup = get_soup(url)
tags = soup.select("option")
for tag in tags:
    print(tag)
