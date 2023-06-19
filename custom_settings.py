import os
from lifeguard.settings import SettingsManager, SETTINGS_MANAGER

settings_manager = SettingsManager(
    {
        "STATUS_NOTIFICATION_SERVICE": {
            "default": "",
            "description": "Base url of status notification service",
        },
        "STATUS_NOTIFICATION_SERVICE_API_TOKEN": {
            "default": "",
            "description": "Api token of status notification service",
        },
        "API_USERNAME": {
            "default": "",
            "description": "Username to access lifeguard",
        },
        "API_PASSWORD": {
            "default": "",
            "description": "Password to access lifeguard",
        },
        "BOT_VALID_CHATS": {
            "default": "",
            "type": "list",
            "description": "Valid chats to access bot",
        },
        "PROMPT_LANG": {
            "default": "pt_br",
            "description": "Language to execute prompt",
        },
        "LAKE_DATABASE_HOST": {
            "default": "127.0.0.1",
            "description": "Database host",
        },
        "LAKE_DATABASE_USER": {
            "default": "",
            "description": "Database user",
        },
        "LAKE_DATABASE_PASSWORD": {
            "default": "",
            "description": "Database password",
        },
        "LAKE_DATABASE_NAME": {
            "default": "",
            "description": "Database name",
        },
    }
)

SETTINGS_MANAGER.settings.update(settings_manager.settings)

STATUS_NOTIFICATION_SERVICE = settings_manager.read_value("STATUS_NOTIFICATION_SERVICE")
STATUS_NOTIFICATION_SERVICE_API_TOKEN = settings_manager.read_value(
    "STATUS_NOTIFICATION_SERVICE_API_TOKEN"
)

API_USERNAME = settings_manager.read_value("API_USERNAME")
API_PASSWORD = settings_manager.read_value("API_PASSWORD")

BOT_VALID_CHATS = settings_manager.read_value("BOT_VALID_CHATS")

PROMPT_LANG = settings_manager.read_value("PROMPT_LANG")

LAKE_DATABASE_HOST = settings_manager.read_value("LAKE_DATABASE_HOST")
LAKE_DATABASE_USER = settings_manager.read_value("LAKE_DATABASE_USER")
LAKE_DATABASE_PASSWORD = settings_manager.read_value("LAKE_DATABASE_PASSWORD")
LAKE_DATABASE_NAME = settings_manager.read_value("LAKE_DATABASE_NAME")
