import pickle
from mysoup import get_dfs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from subprocess import CREATE_NO_WINDOW
# p = "./data/jra_220716_updated.pickle"
# with open(p, "rb") as f:
#     races = pickle.load(f)

# for race in races:
#     print(race[:-2])

DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h32ec214_0/lib/site-packages/chromedriver_binary/chromedriver.exe"
service = fs.Service(executable_path=DRIVER)
service.creationflags = CREATE_NO_WINDOW # 標準出力のログを表示させない
options = Options()
options.headless = True

url = "https://race.netkeiba.com/odds/index.html?type=b1&race_id=202202011111&rf=shutuba_submenu"
dfs = get_dfs(url)
winodds_df = dfs[0]

browser = webdriver.Chrome(service=service, options=options)
browser.get(url)
print("connected.")

for i in range(len(winodds_df)):
    umaban = str(i+1).rjust(2, "0")
    xp = f'//*[@id="odds-1_{umaban}"]'
    # print(xp)
    element = browser.find_element(By.XPATH, xp)
    waku = winodds_df.loc[i, "枠"]
    horse = winodds_df.loc[i, "馬名"]
    print(waku, str(i+1), horse, element.text)

browser.quit()
print("unconnected.")
