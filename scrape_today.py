import datetime
import numpy as np
import pandas as pd
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
    CHROMEDRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h50d1736_0/lib/python3.8/site-packages/chromedriver_binary/chromedriver"
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    options = Options()
    options.headless = True

    browser = webdriver.Chrome(service=chrome_service, options=options)
    browser.get(netkeiba_url)
    print("connected.")
    elements = browser.find_elements(By.CSS_SELECTOR, "dl.RaceList_DataList")
    cs = "dt:nth-child(1) > div:nth-child(1) > p:nth-child(1)"
    racelist = [element.find_element(By.CSS_SELECTOR, cs).text for element in elements]
    # -> ['2回 福島 5日目', '3回 小倉 5日目', '1回 函館 11日目']
    browser.quit()

    return racelist

if __name__ == "__main__":

    entry_url = "https://race.netkeiba.com/race/shutuba.html?race_id="
    # racelist = get_racelist()
    racelist = ['2回 福島 5日目', '3回 小倉 5日目', '1回 函館 11日目']
    races = []
    for s in racelist:
        times, place, dth = s.split()
        hold = place + times + "_" + dth.strip("目")
        url = yyyy + cc[place] + times.strip("回").rjust(2, "0") + dth.strip("日目").rjust(2, "0")
        races.append((hold, url))
    
    for i, (hold, url) in enumerate(races):
        # if i: continue
        url01 = entry_url + url + "01"
        soup = get_soup(url01)
        yymmdd = ""
        for e in soup.title.text.split():
            if re.match("20[0-9]+年[0-9]+月[0-9]+日", e.strip()):
                dt = datetime.datetime.strptime(e.strip(), "%Y年%m月%d日")
                yymmdd = dt.strftime("%y%m%d")

        for j in range(1, 13):
            # if j != 1: continue
            raceurl = entry_url + url + str(j).rjust(2, "0")
            soup = get_soup(raceurl)
            # print(soup.title)
            r = soup.select_one("div[class^='RaceList_Item']").select_one(".RaceNum").text
            racename = soup.title.text.split()[0]
            # racename = soup.select_one("div.RaceList_Item02 .RaceName").text.strip()
            tag = soup.select_one("div.RaceList_Item02 .RaceData01")

            course = tag.select("span")[0].text.strip() + tag.contents[3].split("/")[0].strip()
            head_count = soup.select_one("div.RaceList_Item02 .RaceData02").select("span")[-2].text
            weather = tag.contents[3].split("/")[1].strip()
            condition = tag.select_one("span[class^='Item']").text.replace("/", "").strip()
            start_time = tag.text.split()[0]

            print(yymmdd, hold, r, racename, course, head_count, weather, condition, start_time)

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
            # print(df)

