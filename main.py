from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter
import uvicorn
import asyncio

# Main FastAPI app
app = FastAPI()


request_counter = Counter('request_count', 'Total number of requests')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    request_counter.inc()
    return {"message": f"Hello {name}"}

# Prometheus metrics app
metrics_app = FastAPI()
metrics_app.mount("/", make_asgi_app())

async def start_metrics_server():
    config = uvicorn.Config(metrics_app, host="0.0.0.0", port=9000)
    server = uvicorn.Server(config)
    await server.serve()

# Start the metrics server in a separate thread
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(start_metrics_server())