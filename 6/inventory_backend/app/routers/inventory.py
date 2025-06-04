from fastapi import APIRouter, HTTPException
from app.crud.inventory import (
    consultar_stock_por_isbn,
    consultar_precio_por_isbn,
    agregar_stock,
    generar_orden_compra
)

router = APIRouter()

@router.get("/stock/{isbn}")
def get_stock(isbn: str):
    try:
        stock = consultar_stock_por_isbn(isbn)
        return {"isbn": isbn, "stock": stock}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price/{isbn}")
def get_price(isbn: str):
    try:
        price = consultar_precio_por_isbn(isbn)
        return {"isbn": isbn, "price": price}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stock/add")
def post_add_stock(isbn: str, cantidad: int):
    try:
        agregar_stock(isbn, cantidad)
        return {"message": f"Se agregaron {cantidad} unidades al libro con ISBN {isbn}"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orden_compra/")
def get_orden_compra(stock_min: int = Query(..., gt=0), author: str | None = None):
    try:
        data = generar_orden_compra(stock_min, author)
        return {"orden_compra": data}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))