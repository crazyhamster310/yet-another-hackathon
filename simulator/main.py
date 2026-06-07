import asyncio
import json
import logging
import os
import sys

import httpx
import websockets

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ScreenSimulator")

# Параметры из окружения
API_URL = os.getenv("API_URL", "http://proxy/api/v1")
WS_URL = os.getenv("WS_URL", "ws://proxy/ws")
SCREEN_SLUG = os.getenv("SCREEN_SLUG", "lobby-1")


class SmartDisplaySimulator:
    def __init__(self, slug: str):
        self.slug = slug
        self.screen_id: str | None = None
        self.is_emergency = False
        self.emergency_text = ""
        self.slots: dict[str, dict | None] = {}

    async def fetch_config(self):
        logger.info(f"Запрос конфигурации для slug: {self.slug}...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{API_URL}/screens/{self.slug}")
                if response.status_code == 404:
                    logger.error(
                        f"Экран со slug '{self.slug}' не найден в базе. Создайте его через Swagger."
                    )
                    return False
                response.raise_for_status()
                data = response.json()

                self.screen_id = data["id"]
                self.slots = data["slots"]
                self.is_emergency = data["is_emergency"]
                self.emergency_text = data["emergency_text"] or ""

                logger.info(
                    f"Конфигурация загружена успешно. ID: {self.screen_id}"
                )
                return True
            except Exception as e:
                logger.error(f"Ошибка при подключении к API: {e}")
                return False

    async def websocket_listener(self):
        uri = f"{WS_URL}/{self.screen_id}"
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    logger.info("WebSocket соединение установлено.")
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        if data.get("type") == "EMERGENCY_UPDATE":
                            payload = data["payload"]
                            self.is_emergency = payload["is_emergency"]
                            self.emergency_text = payload["text"]
                            logger.warning(
                                f"ОБНОВЛЕНИЕ ЧС: status={self.is_emergency}, text={self.emergency_text}"
                            )
            except Exception as e:
                logger.error(f"WebSocket потерян, переподключение... ({e})")
                await asyncio.sleep(5)

    async def display_loop(self):
        while True:
            print("\n" + "=" * 60)
            if self.is_emergency:
                print(f"!!! РЕЖИМ ЧС: {self.emergency_text} !!!")
                print("=" * 60)

            print(f"Дисплей: {self.slug} | Слоты:")
            for i in range(4):
                slot_data = self.slots.get(str(i))

                if slot_data:
                    w_type = slot_data["widget_type"].upper()
                    title = slot_data["title"] or "Без заголовка"
                    content = slot_data["content"]
                    print(f"[{i}] {w_type} | {title}: {content[:40]}...")
                else:
                    print(f"[{i}] <ПУСТОЙ СЛОТ>")

            print("=" * 60)
            await asyncio.sleep(15)

    async def start(self):
        while not await self.fetch_config():
            await asyncio.sleep(5)

        await asyncio.gather(self.display_loop(), self.websocket_listener())


if __name__ == "__main__":
    simulator = SmartDisplaySimulator(SCREEN_SLUG)
    try:
        asyncio.run(simulator.start())
    except KeyboardInterrupt:
        pass
