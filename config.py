"""

Чтение параметров программы. Сохранение пока не нужно.

"""

import yaml

cnf = None


def read_config():
    global cnf
    try:
        read_file = open("config.yaml", encoding="utf8")
        cnf = yaml.full_load(read_file)
        read_file.close()
    except FileNotFoundError:
        # если файла конфига не существует, то создаем его
        cnf = {
            "hide_chrome": False,
        }
        with open("config.yaml", "w", encoding="utf8") as write_file:
            yaml.dump(cnf, write_file)
    return cnf


if cnf is None:
    cnf = read_config()


if __name__ == "__main__":
    # самопроверка
    print(cnf)

    if cnf['hide_chrome']:
        print("11111")
    else:
        print("2222")
