from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
from astrbot.api import AstrBotConfig
import aiohttp

@register("随机小姐姐", "柠柚", "获取随机小姐姐视频的插件", "1.0.1")
class RandomBeautyVideoPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        
        # 从配置中获取API相关参数
        self.api_url = self.config.get("api_url", "https://api.nycnm.cn/api/v2/video")
        self.api_key = self.config.get("api_key", "")
        self.video_type = self.config.get("video_type", "mp4")
        self.timeout = self.config.get("timeout", 30)
        
        self.session = aiohttp.ClientSession()
        
    async def terminate(self):
        await self.session.close()
        
    @filter.command("小姐姐", alias=["随机小姐姐", "看小姐姐", "美女视频", "看美女"])
    async def random_beauty_video(self, event: AstrMessageEvent):
        try:
            # 构建请求参数
            params = {
                "type": self.video_type,
                "apikey": self.api_key
            }
            
            # 设置超时
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with self.session.get(self.api_url, params=params, timeout=timeout) as response:
                if response.status == 200:
                    video_component = Video.fromURL(self.api_url + f"?type={self.video_type}&apikey={self.api_key}")
                    yield event.chain_result([video_component])
                else:
                    yield event.plain_result("获取视频失败 请稍后重试")
        except Exception:
            yield event.plain_result("视频异常 请稍后重试")