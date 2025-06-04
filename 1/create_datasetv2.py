import requests
import csv
import random
import time

def get_books_from_search(query, page):
    url = f"https://openlibrary.org/search.json?q={query}&page={page}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("docs", [])
    except Exception as e:
        print("Error:", e)
    return []

# Letras comunes para búsqueda
queries = list("abcdefghijklmnopqrstuvwxyz")

books = []
seen_titles = set()

while len(books) < 100000:
    for q in queries:
        for page in range(1, 21):  # 20 páginas por letra = ~20000 libros por letra
            print(f"Buscando: q={q} | page={page} | libros actuales: {len(books)}")
            docs = get_books_from_search(q, page)
            for doc in docs:
                title = doc.get("title")
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)

                book = {
                    "isbn": doc.get("isbn", [f"{random.randint(1000000000000,9999999999999)}"])[0],
                    "title": title,
                    "publisher": doc.get("publisher", ["Editorial Ficticia"])[0],
                    "author": ", ".join(doc.get("author_name", ["Autor Desconocido"])),
                    "quantity": random.randint(1, 300),
                    "price": random.randint(5000, 80000)
                }
                books.append(book)

                if len(books) >= 100000:
                    break
            if len(books) >= 100000:
                break
            time.sleep(0.5)  # evitar sobrecargar la API
        if len(books) >= 100000:
            break
    if len(books) >= 100000:
        break

# Guardar como CSV
csv_path = "openlibrary_books_100k.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)

print(f"✅ Archivo generado con {len(books)} libros: {csv_path}")
