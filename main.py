import httpx
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core import AstrBotConfig
from astrbot.core.message.components import At

error_code = {403, 404, 429, 500}


def getimg(qq, key, api):
    if api is None:
        return -1
    url = "https://api.xiaoyu17love.top/API/bqbjh.php"
    params = {
        "apikey": api,
        "type": "zhitu",
        "key": key,
        "qqs": [qq],
    }
    response = httpx.get(url, params=params)
    j = response.json()
    imgUrl = j['data']['url']
    if j['code'] == 200:
        return imgUrl
    elif j['code'] in error_code:
        return j['code']
    else:
        return None


class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("doro")
    async def doro(self, event: AstrMessageEvent):
        """生成doro敲头"""  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        sender_id = event.get_sender_id()
        message = event.get_messages()
        message_chain = event.get_messages()  # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        config = self.config
        Key = config.get('Key')

        qq_id = sender_id
        for comp in message:
            if isinstance(comp, At):
                qq_id = comp.qq
                break

        yield event.plain_result(f'制作中')

        URL = getimg(qq_id, key="doro_banging", api=Key)
        if URL is None:
            yield event.plain_result(f'制作失败，请到控制台查看详情')
        elif URL in error_code:
            logger.error(URL)
            yield event.plain_result(f'制作失败，请到控制台查看详情')
        elif URL == -1:
            logger.warn(f'未填写Key，请前往https://api.xiaoyu17love.top/申请')
            yield event.plain_result(f'制作失败，未填写APIKey')
        else:
            yield event.image_result(f'{URL}')

    @filter.command('arona')
    async def arona(self, event: AstrMessageEvent):
        """生成阿罗娜丢"""
        sender_id = event.get_sender_id()
        message = event.get_messages()
        message_chain = event.get_messages()  # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        config = self.config
        Key = config.get('Key')

        qq_id = sender_id
        for comp in message:
            if isinstance(comp, At):
                qq_id = comp.qq
                break

        yield event.plain_result(f'制作中')

        URL = getimg(qq_id, key='arona_throw', api=Key)
        if URL is None:
            yield event.plain_result(f'制作失败，请到控制台查看详细')
        elif URL in error_code:
            yield event.plain_result(f'制作失败，请到控制台查看详细')
            logger.error(URL)
        elif URL == -1:
            logger.warn(f'未填写Key，请前往https://api.xiaoyu17love.top/申请')
            yield event.plain_result(f'制作失败，未填写APIKey')
        else:
            yield event.image_result(f"{URL}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
