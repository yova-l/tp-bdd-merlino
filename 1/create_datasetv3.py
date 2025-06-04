import requests
import csv
import random
import time

subjects = [
    "fantasy", "science_fiction", "romance", "history", "mystery",
    "thriller", "horror", "biography", "children", "young_adult",
    "drama", "travel", "sports", "music", "poetry"
]

books = []
seen_titles = set()

def fetch_subject_books(subject, offset):
    url = f"https://openlibrary.org/subjects/{subject}.json?limit=1000&offset={offset}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("works", [])
    except Exception as e:
        print("Error:", e)
    return []

for subject in subjects:
    print(f"Consultando subject: {subject}")
    for offset in range(0, 10000, 1000):  # hasta 10k libros por categoría
        print(f" -> offset={offset} | libros actuales: {len(books)}")
        works = fetch_subject_books(subject, offset)
        for work in works:
            title = work.get("title")
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)

            book = {
                "isbn": f"{random.randint(1000000000000, 9999999999999)}",
                "title": title,
                "publisher": random.choice(["Penguin", "Anagrama", "Alfaguara", "Planeta", "Minotauro"]),
                "author": ", ".join([a["name"] for a in work.get("authors", [])]) or "Autor desconocido",
                "quantity": random.randint(1, 300),
                "price": random.randint(5000, 80000)
            }
            books.append(book)

            if len(books) >= 100000:
                break
        if len(books) >= 100000:
            break
        time.sleep(0.5)
    if len(books) >= 100000:
        break

# Guardar CSV
csv_path = "openlibrary_books_100k.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)

print(f"✅ ¡Archivo generado con {len(books)} libros!: {csv_path}")
