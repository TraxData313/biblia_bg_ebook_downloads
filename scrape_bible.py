import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://biblia.bg/index.php"


def get_book_list(tr=1):
    """Взима списъка с всички книги и техните ID-та от dropdown менюто."""
    resp = requests.get(BASE_URL, params={"k": 1, "g": 1, f"tr{tr}": 1})
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    books = []
    for option in soup.select("select[name=k] option"):
        book_id = int(option["value"])
        book_name = option.text.strip()
        books.append((book_id, book_name))
    return books


def fetch_chapter(book_id, chapter, tr=1):
    """Взима HTML за дадена книга и глава и връща текста на стиховете."""
    params = {"k": book_id, "g": chapter, f"tr{tr}": 1}
    resp = requests.get(BASE_URL, params=params)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    verses = []
    for div in soup.select("div.versions_text"):
        verses.append(div.get_text(strip=True))

    return verses


def scrape_bible(tr=1):
    output_files = {
        1: 'Превод от 1940 г/Библия - Превод от 1940 г.txt',
        2: 'Цариградски превод/Библия - Цариградски превод.txt',
        3: 'King James Version/Bible - King James Version.txt'
    }
    print(f'Избери превод:\n {output_files}')
    tr = int(input('>>> '))
    output_file = output_files[tr]
    books = get_book_list(tr=tr)
    with open(output_file, "w", encoding="utf-8") as f:
        for book_id, book_name in books:
            f.write(f"# {book_name}\n\n")

            chapter = 1
            while True:
                print(f"Свалям [{book_name}], глава [{chapter}]...                 ", end='\r', flush=True)
                verses = fetch_chapter(book_id, chapter, tr=tr)
                if not verses:
                    break  # няма повече глави
                f.write(f"## {book_name} {chapter}\n")
                for v in verses:
                    f.write(v + "\n")
                f.write("\n")
                chapter += 1
                time.sleep(0.5)  # пауза, за да не претоварваме сайта

    print("Готово! Резултатът е записан в", output_file)


if __name__ == "__main__":
    scrape_bible()



