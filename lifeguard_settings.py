import lifeguard_telegram
import lifeguard_mongodb
import lifeguard_simple_dashboard

from lifeguard.auth import BASIC_AUTH_METHOD
from custom_settings import API_USERNAME, API_PASSWORD

PLUGINS = [lifeguard_mongodb, lifeguard_telegram, lifeguard_simple_dashboard]


def setup(lifeguard_context):
    lifeguard_context.auth_method = BASIC_AUTH_METHOD
    lifeguard_context.users = [{"username": API_USERNAME, "password": API_PASSWORD}]
    # lifeguard_context.cors_settings = {r"/*": {"origins": "*"}}
