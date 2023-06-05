from lifeguard.validations import validation
from lifeguard.actions.database import save_result_into_database
from lifeguard.actions.notifications import notify_in_thread

from lifeguard_k8s.validations.pods import pods_validation


@validation(
    "diegorubindev-namespace-pods",
    actions=[save_result_into_database, notify_in_thread],
    schedule={"every": {"minutes": 1}},
    settings={
        "notification": {
            "template": """{%- if pods %}
There are {{ pods | length }} pod(s) not running:
{%- for pod in pods %}
- {{ pod }}
{%- endfor %}
{% else %}
All pods are running!
{%- endif %}"""
        }
    },
)
def diegorubindev_namespace_pods():
    return pods_validation("diegorubindev")
