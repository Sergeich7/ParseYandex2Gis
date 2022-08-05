#
# Основной (родитель) класс (общий функционал) парсинга сайтов
#

import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

import config


def url2sitename(url):
    return url.split("/")[2].split(".")[-2]


class SiteParser:

    def __init__(self, url=""):

        self.url = url
        self.sitename = url2sitename(url)

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        if config.cnf["hide_chrome"]:
            # скрываем хром если мешает
            self.options.add_argument("--headless")

        self.services = Service('chromedriver.exe')

        self.driver = webdriver.Chrome(
            options=self.options, service=self.services)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(35)

        # переходим на сайт
        self.driver.get(url)

        self.wait_el = WebDriverWait(self.driver, 10)

        # сохраняем результат
        self.result = []

        print("url: ", url)
        print("Старт")

    def get_cart_id(self, url):
        # Просто генерим рандомно
        # в дальнейшем будем доставать по возможности из url
        return str(int(random.random()*1000000000000))

    def save(self):
        self.driver.quit()
        print("Стоп")

        with open(self.sitename + ".txt", "w", encoding="utf8") as f:
            for [r_type, r_name, r_url] in self.result:
                r_id = f"{self.sitename}-{self.get_cart_id(r_url)}"
                if "http" not in r_url:
                    # url - относительный
                    # декорируем - добавляем https://site.name
                    t = self.url.split("/")
                    r_url = f"{t[0]}//{t[2]}{r_url}"
#                f.write(str((r_id, r_type, r_name, r_url)) + '\n')
                f.write(str((r_id, r_name, r_url)) + '\n')

        print("Записано")
