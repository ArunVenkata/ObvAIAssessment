from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import asyncio
import time

router = APIRouter()

async def event_generator():
    while True:
        await asyncio.sleep(1)
        yield f"data: The current time is {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

@router.get("/events", response_class=StreamingResponse)
async def sse_endpoint(request: Request):
    return StreamingResponse(event_generator(), media_type="text/event-stream")