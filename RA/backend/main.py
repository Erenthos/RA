from fastapi import FastAPI, WebSocket
import asyncpg, os
from datetime import datetime

app = FastAPI()

DB_URL = os.getenv("NEON_URL", "postgresql://neondb_owner:npg_BVgWoL0S6paU@ep-curly-scene-a1o7zs4z-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

async def get_conn():
    return await asyncpg.connect(DB_URL)

@app.get("/")
async def root():
    return {"msg": "Reverse Auction API running"}

@app.post("/bid")
async def place_bid(auction_id: int, user_id: int, bid_amount: float):
    conn = await get_conn()
    await conn.execute(
        "INSERT INTO bids (auction_id, user_id, bid_amount, bid_time) VALUES ($1, $2, $3, $4)",
        auction_id, user_id, bid_amount, datetime.now()
    )
    await conn.close()
    return {"status": "success", "amount": bid_amount}

@app.websocket("/ws/{auction_id}")
async def websocket_endpoint(websocket: WebSocket, auction_id: int):
    await websocket.accept()
    await websocket.send_text(f"Connected to auction {auction_id}")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Bid received: {data}")
