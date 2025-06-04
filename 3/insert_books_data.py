import pandas as pd
import psycopg2

try:
    # Cargar CSVs
    df_publishers = pd.read_csv("publishers.csv")
    df_authors = pd.read_csv("authors.csv")
    df_books = pd.read_csv("books.csv")
    df_book_authors = pd.read_csv("book_authors.csv")

    # Renombrar columnas
    df_publishers.columns = ['id', 'name']
    df_authors.columns = ['id', 'name']
    df_books.columns = ['isbn', 'title', 'quantity', 'price', 'publisher_id']

    # Generar IDs para los libros
    df_books['id'] = range(1, len(df_books) + 1)

    # Mapear isbn → book_id
    isbn_to_id = dict(zip(df_books['isbn'], df_books['id']))
    df_book_authors['book_id'] = df_book_authors['isbn'].map(isbn_to_id)
    df_book_authors = df_book_authors.drop(columns=['isbn'])

    # Eliminar duplicados en combinaciones book_id + author_id
    df_book_authors = df_book_authors.drop_duplicates()

    # Conexión (puerto 5434 según tu configuración)
    conn = psycopg2.connect(
        dbname="books_db",
        user="postgres",
        password="books123",
        host="localhost",
        port="5434"
    )
    cur = conn.cursor()

    # Insertar publishers
    print("Insertando publishers...")
    for _, row in df_publishers.iterrows():
        cur.execute(
            "INSERT INTO publishers (id, name) VALUES (%s, %s)",
            (int(row['id']), row['name'])
        )

    # Insertar authors
    print("Insertando authors...")
    for _, row in df_authors.iterrows():
        cur.execute(
            "INSERT INTO authors (id, name) VALUES (%s, %s)",
            (int(row['id']), row['name'])
        )

    # Insertar books
    print("Insertando books...")
    for _, row in df_books.iterrows():
        cur.execute("""
            INSERT INTO books (id, isbn, title, quantity, price, publisher_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            int(row['id']),
            str(row['isbn']),
            row['title'],
            int(row['quantity']),
            float(row['price']),
            int(row['publisher_id'])
        ))

    # Insertar book_authors
    print("Insertando book_authors...")
    for _, row in df_book_authors.iterrows():
        cur.execute("""
            INSERT INTO book_authors (book_id, author_id)
            VALUES (%s, %s)
        """, (int(row['book_id']), int(row['author_id'])))

    conn.commit()
    print("✅ Inserción completada exitosamente.")

except Exception as e:
    print("❌ Error durante la inserción:", e)
    conn.rollback()

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
