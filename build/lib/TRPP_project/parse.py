import time                                            # Импортируем модуль time
from selenium import webdriver                         # Импортируем Веб Драйвер
from selenium.webdriver.common.by import By            # Имопортируем класс для поиска элементов
from selenium.webdriver.common.keys import Keys        # Импортируем обработчик нажатия кнопок
from PIL import Image                                  # Импортируем библиотеку для работы с изображением
from data import USER_AGENT, URL                       # Импортируем константы


def parse(point_from, point_to):
    '''Parsing unction getting data from 2gis.ru using selenium

    :param point_from: first adress
    :type point_from: str
    :param point_to: second adress
    :type point_to: str
    :return res: Returning dictionary of distance, duration and photo
    :rtype res: dict
    '''
    options = webdriver.ChromeOptions()
    # Добавляем User-Agent в настройки
    options.add_argument(USER_AGENT)
    options.add_argument("--headless")
    # Отключаем режим Веб Драйвера
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Подавление Getting Default Adapter failed
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # Создание Веб Драйвера
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1000, 1000)
    data_dict = {}
    try:
        # Открываем вкладку с ссылкой url
        driver.get(url=URL)
        time.sleep(1)
        # Ввод первого адреса
        from_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/input')
        from_input.clear()
        from_input.send_keys(point_from)
        time.sleep(1)
        from_input.send_keys(Keys.RETURN)
        # Ввод второго адреса
        to_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/input')
        to_input.clear()
        to_input.send_keys(point_to)
        time.sleep(1)
        to_input.send_keys(Keys.ENTER)
        time.sleep(1)
        # Сбор данных в словарь
        data_dict["time"] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div/div[2]/div[1]').text
        data_dict["dist"] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/div/div[1]/div[2]/div/div[2]/div[2]').text
        data_dict["screen"] = "screens/screen.png"
        # Обработка скриншота
        driver.save_screenshot(data_dict["screen"])
        img = Image.open(data_dict["screen"])
        img = img.crop((350, 0, 1000, 1000))
        img.save(data_dict["screen"])
        time.sleep(0.5)
        return data_dict
    except Exception as Ex:          # Проверка на ошибки
        print(Ex)                    # Вывод ошибок
        return "ERROR! Somthing went wrong!"
    finally:
        driver.close()               # Закрытие вкладки
        driver.quit()                # Выключение драйвера
