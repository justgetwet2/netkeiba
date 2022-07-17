import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs

DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h50d1736_0/lib/python3.8/site-packages/chromedriver_binary/chromedriver"
# DRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h32ec214_0/lib/site-packages/chromedriver_binary/chromedriver.exe"
service = fs.Service(executable_path=DRIVER, log_path=os.path.devnull)
options = Options()
options.headless = True

netkeiba_url = "https://race.netkeiba.com/"
odds_url = "odds/index.html?type=b1&race_id="

def netkeiba_odds(race_id):

    def is_num(s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True

    url = netkeiba_url + odds_url + race_id

    browser = webdriver.Chrome(service=service, options=options)
    browser.get(url)
    print("(^^) a headless browser is connected.")

    table_elements = browser.find_elements(By.CLASS_NAME, "RaceOdds_HorseList_Table")
    w_elements = table_elements[0].find_elements(By.TAG_NAME, "tr")
    p_elements = table_elements[1].find_elements(By.TAG_NAME, "tr")

    odds_d = {}
    for i, (w_element, p_element) in enumerate(zip(w_elements, p_elements)):
        if not i: continue
        # print(w_element.find_element(By.CLASS_NAME, "Horse_Info"))
        waku = w_element.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        umaban = w_element.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        horse = w_element.find_element(By.CSS_SELECTOR, "td.Horse_Name").text
        win_odds = w_element.find_element(By.CSS_SELECTOR, "td.Odds").text
        place_odds = p_element.find_element(By.CSS_SELECTOR, "td.Odds").text
        
        print(waku, umaban, horse, win_odds, place_odds)
        
        float_win_odds, float_place1_odds, float_place2_odds = None, None, None
        if is_num(win_odds):
            float_win_odds = float(win_odds)
            float_place1_odds = float(place_odds.split("-")[0].strip())
            float_place2_odds = float(place_odds.split("-")[1].strip())

        odds_d[umaban] = float_win_odds
        odds_d["(" + umaban] = float_place1_odds
        odds_d[umaban + ")"] = float_place2_odds

    browser.quit()
    print("(--)/ a headless browser is unconnected.")

    return odds_d

if __name__ == "__main__":

    race_id = "202203020506"
    odds_d = netkeiba_odds(race_id)
    print(odds_d)