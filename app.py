import httpx
from wombo import Wombo
from typing import Optional
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from random import choice
from piclist import dj_list

app = FastAPI()


class Item(BaseModel):
    keywords: str = Field(..., min_length=1, max_length=20)
    style: Optional[int] = None


@app.get("/")
def root():
    return {"repo": "https://github.com/Brx86/DingZhen", "amount": len(dj_list)}


@app.get("/randomdj")
def random_dj(r: int = 1, g: int = 1):
    pic_name = choice(dj_list)
    pic_url = (
        f"https://raw.githubusercontent.com/Brx86/DingZhen/main/src/{pic_name}"
        if g == 1
        else f"https://ayatale.coding.net/p/picbed/d/DingZhen/git/raw/main/src/{pic_name}"
    )
    if r == 0:
        return {
            "code": 200,
            "status": "ok",
            "url": pic_url,
        }
    return RedirectResponse(pic_url)


@app.exception_handler(RequestValidationError)
async def err(request: Request, exc: RequestValidationError):
    print(f"参数错误: {request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})


@app.post("/wombo")
async def get_url(item: Item = Body()):
    global auth
    async with httpx.AsyncClient(timeout=10) as client:
        w, auth = await Wombo.init(client, auth)
        style_name, url = await w.run(item.keywords, item.style)
        return {"code": 200, "style": style_name, "keywords": item.keywords, "url": url}


if __name__ == "__main__":
    import uvicorn  # type: ignore

    auth = (0,)
    uvicorn.run(app, host="0.0.0.0", port=7777)