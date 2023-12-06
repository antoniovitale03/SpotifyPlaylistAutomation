import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re


class FacebookSpotifyAutomation:

    def __init__(self, site, email, passw):
        self.driver = webdriver.Chrome(options=self.set_browser_options())
        self.site = site
        self.email = email
        self.passw = passw
        self.message = self.get_message()
        self.SCRIVI_QUALCOSA = "//div[@data-pagelet='GroupInlineComposer']//div[@role='button']"
        self.FORM_MESSAGGIO = ["//form[@method='POST']//div[@aria-label='Crea un post pubblico...']",
                               "//form[@method='POST']//div[@aria-label='Scrivi qualcosa...']"]
        self.PUBBLICA = "//form[@method='POST']//div[@aria-label='Pubblica']"

    def set_browser_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    def get_message(self):
        playlist_link = 'https://open.spotify.com/playlist/3u2GtcQOoIcPxnNKeXrQt4?si=86eaaa6b203a4cb5'
        return "Hello to all music lovers! I have decided to share with you my playlist that I have been curating for about two years: a set of songs that have struck me in different ways, a journey through my musical variety. I hope that my tastes also capture your attention: each song has been carefully chosen, bringing with it a unique emotion. If you find something you like, I'd love to receive a like and hear your opinions. And if you think your friends might like it too, share it! Music has the power to connect us and I'm excited to share this journey with you. Thanks for listening and being part of this experience! #PersonalPlaylist #LikeAndShare" + playlist_link


    def login(self, driver):
        driver.get(self.site)
        time.sleep(2)
        driver.find_element(By.XPATH, value="//button[@title='Consenti tutti i cookie']").click() #cookies button
        driver.find_element(By.XPATH, value="//*[@id='email']").send_keys(self.email) #email input
        driver.find_element(By.XPATH, value='//*[@id="pass"]').send_keys(self.passw) #password input
        driver.find_element(By.XPATH, value='//button[@name="login"]').click() #login button
        time.sleep(3)

    def scrolla_pagina(self, driver, n):
        for i in range(n):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def numero_gruppi(self, driver):
        span_element = driver.find_element(By.XPATH, '//span[starts-with(text(), "Tutti i gruppi di cui fai parte")]').text
        return int(re.search(r'\((\d+)\)', span_element).group(1))

    def crea_vettore_gruppi(self, driver):
        links = set()
        driver.get("https://www.facebook.com/groups/joins/?nav_source=tab")
        driver.maximize_window()
        num_gruppi = self.numero_gruppi(driver)
        while len(links) < num_gruppi:
            links.update(link.get_attribute("href") for link in self.driver.find_elements(By.XPATH, value="//a[@aria-label='Visualizza gruppo']"))
            self.scrolla_pagina(driver, 6)
        return list(links)

    def scrivi_qualcosa(self, driver):
        for element in driver.find_elements(By.XPATH, '//span'):
            if element.text in ["Scrivi qualcosa...", "Crea un post pubblico..."]:
                element.find_element(By.XPATH, value='./ancestor::div/ancestor::div').click()
                pause

    def form_messaggio(self, driver):
        try:
            driver.find_element(By.XPATH, value=self.FORM_MESSAGGIO[0]).send_keys(self.message)
        except selenium.common.exceptions.NoSuchElementException:
            driver.find_element(By.XPATH, value=self.FORM_MESSAGGIO[1]).send_keys(self.message)

    def post(self, driver):
        self.login(driver)
        links = self.crea_vettore_gruppi(driver)
        for link in links:
            try:
                driver.get(link)
                time.sleep(3)
                self.scrivi_qualcosa(driver)
                time.sleep(3)
                self.form_messaggio(driver)
                time.sleep(3)
                driver.find_element(By.XPATH, value=self.PUBBLICA).click()
                time.sleep(60)
            except selenium.common.exceptions.NoSuchElementException:
                pass
