import os
import uvicorn
import asyncio
from fastapi import FastAPI
from auction_api import app
from tasks import scheduler
from notifications import notifier
from stalcraft_db import database

# Инициализация
app = FastAPI()
app.mount("/api", app)

async def run_monitoring():
    await scheduler.start()
    while True:
        await asyncio.sleep(1)

async def main():
    server = uvicorn.Server(
        config=uvicorn.Config(
            app,
            host="0.0.0.0",
            port=int(os.getenv("API_PORT", 8000)),
            log_level=os.getenv("LOG_LEVEL", "info")
        )
    )

    await asyncio.gather(
        server.serve(),
        run_monitoring()
    )

if __name__ == "__main__":
    asyncio.run(main())
