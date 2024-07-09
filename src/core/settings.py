"""
Settings Module.
"""

from functools import lru_cache
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class DatabaseSettings(BaseSettings):
    """
    Database settings class.

    Attributes:
        url (str): Database URL.
        pool_size (int): Connection pool size.
        max_overflow (int): Max overflow.
        echo (bool): If True, print SQL statements. For debugging.
        pool_pre_ping (bool): If True, ping the database before each query.
        pool_recycle (int): Connection pool recycle time in seconds.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="DB_", case_sensitive=False, extra="ignore"
    )
    url: str
    pool_size: int
    max_overflow: int
    echo: bool
    pool_pre_ping: bool
    pool_recycle: int

class ServiceCallerConfig:
    class Anthropic:
        API_KEY: str = os.environ.get('ANTHROPIC_API_KEY')
        MODEL: str = os.environ.get('GPT_MODEL', 'claude-3-opus-20240229')
        MAX_TOKEN: str = os.environ.get('MAX_TOKEN', 1024)
        TEMPERATURE: str = os.environ.get('TEMPERATURE', 0.8)

class BusinessLogicConfig:

    @staticmethod
    def get_system_message(system: str | None = None) -> str | None:
        """
        Get system message. If system is not provided, it will get the default system message.

        Args:
            system (str): System description.

        Returns:
            str: System message.
        """
        try:
            return system or open('src/core/system-message.txt', 'r').read()
        except FileNotFoundError:
            return None


@lru_cache
def load_settings(settings_cls_name: str) -> BaseSettings:
    """
    Load settings.

    Args:
        settings_cls_name (str): Settings class name.

    Returns:
        BaseSettings: Settings class.
    """
    load_dotenv(find_dotenv())
    settings_cls = globals()[settings_cls_name]
    return settings_cls()
