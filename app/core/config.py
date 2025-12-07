from dataclasses import dataclass
import os
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    secret_key: str
    algorithm: str
    access_token_expire_seconds: int
    auth_username: str
    auth_password: str
    dev_mode: bool  # 開発モード: True の場合は認証をバイパス


@lru_cache
def get_settings() -> Settings:
    return Settings(
        secret_key=os.getenv("AUTH_SECRET_KEY", "change-me"),
        algorithm=os.getenv("AUTH_ALGORITHM", "HS256"),
        access_token_expire_seconds=int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "10800")),
        auth_username=os.getenv("ADMIN_USERNAME", "admin"),
        auth_password=os.getenv("ADMIN_PASSWORD", "admin"),
        dev_mode=os.getenv("DEV_MODE", "false").lower() == "true",
    )


def reset_settings_cache() -> None:
    """Clear the cached settings. Mainly helpful for tests."""
    get_settings.cache_clear()
