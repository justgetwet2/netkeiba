import datetime
import numpy as np
import pandas as pd
import pickle
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs

from mysoup import get_soup, get_dfs, netkeiba_url

yyyy = "2022"

cc = {}
cc['札幌'] = '01'
cc['函館'] = '02'
cc['福島'] = '03'
cc['新潟'] = '04'
cc['東京'] = '05'
cc['中山'] = '06'
cc['中京'] = '07'
cc['京都'] = '08'
cc['阪神'] = '09'
cc['小倉'] = '10'

def get_racelist():
    DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h50d1736_0/lib/python3.8/site-packages/chromedriver_binary/chromedriver"
    # DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h32ec214_0/lib/site-packages/chromedriver_binary/chromedriver.exe"
    service = fs.Service(executable_path=DRIVER)
    options = Options()
    options.headless = True

    browser = webdriver.Chrome(service=service, options=options)
    browser.get(netkeiba_url)
    print("(^^) a headless browser is connected.")
    elements = browser.find_elements(By.CSS_SELECTOR, "dl.RaceList_DataList")
    cs = "dt:nth-child(1) > div:nth-child(1) > p:nth-child(1)"
    racelist = [element.find_element(By.CSS_SELECTOR, cs).text for element in elements]
    browser.quit()
    print("(--)/ a headless browser is unconnected.")
    
    return racelist

if __name__ == "__main__":

    entry_url = "race/shutuba.html?race_id="
    racelist = get_racelist()
    # racelist = ['2回 福島 5日目', '3回 小倉 5日目', '1回 函館 11日目']
    days = []
    for s in racelist:
        times, place, dth = s.split()
        hold = "第" + times.strip("回").rjust(2, "0") + "回" + place + dth.strip("日目").rjust(2, "0")
        hold_id = yyyy + cc[place] + times.strip("回").rjust(2, "0") + dth.strip("日目").rjust(2, "0")
        days.append((hold, hold_id))
    
    races = []
    for i, (hold, hold_id) in enumerate(days):
        # if i: continue
        url01 = netkeiba_url + entry_url + hold_id + "01"
        soup = get_soup(url01)
        yymmdd = ""
        for e in soup.title.text.split():
            if re.match("20[0-9]+年[0-9]+月[0-9]+日", e.strip()):
                dt = datetime.datetime.strptime(e.strip(), "%Y年%m月%d日")
                yymmdd = dt.strftime("%y/%m/%d")

        for j in range(1, 13):
            # if j - 1: continue
            race_id = hold_id + str(j).rjust(2, "0")
            race_url = entry_url + race_id
            soup = get_soup(netkeiba_url + race_url)
            # print(soup.title)
            r = soup.select_one("div[class^='RaceList_Item']").select_one(".RaceNum").text
            r = r.rjust(3, "0")
            racename = soup.title.text.split()[0]
            # racename = soup.select_one("div.RaceList_Item02 .RaceName").text.strip()
            tag = soup.select_one("div.RaceList_Item02 .RaceData01")

            course = tag.select("span")[0].text.strip() + tag.contents[3].split("/")[0].strip()
            head_count = soup.select_one("div.RaceList_Item02 .RaceData02").select("span")[-2].text
            start_time = tag.text.split()[0].strip("発走")
            weather = tag.contents[3].split("/")[1].strip()
            condition = tag.select_one("span[class^='Item']").text.replace("/", "").strip()
            condition = weather.split(":")[1] + "/" + condition.split(":")[1]

            table = soup.select_one("table.Shutuba_Table")
            wakuban = [tag.text for tag in table.select("td[class^='Waku'] span")]
            umaban = [tag.text for tag in table.select("td[class^='Umaban']")]
            h_tags = table.select("span.HorseName a")
            horse_name = [tag.text for tag in h_tags]
            horse_url = [tag.get("href") for tag in h_tags]
            j_tags = table.select("a[href^='https://db.netkeiba.com/jockey/result']")
            jockey_name = [tag.text for tag in j_tags]
            jockey_code = [tag.get("href").split("/")[-2] for tag in j_tags]
            
            data = wakuban, umaban, horse_name, jockey_name, horse_url, jockey_code
            columns = "枠番", "馬番", "馬名", "騎手", "馬url", "騎手code"
            df = pd.DataFrame(np.array(data).T, columns=columns)

            t = yymmdd, hold, r, racename, course, head_count, start_time, condition, race_id, df, {}
            print(" ".join(t[:-2]))
            races.append(t)

    p = "./data/jra_" + yymmdd.replace("/", "") + "_updated.pickle"
    with open(p, "wb") as f:
        pickle.dump(races, f, pickle.HIGHEST_PROTOCOL)
