import time
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from model import Video


# Основная функция с логикой parser'а
def parser(url_local: str) -> Optional[List[Video]]:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url_local)

        # Если у вас есть кнопка с подтверждением при отрытии страницы YouTube - раскомментировуйте
        # button = driver.find_element(By.CSS_SELECTOR, 'button[jsname="tWT92d"]')
        # if button:
        #     button.click()

        driver.implicitly_wait(10)
        contents = driver.find_element(By.ID, "contents")

        videos = []
        links = []

        while True:
            video_element = contents.find_elements(By.ID, "content")
            for el in video_element:
                el_link = el.find_element(By.TAG_NAME, "a")
                el_title = el.find_element(By.TAG_NAME, "span")
                el_view = el.find_element(By.XPATH, 'ytm-shorts-lockup-view-model-v2/ytm-shorts-lockup-view-model/div/div[@class="ShortsLockupViewModelHostMetadataSubhead ShortsLockupViewModelHostOutsideMetadataSubhead"]/span')

                if el_link.get_attribute("href") and el_link.get_attribute("href") not in links:
                    videos.append(Video(link=el_link.get_attribute("href"), title=el_title.text, view=el_view.text))

                    # Для отсутствия дубликатов (для проверки при добавлении)
                    links.append(el_link.get_attribute("href"))

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
        return videos
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
        driver.quit()