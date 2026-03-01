"""
配置管理
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # API-Football Key (免费注册: https://dashboard.api-football.com/)
    API_FOOTBALL_KEY: str = os.getenv("API_FOOTBALL_KEY", "")
    
    # FastAPI 配置
    APP_NAME: str = "EA FC Live Dashboard"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # WebSocket
    WS_HEARTBEAT: int = 30  # 心跳间隔（秒）
    
    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置
settings = get_settings()
