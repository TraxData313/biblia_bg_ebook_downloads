import re

def convert_markdown_to_html():
    files = {
        1: 'Превод от 1940 г/Библия - Превод от 1940 г',
        2: 'Цариградски превод/Библия - Цариградски превод',
        3: 'King James Version/Bible - King James Version'
    }

    print(f'Избери превод:\n {files}')
    tr = int(input('>>> '))
    file = files[tr]
    input_file_txt  = f"{file}.txt"
    output_file_html = f"{file}.html"

    with open(input_file_txt, "r", encoding="utf-8") as f:
        text = f.read()

    current_book = ""
    current_chapter = ""

    lines = []
    for line in text.splitlines():
        # книга
        if line.startswith("# "):
            current_book = line[2:].strip()
            lines.append(f"<h1>{current_book}</h1>")
            continue

        # глава
        if line.startswith("## "):
            chap_match = re.match(r"##\s*(.+?)\s+(\d+)", line)
            if chap_match:
                current_book = chap_match.group(1).strip()
                current_chapter = chap_match.group(2).strip()
            continue

        # стих
        verse_match = re.match(r"^(\d+)(.*)", line)
        if verse_match and current_book and current_chapter:
            verse_num = verse_match.group(1)
            verse_text = verse_match.group(2).lstrip()
            abbrev = re.match(r"^(\d?\s?\w{1,3})", current_book)
            abbrev = abbrev.group(1) if abbrev else current_book[:3]
            new_line = f"{abbrev} {current_chapter}:{verse_num} {verse_text}"
            lines.append(new_line + "<br>")
            continue

        # празни или други
        if line.strip() == "":
            lines.append("")
        else:
            lines.append(line + "<br>")

    body_text = "\n".join(lines)

    html_text = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>{file.split('/')[-1]}</title>
</head>
<body>
<h2>{file.split('/')[-1]}</h2>
Източник на текста: https://biblia.bg<br>
Форматиране на електронната книга: https://github.com/TraxData313/biblia_bg_ebook_downloads<br>
<hr>
{body_text}
</body>
</html>
"""

    with open(output_file_html, "w", encoding="utf-8") as f:
        f.write(html_text)

    print("Готово:", output_file_html)


if __name__ == "__main__":
    convert_markdown_to_html()
