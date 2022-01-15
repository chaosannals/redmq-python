import asyncio
from redmq.client import RedMQClient

async def main(loop):
    key = 'demokey'
    secret = b'1234567890ABCEDF1234567890ABCEDF'
    client = RedMQClient(key, secret)
    for i in range(10):
        r = await client.push({
            'bbb': i
        }, 'works.demo')
        print(r)
    print('=============================')
    info = await client.info('works.demo')
    print(info)
    print('=============================')
    w = await client.peek('works.demo')
    print(w)

async def main2(loop):
    key = 'demokey'
    secret = b'1234567890ABCEDF1234567890ABCEDF'
    client = RedMQClient(key, secret)
    r = await client.login()
    print(r)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
