from urllib.parse import urljoin
from aiohttp import ClientSession

class RedMQClient:
    '''
    客户端
    '''

    def __init__(self, host='127.0.0.1', port=33000):
        '''
        初始化。
        '''

        self.host = host
        self.port = port


    async def request(self, path, data):
        '''
        请求。
        '''
        
        url = urljoin(f'http://{self.host}:{self.port}', path)
        async with ClientSession() as session:
            async with session.post(url, json=data) as response:
                return response.status, response.headers, await response.json()

    async def info(self, queue):
        '''
        获取队列信息。
        '''

        return await self.request('/work/info', {
            'queue': queue,
        })

    async def push(self, data, queue):
        '''
        推送任务。
        '''

        return await self.request('/work/push', {
            'queue': queue,
            'data': data,
        })

    async def pull(self, queue):
        '''
        '''

        return await self.request('/work/pull', {
            'queue': queue,
        })

    async def peek(self, queue):
        '''
        '''

        return await self.request('/work/peek', {
            'queue': queue,
        })
