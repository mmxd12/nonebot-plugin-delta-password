# 🔐 三角洲密码插件

一个用于查询《三角洲行动》游戏每日密码和位置图片的 NoneBot2 插件。🎮

## ✨ 功能特点

- 🔐 查询所有地图的每日密码
- 🗺️ 查看特定地图的详细信息  
- 🖼️ 查看地图位置参考图片
- 📱 支持 QQ 官方适配器
- ⚙️ 可自定义命令和别名

## 📦 安装方式

    pip install nonebot-plugin-delta-password


## 🔧 配置方法

在 NoneBot2 的pyproject.toml文件中添加以下配置：

- 在dependencies = [...] 中添加："nonebot-plugin-delta-password>=x.x.x" # 请替换为最新版本号
然后在[tool.nonebot.plugins] 添加：
- "nonebot-plugin-delta-password" = ["nonebot_plugin_delta_password"]


### 📋 基本命令

    | 命令 | 功能 | 示例 |
    |------|------|------|
    | `每日密码` | 显示所有地图密码 | `每日密码` |
    | `每日密码 [地图名]` | 显示地图详细信息 | `每日密码 零号大坝` |
    | `查看图片 [地图名]` | 查看地图位置图片 | `查看图片 长弓溪谷` |
    | `图片 [地图名]` | 查看图片（别名） | `图片 航天基地` |

    ### 🔤 命令别名

    **🔑 密码查询命令别名：**
    - `密码`
    - `delta密码`  
    - `今日密码`
    - `三角洲密码`

    **🖼️ 图片查看命令别名：**
    - `图片`
    - `位置图`
    - `参考图`


## 🔌 支持的适配器

- ✅ OneBot V11
- ✅ QQ官方适配器
- 理论上其他应该能用，个人只用这两个

## ✅ 依赖要求

- Python 3.9+
- httpx 0.28.1+
- NoneBot 2.0.0+

## 📜 许可证

MIT License