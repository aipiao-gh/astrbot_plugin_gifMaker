from pathlib import Path
import httpx
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core import AstrBotConfig
from astrbot.core.message.components import At

error_code = {403, 404, 429, 500}
plugin_dir = Path(__file__).parent
error_img_path = str(plugin_dir / "resource/error.jpg")


def getimg(qq, key, api, timeout):
    if api is None:
        return -1
    url = "https://api.xiaoyu17love.top/API/bqbjh.php"
    params = {
        "apikey": api,
        "type": "zhitu",
        "key": key,
        "qqs": [qq],
    }

    try:
        response = httpx.get(url, params=params, timeout=timeout)
        data = response.json()
    except (httpx.HTTPStatusError, httpx.ReadTimeout) as e:
        logger.error(f"API 服务异常 (HTTP {e})")
        return error_img_path
    code = data['code']
    if code == 200:
        img_url = data['data']['url']
        return img_url
    elif code in error_code:
        logger.error(f'制作失败，错误代码：{code}')
        return error_img_path
    else:
        logger.error('制作失败，原因未知')
        return "未知错误"


class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    def _hand_image_command(self, event: AstrMessageEvent, key: str):
        sender_id = event.get_sender_id()
        message = event.get_messages()
        message_chain = event.get_messages()
        logger.info(message_chain)
        config = self.config
        api = config.get('Key')
        timeout_time = config.get('Timeout')

        qq_id = sender_id
        for comp in message:
            if isinstance(comp, At):
                qq_id = comp.qq
                break

        result = getimg(qq_id, key, api, timeout_time)
        return result

    @filter.command("doro")
    async def doro(self, event: AstrMessageEvent):
        """生成doro敲头"""  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        yield event.plain_result(f'制作中')
        img_url = self._hand_image_command(event, key="doro_banging")
        if 'http' in img_url or 'error.jpg' in img_url:
            yield event.image_result(f'{img_url}')
        elif img_url == -1:
            yield event.plain_result('未填写API，请填写配置文件')
        else:
            yield event.plain_result(f'{img_url}')

    @filter.command('arona')
    async def arona(self, event: AstrMessageEvent):
        """生成阿罗娜丢"""
        yield event.plain_result(f'制作中')
        img_url = self._hand_image_command(event, key="arona_throw")
        if 'http' in img_url or 'error.jpg' in img_url:
            yield event.image_result(f'{img_url}')
        elif img_url == -1:
            yield event.plain_result('未填写API，请填写配置文件')
        else:
            yield event.plain_result(f'{img_url}')

    @filter.command('plana')
    async def plana(self, event: AstrMessageEvent):
        """生成普拉那吃"""
        yield event.plain_result(f'制作中')
        img_url = self._hand_image_command(event, key="plana_eat")
        if 'http' in img_url or 'error.jpg' in img_url:
            yield event.image_result(f'{img_url}')
        elif img_url == -1:
            yield event.plain_result('未填写API，请填写配置文件')
        else:
            yield event.plain_result(f'{img_url}')

    @filter.command('capoo')
    async def capoo(self, event: AstrMessageEvent):
        """生成capoo打棒球"""
        yield event.plain_result(f'制作中')
        img_url = self._hand_image_command(event, key="play_baseball")
        if 'http' in img_url or 'error.jpg' in img_url:
            yield event.image_result(f'{img_url}')
        elif img_url == -1:
            yield event.plain_result('未填写API，请填写配置文件')
        else:
            yield event.plain_result(f'{img_url}')

    @filter.command('capoohit')
    async def capoo_hit(self, event: AstrMessageEvent):
        """生成被capoo揍"""
        yield event.plain_result('制作中')
        img_url = self._hand_image_command(event, key='capoo_lashings')
        if 'http' in img_url or 'error.jpg' in img_url:
            yield event.image_result(f'{img_url}')
        elif img_url == -1:
            yield event.plain_result('未填写API，请填写配置文件')
        else:
            yield event.plain_result(f'{img_url}')

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
