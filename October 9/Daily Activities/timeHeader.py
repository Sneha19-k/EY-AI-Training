from fastapi import FastAPI, Request
import time

app = FastAPI()

# Middleware to calculate request duration
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start_time) * 1000  # in milliseconds
    response.headers["X-Response-Time"] = f"{duration:.2f}ms"
    return response

# Simple route
@app.get("/")
async def hello():
    return {"message": "Hello, World!"}
