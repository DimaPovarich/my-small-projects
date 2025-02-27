import requests
from bs4 import BeautifulSoup

def translate_text(text, lang_from, lang_to):
    try:
        # Создаем URL запроса
        url = f"https://translate.google.com/m?hl={lang_to}&sl={lang_from}&q={text.replace(' ', '+')}"
        
        # Выполняем запрос к Google Translate
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers)
        
        # Проверяем статус ответа
        if response.status_code != 200:
            print("Ошибка подключения к серверу.")
            return None
        
        # Парсим страницу с результатами
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find('div', class_='result-container').text
        
        return result

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def main():
    print("Выберите способ ввода текста:")
    print("1. Ввести текст вручную")
    print("2. Указать путь к файлу")
    choice = input("Выберите (1/2): ")

    # Ввод языка текста и перевода
    lang_from = input("Введите код исходного языка (например, en): ").strip()
    lang_to = input("Введите код языка перевода (например, ru): ").strip()

    # Получаем текст для перевода
    if choice == '1':
        text = input("Введите текст для перевода: ")
    elif choice == '2':
        filepath = input("Введите путь к файлу: ")
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print("Файл не найден.")
            return
    else:
        print("Неверный выбор.")
        return

    # Перевод текста
    result = translate_text(text, lang_from, lang_to)
    if result:
        print("\nПеревод:")
        print(result)


if __name__ == "__main__":
    main()
