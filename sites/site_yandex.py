#
# Парсим yandex.ru/map
#

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs

from .class_site_parser import SiteParser


class SiteYandexClass(SiteParser):

    def parse(self):

        # загружаем полностью все ссылки на карточки
        # перемещаем фокус на 1ую ссылку на карточку (во фрэйм с карточками)
        xpath = "//a[@class='search-snippet-view__link-overlay _focusable']"
        fr_data = self.driver.find_element(By.XPATH, value=xpath)
        webdriver.ActionChains(self.driver).move_to_element(fr_data)
        time.sleep(1)
        len_before_END = -10

        # считаем сколько всего открыто карточек при старте
        soup = bs(self.driver.page_source, "lxml")
        len_after_END = len(soup.find_all("a",
            attrs={"class": "search-snippet-view__link-overlay _focusable"}))
        while len_before_END != len_after_END:
            len_before_END = len_after_END
            print(len_before_END, ">>> ", end="")
            # уходим на конец фрэйма. эмитируем нажатие END
            fr_data.send_keys(Keys.END)
            time.sleep(2)
            # опять считаем сколько всего открыто теперь карточек
            soup = bs(self.driver.page_source, "lxml")
            len_after_END = len(soup.find_all("a", attrs={"class":
                "search-snippet-view__link-overlay _focusable"}))
        print()

        soup = bs(self.driver.page_source, "lxml")
        all_carts = soup.find_all(
            "div", attrs={"class": "search-business-snippet-view"})
        for cart in all_carts:
            cart_div = bs(str(cart.contents[0]), "lxml")

            if cart_div.find("span", attrs={"class":
                "business-verified-badge _prioritized"}):
                type_of_public = "Премиум"
            else:
                type_of_public = "Обычный"

            self.result.append((
                    type_of_public,                     # тип публикации
                    cart.previous_sibling.text,         # название организации
                    cart.previous_sibling.get('href')   # url на карточку
                ))

    def ger_cart_id(self, url):
        return url.split("/")[4]

