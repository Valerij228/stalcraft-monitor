from apscheduler.schedulers.asyncio import AsyncIOScheduler
from stalcraft_db import database
from notifications import notifier
import logging

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)

async def check_price_alerts():
    for item_id, config in database.custom_items.items():
        if not config.price_alerts:
            continue

        # Заглушка для примера
        current_price = 14_500_000

        for alert in config.price_alerts:
            if current_price <= alert:
                await notifier.send_alert(
                    chat_id=123456789,  # Ваш chat_id
                    item_id=item_id,
                    price=current_price
                )
                logger.info(f"Уведомление отправлено для {item_id}")

scheduler.add_job(check_price_alerts, 'interval', minutes=5)
