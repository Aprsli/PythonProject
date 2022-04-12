import asyncio
import nest_asyncio
nest_asyncio.apply()
from concurrent.futures import ProcessPoolExecutor


async def main():
    await asyncio.sleep(3)
    print("hello")

async def test():
    return 1


if __name__ == '__main__':
    result = asyncio.run(asyncio.gather(main(), test(), test(), main()))
    with ProcessPoolExecutor(max_workers=4) as executor:
        future = executor.submit(pow, 323, 1235)
        print(future.result())
