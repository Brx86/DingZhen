import asyncio
import time

import httpx
from random import choice


sd_set = set()


async def scan_sd(n: int, pool: int = 50) -> str | None:
    """检查网页是否有效且为Stable Diffusion Webui，有效地址加入集合

    Args:
        n (int): 三级域名

    Returns:
        str | None: 如果有效则直接返回url，无效返回None
    """
    sem = asyncio.Semaphore(pool)
    async with sem:
        for _ in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(url := f"https://{n}.gradio.app")
                    break
            except:
                pass
        else:
            return
        if "Stable Diffusion" in r.text and "auth_required" not in r.text:
            print(
                f"\033[1;32mStable:\t  \033[4;34m{url}\033[0m\t{time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            sd_set.add(n)
            return url


def recheck_sd(n: int) -> bool | None:
    """重新检查地址是否有效

    Args:
        n (int): 三级域名

    Returns:
        bool: 有效/无效返回布尔值
    """
    for _ in range(3):
        try:
            r = httpx.get(f"https://{n}.gradio.app", timeout=10)
            if "Stable Diffusion" in r.text and "auth_required" not in r.text:
                return True
            else:
                if n in sd_set:
                    print(f"\033[1;33mRemove:\t  https://{n}.gradio.app\033[0m")
                    sd_set.remove(n)
                return False
        except:
            pass


async def get_one_sd() -> str | None:
    """获取一个有效地址

    Returns:
        str | None: 如果有效则直接返回url，无效则重试，直到有效
    """
    if sd_set:
        for _ in range(10):
            n: int = choice(list(sd_set))
            if await asyncio.to_thread(recheck_sd, n):
                return f"https://{n}.gradio.app"


async def run_scan_sd():
    """开始扫描端口"""
    while True:
        for n in range(10000, 25000):
            await asyncio.sleep(0.1)
            if len(sd_set) < 80:
                asyncio.create_task(scan_sd(n))
            else:
                await asyncio.sleep(60)


def run_check_sd():
    """等待20秒开始检测"""
    while True:
        time.sleep(20)
        if sd_set:
            for n in list(sd_set):
                recheck_sd(n)
