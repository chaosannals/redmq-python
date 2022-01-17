from datetime import datetime, timedelta
from urllib.parse import urljoin
from aiohttp import ClientSession
from .exception import RedMQRequestException
from .crypt import random_text, encrypt256, decrypt256


class RedMQClient:
    '''
    客户端
    '''

    def __init__(self, key: str, secret: bytes, host='127.0.0.1', port=33000):
        '''
        初始化。
        '''

        self.key = key
        self.secret = secret
        self.host = host
        self.port = port
        self.token = None
        self.token_expired_at = None

    async def request(self, path, data):
        '''
        请求。
        '''

        url = urljoin(f'http://{self.host}:{self.port}', path)
        async with ClientSession() as session:
            async with session.post(url, json=data) as response:
                return response.status, response.headers, await response.json()

    async def request_by_auth(self, path, data):
        '''
        授权请求
        '''

        now = datetime.now()
        if self.token is None or self.token_expired_at < now:
            await self.login()

        s, hs, d = await self.request(path, {
            'key': self.key,
            'data': encrypt256(self.token, data)
        })

        if 'data' in d:
            d['data'] = decrypt256(self.token, d['data'])
        return s, hs, d

    async def login(self):
        '''
        登录
        '''

        key = random_text()
        expired_at = datetime.now() + timedelta(minutes=1)
        ekey = encrypt256(self.secret, {
            'key': key,
            'expired_at': expired_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

        s, hs, d = await self.request('/login', {
            'app': self.key,
            'key': key,
            'ekey': ekey
        })

        if 200 > s or s >= 300:
            raise RedMQRequestException(s, hs, d)

        data = decrypt256(self.secret, d.get('data'))
        self.token = bytes(data.get('token'), encoding='utf8')
        self.token_expired_at = datetime.strptime(
            data.get('expired_at'),
            '%Y-%m-%d %H:%M:%S'
        )
        return data

    async def info(self, queue):
        '''
        获取队列信息。
        '''

        return await self.request_by_auth('/work/info', {
            'queue': queue,
        })

    async def push(self, data, queue):
        '''
        推送任务。
        '''

        return await self.request_by_auth('/work/push', {
            'queue': queue,
            'data': data,
        })

    async def pull(self, queue):
        '''
        '''

        return await self.request_by_auth('/work/pull', {
            'queue': queue,
        })

    async def peek(self, queue):
        '''
        '''

        return await self.request_by_auth('/work/peek', {
            'queue': queue,
        })
