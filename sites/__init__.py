

from .class_site_parser import url2sitename

# для каждого сайта импортируем свой класс
from .site_yandex import SiteYandexClass
from .site_2gis import Site2GisClass

site_classes = {
    "yandex": SiteYandexClass,
    "2gis": Site2GisClass,
}


def launch_site_parse(url):
    # определяет по url сайт и создает и запускает соответствующий парсер
    site_key = url2sitename(url)
    sc = site_classes[site_key](url)
    sc.parse()
    sc.save()


__all__ = [
    SiteYandexClass,
    Site2GisClass,
    ]
    