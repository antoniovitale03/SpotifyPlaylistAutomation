from selenium import webdriver
from selenium.webdriver.common.by import By


def set_browser_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options

driver = webdriver.Chrome(options=set_browser_options())
driver.get("https://spotify.com")