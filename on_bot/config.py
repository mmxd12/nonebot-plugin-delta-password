from pydantic import BaseModel, ConfigDict
from typing import Set

class Config(BaseModel):
    # API配置
    delta_password_api: str = "https://tmini.net/api/sjzmm?type=json"
    
    # 命令配置
    delta_password_cmd: str = "每日密码"
    delta_password_aliases: Set[str] = {"密码", "delta密码", "今日密码", "三角洲密码"}
    
    model_config = ConfigDict(extra="ignore")