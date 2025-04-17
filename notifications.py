import os
from telegram import Bot
from stalcraft_db import database

class NotificationSystem:
    def __init__(self):
        self.bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))

    async def send_alert(self, chat_id: int, item_id: str, price: float):
        config = database.get_item_config(item_id)
        item = next(i for i in database.items if i["id"] == item_id)

        message = (
            f"🚨 **Ценовое уведомление**\n"
            f"▶️ {config.custom_name or item['name']['lines']['ru']}\n"
            f"💵 Текущая цена: {price:,.2f} ₽\n"
            f"🔔 Триггер: {config.price_alerts}"
        )

        await self.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown"
        )

notifier = NotificationSystem()
