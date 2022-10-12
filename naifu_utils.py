import asyncio
import time

import httpx
from random import choice


sd_set = set()
naifu_set = set()


async def check_html(n: int, pool: int = 30) -> str | None:
    """检查网页是否有效且为Stable Diffusion Webui或Naifu，有效地址加入集合

    Args:
        n (int): 端口号

    Returns:
        str | None: 如果有效则直接返回url，无效返回None
    """
    sem = asyncio.Semaphore(pool)
    async with sem:
        for _ in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(url := f"http://bore.pub:{n}")
                    if "NAIFU" in r.text and "novelai" in r.text:
                        print(
                            f"\033[1;32mNaifu :\t  \033[4;34m{url}\033[0m\t{time.strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                        naifu_set.add(n)
                        return url
                    elif "Stable Diffusion" in r.text:
                        print(
                            f"\033[1;32mStable:\t  \033[4;34m{url}\033[0m\t{time.strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                        sd_set.add(n)
                        return url
                    else:
                        return
            except (httpx.RemoteProtocolError, httpx.ConnectError):
                return
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                pass
            except Exception as e:
                print(repr(e))


async def run():
    while True:
        for n in range(33000, 43000):
            await asyncio.sleep(0.1)
            asyncio.create_task(check_html(n))


async def recheck():
    while True:
        await asyncio.sleep(10)
        for n in list(naifu_set):
            if (await check_html(n, pool=100)) is None:
                print(f"\033[1;33mRemove:\t  http://bore.pub:{n}\033[0m")
                if n in naifu_set:
                    naifu_set.remove(n)


async def get_one():
    if naifu_set:
        for _ in range(10):
            n: int = choice(list(naifu_set))
            if await check_html(n, pool=100):
                return f"http://bore.pub:{n}"
            else:
                print(f"\033[1;33mRemove:\t  http://bore.pub:{n}\033[0m")
                naifu_set.remove(n)
