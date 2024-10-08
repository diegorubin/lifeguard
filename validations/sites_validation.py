from lifeguard.actions.database import save_result_into_database
from lifeguard.actions.notifications import notify_in_thread
from lifeguard.validations import validation

from validations.shared.simple_http_validation import simple_http_validation

NOTIFICATION_SETTINGS = {
    "template": """*url*: {{url}}
{%- if status %}
*status*: {{status}}
{%- endif %}
{%- if error %}
*error*: {{error}}
{%- endif %}
""",
}


@validation(
    group="site",
    description="status page",
    actions=[save_result_into_database, notify_in_thread],
    schedule={"every": {"minutes": 5}},
    settings={"notification": NOTIFICATION_SETTINGS},
)
def status_page():
    return simple_http_validation("https://status.diegorubin.dev")


@validation(
    group="site",
    description="urlshortener",
    actions=[save_result_into_database],
    schedule={"every": {"minutes": 5}},
    settings={"notification": NOTIFICATION_SETTINGS},
)
def urlshortener():
    return simple_http_validation("https://drub.in/login")
