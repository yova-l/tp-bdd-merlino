import psycopg2
import pandas as pd

# Conexión
conn = psycopg2.connect(
    dbname="books_db",
    user="postgres",
    password="books123",
    host="localhost",
    port="5434"
)

# Helper para ejecutar y mostrar consultas
def run_query(query, description):
    print(f"\n🔎 {description}")
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

# 1. Primeros 10 libros (simple)
run_query("""
    SELECT id, title, price
    FROM books
    ORDER BY id
    LIMIT 10
""", "Primeros 10 libros")

# 2. Libros con precio entre X e Y
X, Y = 20000, 40000
run_query(f"""
    SELECT id, title, price
    FROM books
    WHERE price BETWEEN {X} AND {Y}
    ORDER BY price
    LIMIT 10
""", f"Libros con precio entre {X} y {Y}")

# 3. Libros con su publisher
run_query("""
    SELECT b.id, b.title, b.price, p.name AS publisher
    FROM books b
    JOIN publishers p ON b.publisher_id = p.id
    ORDER BY b.id
    LIMIT 10
""", "Libros con su editorial")

# 4. Libros con sus autores
run_query("""
    SELECT b.title, a.name AS author
    FROM books b
    JOIN book_authors ba ON b.id = ba.book_id
    JOIN authors a ON ba.author_id = a.id
    ORDER BY b.id
    LIMIT 10
""", "Libros con sus autores")

# 5. Cantidad de libros por autor
run_query("""
    SELECT a.name, COUNT(*) AS book_count
    FROM authors a
    JOIN book_authors ba ON a.id = ba.author_id
    GROUP BY a.name
    ORDER BY book_count DESC
    LIMIT 10
""", "Cantidad de libros por autor")

conn.close()
