from bs4 import BeautifulSoup
import bs4
import pandas as pd
import requests
ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}

def get_soup(url: str) -> bs4.BeautifulSoup:
    try:
        res = requests.get(url, headers=ua)
    except requests.RequestException as e:
        print("Error: ", e)
    else:
        return BeautifulSoup(res.content, "html.parser")

def get_dfs(url: str) -> list:
    dfs = []
    soup = get_soup(url)
    if soup:
        if soup.find("table"):
            dfs = pd.io.html.read_html(soup.prettify())
        else:
            print(f"It's no table! {url}")
    return dfs

netkeiba_url =  "https://www.netkeiba.com/"

if __name__ == "__main__":

    soup = get_soup(netkeiba_url)
    print(soup.title)
    # <title>netkeiba.com - 国内最大級の競馬情報サイト</title>