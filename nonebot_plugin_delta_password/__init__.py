from nonebot.plugin import PluginMetadata
from .handler import password_matcher, image_matcher

__plugin_meta__ = PluginMetadata(
    name="三角洲密码",
    description="查询三角洲行动每日密码和位置图片",
    usage=(
        "【命令列表】\n"
        "1. 每日密码 - 显示所有地图密码\n"
        "2. 每日密码 [地图名] - 显示地图详细信息\n"
        "3. 查看图片 [地图名] - 查看地图位置图片\n"
        "\n"
        "【示例】\n"
        "每日密码\n"
        "每日密码 零号大坝\n"
        "查看图片 长弓溪谷\n"
        "图片 航天基地"
    ),
    type="application",
)

__all__ = ["password_matcher", "image_matcher"]