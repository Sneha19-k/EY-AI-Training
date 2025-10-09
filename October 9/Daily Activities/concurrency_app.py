from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

#--------------------SYNC ENDPOINT-----------------
@app.get("/sync-task")
def sync_task():
    time.sleep(10)
    return {"message": "sync task completed after 10 seconds "}

#---------------------ASYNC ENDPOINT----------------
@app.get("/async-task")
async def async_task():
    await asyncio.sleep(10)
    return {"message": "Async task completed after 10 seconds "}