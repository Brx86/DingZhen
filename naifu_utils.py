import asyncio
import time

import httpx
from random import choice

# from sd_utils import sd_set

nd_set = set()


async def scan_nd(n: int, pool: int = 50) -> str | None:
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
                            f"\033[1;32mNaifu :\t  \033[4;34m{url}\033[0m\t\t{time.strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                        nd_set.add(n)
                        return url
                    # elif "Stable Diffusion" in r.text and "auth_required" not in r.text:
                    #     print(
                    #         f"\033[1;32mStable:\t  \033[4;34m{url}\033[0m\t\t{time.strftime('%Y-%m-%d %H:%M:%S')}"
                    #     )
                    #     sd_set.add(n)
                    #     return url
                    else:
                        return
            except (httpx.RemoteProtocolError, httpx.ConnectError):
                return
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                pass
            except Exception as e:
                print(repr(e))


def recheck_nd(n: int) -> bool | None:
    """重新检查端口是否有效

    Args:
        n (int): 端口号

    Returns:
        bool: 有效/无效返回布尔值
    """
    for _ in range(3):
        try:
            httpx.get(f"http://bore.pub:{n}", timeout=10)
            return True
        except Exception as e:
            # print(repr(e))
            print(f"\033[1;33mRemove:\t  http://bore.pub:{n}\033[0m")
            if n in nd_set:
                nd_set.remove(n)
            return False


async def get_one_nd() -> str | None:
    """获取一个有效地址

    Returns:
        str | None: 如果有效则直接返回url，无效则重试，直到有效
    """
    if nd_set:
        for _ in range(10):
            n: int = choice(list(nd_set))
            if await asyncio.to_thread(recheck_nd, n):
                return f"http://bore.pub:{n}"


async def run_scan_nd():
    """开始扫描端口"""
    while True:
        for n in range(33000, 43000):
            await asyncio.sleep(0.05)
            if len(nd_set) < 80:
                asyncio.create_task(scan_nd(n))
            else:
                await asyncio.sleep(60)


def run_check_nd():
    """等待20秒开始检测"""
    while True:
        time.sleep(20)
        if nd_set:
            for n in list(nd_set):
                recheck_nd(n)
