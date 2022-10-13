import asyncio
from io import BytesIO
from random import choice, randint
from typing import Optional

import httpx
from fastapi import Body, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from pydantic import BaseModel, Field, conint

from piclist import dj_list
from wombo import Wombo

app = FastAPI()


class Item(BaseModel):
    keywords: str = Field(..., min_length=1, max_length=20)
    style: Optional[conint(ge=1, le=26)] = None  # type: ignore
    file: Optional[conint(ge=0, le=1)] = None  # type: ignore


async def download(url):
    async with httpx.AsyncClient(timeout=10) as c:
        print(f"Downloading...")
        r = await c.get(url)
        if r.status_code == 200:
            return BytesIO(r.content)
        print(f"Error: {r.status_code}")
        return None


@app.get("/", status_code=200)
def root():
    return {"repo": "https://github.com/Brx86/DingZhen", "amount": len(dj_list)}


@app.get("/randomdj", status_code=200)
def random_dj(r: int = 1, g: int = 0):
    pic_name = choice(dj_list)
    pic_url = (
        f"https://raw.githubusercontent.com/Brx86/DingZhen/main/src/{pic_name}"
        if g == 1
        else f"https://ayatale.coding.net/p/picbed/d/DingZhen/git/raw/main/src/{pic_name}"
    )
    if r == 0:
        return {"status": "ok", "url": pic_url}
    return RedirectResponse(pic_url)


@app.get("/kemo", status_code=200)
def kemo():
    pic_url = f"https://ayatale.coding.net/p/picbed/d/kemo/git/raw/master/{randint(1,696)}.jpg"
    return RedirectResponse(pic_url)


@app.exception_handler(RequestValidationError)
async def err(request: Request, exc: RequestValidationError):
    print(f"参数错误: {request.method} {request.url}")
    return JSONResponse({"code": 400, "status": "error", "message": exc.errors()})


@app.get("/wombo", status_code=200)
def usage_wombo():
    return {
        "status": "ok",
        "usage": """curl -X POST -H "Content-type: application/json" "https://api.aya1.top/wombo" -d '{"keywords":"example"}'""",
    }


@app.post("/wombo", status_code=200)
async def handle_wombo(response: Response, item: Item = Body()):
    async with httpx.AsyncClient(timeout=20) as client:
        w = await Wombo.init(client)
        style_name, url = await w.run(item.keywords, item.style)
        info = {"style": style_name, "keywords": item.keywords}
        while "https" in url:
            print(f"URL: {url}")
            if item.file == 1:
                img = await download(url)
                if img == None:
                    break
                return StreamingResponse(content=img, media_type="image/jpg")
            info.update({"status": "ok", "url": url})
            return info
        response.status_code = 408
        info.update({"status": "timeout"})
        return info


from naifu_utils import *
from sd_utils import *
from threading import Thread


@app.get("/logs")
async def return_log():
    with open(f"{cwd}/logs/logfile.log", "r") as f:
        return Response(f.read())


@app.get("/ai")
async def redirect_nd_old():
    if url := await get_one_nd():
        return RedirectResponse(url)
    else:
        return "当前没有可用的地址！"


@app.get("/naifu")
async def redirect_nd():
    if url := await get_one_nd():
        return RedirectResponse(url)
    else:
        return "当前没有可用的地址！"


@app.get("/stable")
async def redirect_sd():
    if url := await get_one_sd():
        return RedirectResponse(url)
    else:
        return "当前没有可用的地址！"


@app.get("/{name}/{action}")
async def return_url(name: str, action: str):
    if name == "naifu" and action == "url":
        return (await get_one_nd()) or "当前没有可用的地址！"
    elif name == "stable" and action == "url":
        return (await get_one_sd()) or "当前没有可用的地址！"
    elif name == "naifu" and action == "info":
        return {"available": len(nd_set), "list": nd_set}
    elif name == "stable" and action == "info":
        return {"available": len(sd_set), "list": sd_set}


@app.on_event("startup")
async def start():
    print("\033[1;32mStart:\t  Scanning from 33000 to 40000\033[0m")
    asyncio.create_task(run_scan_nd())
    asyncio.create_task(run_scan_sd())
    Thread(target=run_check_nd).start()
    Thread(target=run_check_sd).start()


if __name__ == "__main__":
    import uvicorn, pathlib  # type: ignore

    cwd = pathlib.Path(__file__).parent.resolve()
    uvicorn.run(app, host="0.0.0.0", port=7777, log_config=f"{cwd}/logs/log.ini")