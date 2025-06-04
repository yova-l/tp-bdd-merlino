from app.db import get_connection
import json

def consultar_stock_por_isbn(isbn: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT consultar_stock_por_isbn(%s);", (isbn,))
            result = cur.fetchone()
            print("DEBUG consultar_stock_por_isbn RESULT:", result)
            return result["consultar_stock_por_isbn"] if result else 0

def consultar_precio_por_isbn(isbn: str) -> float:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT consultar_precio_por_isbn(%s);", (isbn,))
            result = cur.fetchone()
            print("DEBUG consultar_precio_por_isbn RESULT:", result)
            return float(result["consultar_precio_por_isbn"]) if result else 0.0

def agregar_stock(isbn: str, cantidad: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT agregar_stock(%s, %s);", (isbn, cantidad))
            conn.commit()

def generar_orden_compra(stock_min: int, author: str = None) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            if author:
                cur.execute("SELECT generar_orden_compra(%s, %s);", (stock_min, author))
            else:
                cur.execute("SELECT generar_orden_compra(%s);", (stock_min,))
            result = cur.fetchone()
            print("DEBUG generar_orden_compra RESULT:", result)
            if result:
                return json.loads(result["generar_orden_compra"])
            return {}
