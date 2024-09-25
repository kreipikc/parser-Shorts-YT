import pandas
import time
import os
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from art import tprint

# Проверка на ошибки в URL
def check_youtube(url_loc: str) -> bool:
    if url_loc[:23] != "https://www.youtube.com" or url_loc[-7:] != "/shorts":
        print("\nСсылка не соответствует ссылке YouTube или это ссылка не на shorts.")
        print("Вот пример ссылки на shorts: https://www.youtube.com/@nickname/shorts\n")
        return True
    return False

# Основная функция с логикой parser'а
def parser(url_local: str) -> List[List[str]]:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url_local)

        button = driver.find_element(By.CSS_SELECTOR, 'button[jsname="tWT92d"]')
        if button:
            button.click()

        driver.implicitly_wait(10)
        contents = driver.find_element(By.ID, "contents")

        links = []
        title = []
        view = []

        while True:
            video_element = contents.find_elements(By.ID, "content")
            for el in video_element:
                el_link = el.find_element(By.TAG_NAME, "a")
                el_title = el.find_element(By.TAG_NAME, "span")
                el_view = el.find_element(By.XPATH, 'ytm-shorts-lockup-view-model-v2/ytm-shorts-lockup-view-model/div/div[@class="ShortsLockupViewModelHostMetadataSubhead ShortsLockupViewModelHostOutsideMetadataSubhead"]/span')

                if el_link.get_attribute("href") and el_link.get_attribute("href") not in links:
                    links.append(el_link.get_attribute("href"))
                    title.append(el_title.text)
                    view.append(el_view.text)

            # Если видео на начальной странице больше чем 48 -> делаем scroll
            if len(video_element) >= 48:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

                time.sleep(3)

                new_video_element = contents.find_elements(By.ID, "content")
                if len(new_video_element) == len(video_element):
                    break
                else:
                    video_element = new_video_element
            else:
                break
        return [links, title, view]
    except Exception as e:
        print(f"Error: {e}")
        return [[], [], []]

# Сохранение результатов в csv формате
def save_to_csv(link: [str], title: [str], view: [str]) -> None:
    df = pandas.DataFrame(list(zip(title, link, view)), columns=['Title', 'Link', 'View'])
    if not os.path.isdir("data"):
        os.mkdir("data")
    df.to_csv(f"data/data_{url[25:-7]}.csv", index=False)

    # Бар с визуализацией загрузки
    for _ in tqdm(title):
        time.sleep(0.01)

    print(f'\nВсе данные сохранены по пути "{os.path.dirname(os.path.abspath(__file__))}\data\data_{url[25:-7]}.csv"')
    print(f"\n{df}")


if __name__ == "__main__":
    tprint("Welcome to Parser")
    while True:
        print("\nЧто вы хотите сделать? (parser - 1; open - 2; exit - 3)")
        choice = input()

        if choice.strip() == "1" or choice.lower().strip() == "parser":
            while True:
                print("Введите ссылку на страницу с shorts:")
                url = input()
                if not check_youtube(url):
                    link_list, title_list, view_list = parser(url)
                    if link_list != [] and title_list != [] and view_list != []:
                        save_to_csv(link_list, title_list, view_list)
                        break
                    else:
                        print("Empty result.\n")
                elif url.strip().lower() == "exit": exit(0)
                else:
                    print("Неверно введена ссылка.\nПроверьте написание и попробуйте снова.\n")
        elif choice.strip() == "2" or choice.lower().strip() == "open":
            while True:
                try:
                    print("Введите ник:")
                    nick = input()
                    data = pandas.read_csv(f"data/data_{nick}.csv")

                    print("\nВсе значения(1) или только часть(2)?")
                    while True:
                        var = input()

                        if var.strip() == "1" or var.lower().strip() == "все значения":
                            print(data.to_string())
                            break
                        elif var.strip() == "2" or var.lower().strip() == "часть":
                            print(data)
                            break
                        elif var.strip().lower() == "exit":
                            exit(0)
                        else:
                            print("\nОшибка. Введите '1' или '2'.")
                    break
                except FileNotFoundError:
                    print("Ник введен не верно.\nПроверьте написание и попробуйте ещё раз.\n")
        elif choice.strip() == "3" or choice.lower().strip() == "exit": exit(0)
        else:
            print("Неверно ввели значение.\n")