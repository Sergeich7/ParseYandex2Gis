#
# Парсим 2gis.ru
#

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs

from .class_site_parser import SiteParser


class Site2GisClass(SiteParser):

    def parse(self):

        # закрываем окошко с предупреждением о cookies
        xpath_cookies_btn = "//div[@class='_euwdl0']"
        el_next_page = self.driver.find_element(
            By.XPATH, value=xpath_cookies_btn)
        if el_next_page:
            wbd = webdriver.ActionChains(
                self.driver).move_to_element(el_next_page)
            time.sleep(1)
            wbd.click(el_next_page).perform()
            time.sleep(1)

        fl_next = True      # флаг выхода из цикла
        while fl_next:

            # нахоим все дивы карточек
            soup = bs(self.driver.page_source, "lxml")
            all_carts_on_page = soup.find_all(
                "div", attrs={"class": "_1hf7139"})
            # перебираем все дивы карточек
            for cart in all_carts_on_page:

                # url на карточку
                cart_div = bs(str(cart.contents[1]), "lxml")

                # url на карточку
                cart_a = cart_div.find("a", attrs={"class": "_1rehek"})
                url = cart_a.get('href').split("?")[0]

                # тип отображения
                cart_div = bs(str(cart.contents[-1]), "lxml")
                if cart_div.find("span", attrs={"class": "_1k70kjvn"}):
                    type_of_public = "Премиум"
                else:
                    type_of_public = "Обычный"

                self.result.append((
                        type_of_public,     # тип публикации
                        cart_a.text,        # название организации
                        url                 # url на карточку организации
                    ))

            print(len(self.result), '>>> ', end="")

            if (    # если не находим стрелку на следующую страницу - выходим
                    (not soup.find(
                        "svg", attrs={"style": "transform:rotate(-90deg)"}))
                    # или если находим кнопку 'добавить организацию' - выходим
                    or (soup.find("button", attrs={"class": "_6gpij7j"}))):
                fl_next = False
                print()
            else:
                # идем на следующую страницу
                els_page_nav = self.driver.find_elements(
                    By.XPATH, value="//div[@class='_n5hmn94']")
                wbd = webdriver.ActionChains(
                    self.driver).move_to_element(els_page_nav[-1])
                time.sleep(1)
                wbd.click(els_page_nav[-1]).perform()
                time.sleep(1)

    def ger_cart_id(self, url):
        return url.split("/")[3]
