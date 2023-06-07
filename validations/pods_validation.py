from lifeguard.validations import validation
from lifeguard.actions.database import save_result_into_database
from lifeguard.actions.notifications import notify_in_thread

from lifeguard_k8s.validations.pods import pods_validation
from lifeguard_openai.actions.errors import explain_error


@validation(
    "diegorubindev-namespace-pods",
    actions=[explain_error, save_result_into_database, notify_in_thread],
    schedule={"every": {"minutes": 1}},
    settings={
        "notification": {
            "update_thread_interval": 3600,
            "template": """{%- if pods %}
There are {{ pods | length }} pod(s) not running:
{%- for pod in pods %}
{{loop.index}}. {{ pod }}: {{ explanation[loop.index - 1] }}
{%- endfor %}
{% else %}
All pods are running!
{%- endif %}""",
        }
    },
)
def diegorubindev_namespace_pods():
    return pods_validation("diegorubindev")
