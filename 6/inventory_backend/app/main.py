from fastapi import FastAPI
from app.routers import inventory, llm, image

app = FastAPI(title="Inventory Management API")

app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
# app.include_router(llm.router, prefix="/llm", tags=["LLM"])
# app.include_router(image.router, prefix="/image", tags=["Image"])
