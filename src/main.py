import pandas
from art import tprint

from parser import parser
from utils import check_youtube, save_to_csv


if __name__ == "__main__":
    tprint("Welcome to Parser")
    try:
        while True:
            print("\nЧто вы хотите сделать? (parser - 1; open - 2; exit - 3)")
            choice = input()

            if choice.strip() == "1" or choice.lower().strip() == "parser":
                while True:
                    print("Введите ссылку на страницу с shorts:")
                    url = input()
                    if not check_youtube(url):
                        videos_list = parser(url)
                        if videos_list:
                            save_to_csv(videos_list=videos_list, url=url)
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
                        data = pandas.read_csv(f"data\\data_{nick}.csv")

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
    except KeyboardInterrupt:
        print("Программа завершена пользователем.")