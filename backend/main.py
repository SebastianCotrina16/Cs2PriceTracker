from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importa CORS
from scraper import get_cheapest_knives, get_cheapest_gloves, get_skin_price
from database import save_skin_price, get_price_history

app = FastAPI()

# ✅ Habilitar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las conexiones (puedes restringir a tu frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/")
async def root():
    return {"message": "CS2 Market Tracker API is running 🚀"}

@app.get("/knives")
async def knives():
    return get_cheapest_knives()

@app.get("/gloves")
async def gloves():
    return get_cheapest_gloves()

@app.get("/skin/{name}")
async def skin(name: str):
    price_data = get_skin_price(name)

    if "price" in price_data:
        save_skin_price(name, price_data["price"])

    history = get_price_history(name)
    return {"name": name, "current_price": price_data.get("price"), "history": history}
