import requests

BASE_URL = "http://localhost:8000"

def test_get_stock(isbn):
    resp = requests.get(f"{BASE_URL}/inventory/stock/{isbn}")
    print("📦 Stock:", resp.json())

def test_get_price(isbn):
    resp = requests.get(f"{BASE_URL}/inventory/price/{isbn}")
    print("💲 Precio:", resp.json())

def test_add_stock(isbn, cantidad):
    resp = requests.post(f"{BASE_URL}/inventory/stock/add", params={"isbn": isbn, "cantidad": cantidad})
    print("➕ Agregar stock:", resp.json())

def test_generar_orden_compra(stock_min, author=None):
    params = {"stock_min": stock_min}
    if author:
        params["author"] = author
    resp = requests.get(f"{BASE_URL}/inventory/orden_compra/", params=params)
    print("📝 Orden de compra:", resp.json())

if __name__ == "__main__":
    isbn = "6154685511062"

    test_get_stock(isbn)
    test_get_price(isbn)
    test_add_stock(isbn, 10)
    test_get_stock(isbn)

    test_generar_orden_compra(10)
    test_generar_orden_compra(9999, author="Stephen King")
