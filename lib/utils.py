import asyncio
import datetime
import settings as C

__all__ = [
    "format_unixtime",
    "async_run"
]


def format_unixtime(tstamp, fmt="%Y%m%d%H%M%S"):
    return datetime.datetime.fromtimestamp(tstamp).strftime(fmt)


def async_run(func, iters, *args):
    loop = asyncio.get_event_loop()
    futures = async_iterate(func, iters, *args)
    return loop.run_until_complete(futures)


async def async_iterate(func, iters, *args):
    semaphore = asyncio.Semaphore(C.ASYNC_LIMIT)

    async def async_semaphore(func, *args):
        async with semaphore:
            return await async_executor(func, *args)

    return await asyncio.gather(
        *[async_semaphore(func, item, *args) for item in iters])


async def async_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)

