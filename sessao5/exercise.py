from fastapi import FastAPI
import asyncio
from datetime import datetime
import random

app = FastAPI()

async def fetch_data_from_source_1():
    delay = random.uniform(0.5, 1.5)
    await asyncio.sleep(delay)
    return {
        "source": "Source 1",
        "data": f"Data from source 1 at {datetime.now().isoformat()}",
        "delay": f"{delay:.2f} seconds"
    }

async def fetch_data_from_source_2():
    delay = random.uniform(0.5, 1.5)
    await asyncio.sleep(delay)
    return {
        "source": "Source 2",
        "data": f"Data from source 2 at {datetime.now().isoformat()}",
        "delay": f"{delay:.2f} seconds"
    }

@app.get("/fetch-data")
async def fetch_data():
    results = await asyncio.gather(
        fetch_data_from_source_1(),
        fetch_data_from_source_2()
    )
    
    return {
        "source_1_data": results[0],
        "source_2_data": results[1],
        "note": "Both fetches completed concurrently"
    }
