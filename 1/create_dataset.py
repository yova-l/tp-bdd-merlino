import requests
import random
import csv
import time

def fetch_author_works(author_id, max_works=100):
    url = f"https://openlibrary.org/authors/{author_id}/works.json?limit={max_works}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("entries", [])
    except Exception:
        pass
    return []

author_ids = [
    "OL23919A", "OL26320A", "OL2162288A", "OL34184A", "OL382982A",
    "OL26321A", "OL44590A", "OL18319A", "OL31574A", "OL79022A",
]

seen_titles = set()
books = []

for author_id in author_ids:
    works = fetch_author_works(author_id, max_works=1000)
    for work in works:
        title = work.get("title", "").strip()
        if not title or title in seen_titles:
            continue
        seen_titles.add(title)

        book = {
            "isbn": f"{random.randint(1000000000000, 9999999999999)}",
            "title": title,
            "publisher": random.choice(["Penguin", "HarperCollins", "Random House", "Planeta", "Anagrama"]),
            "author": author_id,
            "quantity": random.randint(1, 200),
            "price": random.randint(5000, 80000)
        }
        books.append(book)

        if len(books) >= 50000:
            break
    if len(books) >= 50000:
        break
    time.sleep(1)

# Guardar como CSV
with open("openlibrary_books.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)

print("Archivo CSV generado: openlibrary_books.csv")
