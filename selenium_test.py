from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs

url = "https://race.netkeiba.com/"

CHROMEDRIVER = "../python-chromedriver-binary-103.0.5060.53.0-py38h50d1736_0/lib/python3.8/site-packages/chromedriver_binary/chromedriver"
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
options = Options()
options.headless = True

browser = webdriver.Chrome(service=chrome_service, options=options)
browser.get(url)
elements = browser.find_elements(By.CSS_SELECTOR, "dl.RaceList_DataList")
cs = "dt:nth-child(1) > div:nth-child(1) > p:nth-child(1)"
race_list = [element.find_element(By.CSS_SELECTOR, cs).text for element in elements]

browser.quit()
