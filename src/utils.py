import pandas
import time
from pathlib import Path
from typing import List
from tqdm import tqdm
from model import Video


# Проверка на ошибки в URL
def check_youtube(url_loc: str) -> bool:
    if url_loc[:23] != "https://www.youtube.com" or url_loc[-7:] != "/shorts":
        print("\nСсылка не соответствует ссылке YouTube или это ссылка не на shorts.")
        print("Вот пример ссылки на shorts: https://www.youtube.com/@nickname/shorts\n")
        return True
    return False


# Сохранение результатов в csv формате
def save_to_csv(videos_list: List[Video], url: str) -> None:
    data_dir = Path.cwd() / "data"
    data_dir.mkdir(exist_ok=True)

    titles = [video.title for video in videos_list]
    links = [video.link for video in videos_list]
    views = [video.view for video in videos_list]

    df = pandas.DataFrame({
        'Title': titles,
        'Link': links,
        'View': views
    })

    path_csv = data_dir / f"data_{url[25:-7]}.csv"
    df.to_csv(path_or_buf=path_csv, index=False)

    # Бар с визуализацией загрузки
    for _ in tqdm(videos_list):
        time.sleep(0.01)

    print(f"\nВсе данные сохранены по пути '{path_csv.resolve()}'")
    print(f"\n{df.head(5)}")