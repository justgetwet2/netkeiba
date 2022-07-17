import os
import pickle
from mysoup import get_dfs, get_soup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
# from subprocess import CREATE_NO_WINDOW # python 3.8で動かない

# from importlib.metadata import version
# print(version("subprocess"))

# p = "./data/jra_220716_updated.pickle"
# with open(p, "rb") as f:
#     races = pickle.load(f)

# for race in races:
#     print(race[:-2])

DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h50d1736_0/lib/python3.8/site-packages/chromedriver_binary/chromedriver"
# DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h32ec214_0/lib/site-packages/chromedriver_binary/chromedriver.exe"
service = fs.Service(executable_path=DRIVER, log_path=os.path.devnull)
# service.creationflags = CREATE_NO_WINDOW # 標準出力のログを表示させない
options = Options()
options.headless = True

url = "https://race.netkeiba.com/odds/index.html?type=b1&race_id=202202011111&rf=shutuba_submenu"
# dfs = get_dfs(url)
# winodds_df = dfs[0]
# soup = get_soup(url)
# table = soup.select_one("table")
# trs = table.select("tr")
# print(trs[1])


browser = webdriver.Chrome(service=service, options=options)
browser.get(url)
print("(^^) a headless browser is connected.")

table_element = browser.find_element(By.CLASS_NAME, "RaceOdds_HorseList_Table")
tr_elements = table_element.find_elements(By.TAG_NAME, "tr")

for i, element in enumerate(tr_elements):
    if not i: continue
    waku = element.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
    umaban = element.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
    horse = element.find_element(By.CSS_SELECTOR, "td.Horse_Name").text
    odds = element.find_element(By.CSS_SELECTOR, "span.Odds").text
    print(waku, umaban, horse, odds)

browser.quit()
print("(--)/ a headless browser is unconnected.")
