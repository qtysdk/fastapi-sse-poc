import datetime
from typing import Union

import uvicorn
from fastapi import APIRouter, FastAPI
from sse_starlette import EventSourceResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from sse import status_event_generator

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World", "ts": datetime.datetime.isoformat(datetime.datetime.now())}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


router = APIRouter()


@router.get('/status/stream')
async def runStatus(
        request: Request
):
    event_generator = status_event_generator(request)
    return EventSourceResponse(event_generator)


app.mount("/web", StaticFiles(directory="html"), name="web")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
