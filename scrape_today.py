import numpy as np
import pandas as pd
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
    urls = []
    for s in racelist:
        hold, place, dt = s.split()
        c = yyyy + cc[place] + hold.strip("回").rjust(2, "0") + dt.strip("日目").rjust(2, "0")
        urls.append(c)

    for i, url in enumerate(urls):
        if i: continue
        for j in range(1, 13):
            # if j != 1: continue
            raceurl = entry_url + url + str(j).rjust(2, "0")
            soup = get_soup(raceurl)
            r = soup.select_one("div[class^='RaceList_Item']").select_one(".RaceNum").text
            racename = soup.select_one("div.RaceList_Item02 .RaceName").text.strip()
            print(r, racename)
            tag = soup.select_one("div.RaceList_Item02 .RaceData01")
            print(tag.contents[3].split("/")[1].strip())
            print(tag.select("span")[0].text.strip() + tag.contents[3].split("/")[0].strip())
            print(tag.select_one("span[class^='Item']").text.replace("/", "").strip())
            print(tag.text.split()[0])
            print(soup.select_one("div.RaceList_Item02 .RaceData02").select("span")[-2].text)

            # print(soup.prettify()[3000:9000])
            # print(soup.title) # <title>３歳以上障害未勝利 出馬表 | 2022年7月16日 福島1R レース情報(JRA) - netkeiba.com</title>
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

