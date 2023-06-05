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
    }
)

SETTINGS_MANAGER.settings.update(settings_manager.settings)

STATUS_NOTIFICATION_SERVICE = settings_manager.read_value("STATUS_NOTIFICATION_SERVICE")
STATUS_NOTIFICATION_SERVICE_API_TOKEN = settings_manager.read_value(
    "STATUS_NOTIFICATION_SERVICE_API_TOKEN"
)
