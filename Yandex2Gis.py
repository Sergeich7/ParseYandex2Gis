# Программа в многопоточном режиме получает с сайтов 2gis.ru и yandex.ru/map
# названия боулингов Москвы (ну соответственно любых категорий, боулинги просто
# для проверки, их не сильно много) и ссылки на карточки этих организаций.

from concurrent.futures import ThreadPoolExecutor, wait

import sites

if __name__ == "__main__":

    parse_urls = (
        r"https://2gis.ru/moscow/search/%D0%91%D0%BE%D1%83%D0%BB%D0%B8%D0%BD%D0%B3/rubricId/170",
        r"https://yandex.ru/maps/213/moscow/search/%D0%91%D0%BE%D1%83%D0%BB%D0%B8%D0%BD%D0%B3/",
    )

    futures = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in parse_urls:
            futures.append(executor.submit(sites.launch_site_parse, url))
    wait(futures)
