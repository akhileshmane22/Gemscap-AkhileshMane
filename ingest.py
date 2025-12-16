import asyncio
import json
import sqlite3
from datetime import datetime
import websockets

DB = "ticks.db"

SYMBOLS = ["btcusdt", "ethusdt", "bnbusdt"]



def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            symbol TEXT,
            timestamp TIMESTAMP,
            price REAL,
            qty REAL
        )
    """)
    con.commit()
    con.close()


def store_tick(symbol, ts, price, qty):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO ticks VALUES (?,?,?,?)",
        (symbol, ts, price, qty)
    )
    con.commit()
    con.close()


async def stream_symbol(symbol):
    url = f"wss://fstream.binance.com/ws/{symbol}@trade"

    while True:  # 🔁 infinite reconnect loop
        try:
            print(f"🔌 Connecting to {symbol}...")
            async with websockets.connect(
                url,
                ping_interval=20,
                ping_timeout=20,
                close_timeout=5
            ) as ws:

                async for msg in ws:
                    data = json.loads(msg)

                    ts = datetime.utcfromtimestamp(data["T"] / 1000)
                    price = float(data["p"])
                    qty = float(data["q"])

                    store_tick(symbol, ts, price, qty)

        except Exception as e:
            print(f"⚠️ {symbol} stream error: {e}")
            print("🔄 Reconnecting in 5 seconds...")
            await asyncio.sleep(5)



async def main():
    init_db()
    tasks = [stream_symbol(sym) for sym in SYMBOLS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
