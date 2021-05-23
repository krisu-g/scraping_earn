from selenium import webdriver
# selenium.webdriver.common.by.By :
# CLASS_NAME = 'class name'
# CSS_SELECTOR = 'css selector'
# ID = 'id'
# LINK_TEXT = 'link text'
# NAME = 'name'
# PARTIAL_LINK_TEXT = 'partial link text'
# TAG_NAME = 'tag name'
# XPATH = 'xpath'¶
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper_for_proxy import get_proxies
from icecream import ic

web = 'https://sports.tipico.de/en/live/soccer'
path = 'chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.page_load_strategy = 'normal'
driver = webdriver.Chrome(path)
proxies = get_proxies()
driver.get(web)
ic('Strona załadowana')
elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "_evidon-accept-button"))  #This is a dummy element
)
accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
accept.click()

# driver.quit()
