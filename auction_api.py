from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from stalcraft_db import database

app = FastAPI(title="Stalcraft Price Monitor")

class ItemRequest(BaseModel):
    name: str
    custom_name: Optional[str] = None
    price_alerts: List[float] = []
    auto_buy: bool = False
    purchase_limit: Optional[float] = None

@app.post("/api/items/register")
async def register_item(item: ItemRequest):
    try:
        database.add_custom_item(item.name, item.dict())
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.get("/api/items/search")
async def search_items(q: str, lang: str = "ru"):
    items = database.search_items(q, lang)
    return {
        "count": len(items),
        "items": [{
            "id": item["id"],
            "name": item["name"]["lines"][lang],
            "icon": f"{database.icons_base_url}/{item['category'].replace('/', '_')}/{item['id']}.png"
        } for item in items]
    }

@app.get("/api/items/{item_id}/lots")
async def get_lots(item_id: str):
    config = database.get_item_config(item_id)

    # Заглушка для примера
    lots = [
        {"id": "1", "price": 14_500_000},
        {"id": "2", "price": 15_000_000}
    ]

    return {
        "item_id": item_id,
        "custom_name": config.custom_name,
        "filtered_lots": [lot for lot in lots if lot["price"] <= config.purchase_limit]
    }
