import httpx
from typing import Optional, Dict, Any, List
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.qq import Event, Message, MessageSegment

from .config import Config

# 使用默认配置
global_config = Config()

# 创建命令处理器
password_matcher = on_command(
    global_config.delta_password_cmd,
    aliases=set(global_config.delta_password_aliases),
    priority=10,
    block=True
)

# 查看图片命令
image_matcher = on_command("查看图片", aliases={"图片", "位置图", "参考图"}, priority=10, block=True)

async def fetch_daily_passwords() -> Optional[Dict[str, Any]]:
    """获取每日密码数据"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(global_config.delta_password_api)
            data = response.json()
            return data if data.get('status') == 'success' else None
    except Exception as e:
        print(f"获取密码数据失败: {e}")
        return None

def get_map_info(data: Dict[str, Any], map_name: str) -> Optional[Dict[str, Any]]:
    """获取指定地图的完整信息"""
    if not data or data.get('status') != 'success':
        return None
    
    for pwd in data['data']['passwords']:
        if pwd['map_name'] == map_name:
            return pwd
    return None

@password_matcher.handle()
async def handle_password(event: Event, args: Message = CommandArg()):
    """处理密码查询"""
    arg_text = args.extract_plain_text().strip()
    
    data = await fetch_daily_passwords()
    if not data:
        await password_matcher.finish("❌ 获取密码失败，请稍后重试")
        return
    
    passwords_data = data['data']
    
    if arg_text:
        # 查询特定地图
        map_info = get_map_info(data, arg_text)
        if map_info:
            message = Message([
                MessageSegment.text(f"🗺️ {map_info['map_name']}\n"),
                MessageSegment.text(f"🔐 密码: {map_info['password']}\n"),
                MessageSegment.text(f"📍 位置: {map_info['location_info']['description']}\n"),
                MessageSegment.text(f"🖼️ 图片: {len(map_info['location_info']['images'])}张\n"),
                MessageSegment.text(f"💡 发送「查看图片 {map_info['map_name']}」查看位置图片")
            ])
            await password_matcher.finish(message)
        else:
            await password_matcher.finish(f"❌ 未找到地图: {arg_text}")
    else:
        # 查询所有地图
        message_parts = [
            MessageSegment.text("🎮 三角洲行动 - 今日密码\n"),
            MessageSegment.text("═" * 20 + "\n")
        ]
        
        for pwd in passwords_data['passwords']:
            message_parts.append(MessageSegment.text(f"🗺️ {pwd['map_name']:<6} 🔐 {pwd['password']}\n"))

        message_parts.extend([
            MessageSegment.text("\n🔎如需要搜索价格，请使用“搜索帮助”查看指令\n"),
            MessageSegment.text("\n💡 发送「密码 地图名」查看详细信息\n"),
            MessageSegment.text("💡 发送「查看图片 地图名」查看位置图片\n"),
            MessageSegment.text("💡 支持地图: " + "、".join([pwd['map_name'] for pwd in passwords_data['passwords']]))
        ])
        
        await password_matcher.finish(Message(message_parts))

@image_matcher.handle()
async def handle_images(event: Event, args: Message = CommandArg()):
    """处理查看图片命令 - QQ官方适配器版本"""
    arg_text = args.extract_plain_text().strip()
    
    if not arg_text:
        # 如果没有指定地图，显示所有地图列表
        data = await fetch_daily_passwords()
        if not data:
            await image_matcher.finish("❌ 获取数据失败")
            return
        
        message_parts = [MessageSegment.text("🖼️ 可查看图片的地图列表:\n")]
        message_parts.append(MessageSegment.text("═" * 20 + "\n"))
        
        for pwd in data['data']['passwords']:
            image_count = len(pwd['location_info']['images'])
            message_parts.append(MessageSegment.text(f"🗺️ {pwd['map_name']} ({image_count}张图片)\n"))
        
        message_parts.append(MessageSegment.text("\n💡 发送「查看图片 地图名」查看具体图片"))
        await image_matcher.finish(Message(message_parts))
        return
    
    data = await fetch_daily_passwords()
    if not data:
        await image_matcher.finish("❌ 获取数据失败，请稍后重试")
        return
    
    map_info = get_map_info(data, arg_text)
    if not map_info:
        await image_matcher.finish(f"❌ 未找到地图 '{arg_text}'")
        return
    
    images = map_info['location_info']['images']
    if not images:
        await image_matcher.finish(f"❌ 地图 '{arg_text}' 暂无位置图片")
        return
    
    # 先发送文本信息
    await image_matcher.send(Message([
        MessageSegment.text(f"🖼️ {map_info['map_name']} - 位置参考图\n"),
        MessageSegment.text(f"📸 共 {len(images)} 张图片")
    ]))
    
    # QQ官方适配器发送图片的方式
    for i, img_url in enumerate(images, 1):
        try:
            # 方法1: 使用file_image（如果支持）
            image_msg = Message([
                MessageSegment.text(f"📎 图{i}:\n"),
                MessageSegment.file_image(img_url)  # QQ官方适配器可能使用file_image
            ])
            await image_matcher.send(image_msg)
        except Exception as e:
            try:
                # 方法2: 使用image
                image_msg = Message([
                    MessageSegment.text(f"📎 图{i}:\n"),
                    MessageSegment.image(img_url)
                ])
                await image_matcher.send(image_msg)
            except Exception as e2:
                # 方法3: 如果都失败，发送链接
                await image_matcher.send(f"📎 图{i}: {img_url}")
    
    # 结束处理
    await image_matcher.finish("✅ 图片发送完成")