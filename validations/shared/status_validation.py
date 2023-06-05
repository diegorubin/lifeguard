import traceback
import json

from lifeguard import NORMAL, PROBLEM, change_status
from lifeguard.actions.database import save_result_into_database
from lifeguard.http_client import post
from lifeguard.logger import lifeguard_logger as logger
from lifeguard.repositories import ValidationRepository
from lifeguard.validations import validation, ValidationResponse

from custom_settings import (
    STATUS_NOTIFICATION_SERVICE,
    STATUS_NOTIFICATION_SERVICE_API_TOKEN,
)


def _global_status():
    global_status = NORMAL
    repository = ValidationRepository()
    for current_validation in repository.fetch_all_validation_results():
        global_status = change_status(global_status, current_validation.status)
    return global_status


@validation(
    description="lake api server",
    actions=[save_result_into_database],
    schedule={"every": {"minutes": 1}},
    settings={"group": "applications"},
)
def notify_lake_api():
    status = NORMAL
    details = {}

    try:
        response_post = post(
            "{}/api/lifeguard-statuses".format(STATUS_NOTIFICATION_SERVICE),
            data=json.dumps({"data": {"status": _global_status()}}),
            headers={
                "Authorization": f"bearer {STATUS_NOTIFICATION_SERVICE_API_TOKEN}",
                "Content-Type": "application/json",
            },
        )
        logger.info("response from lake %s", response_post.content)

    except:
        status = PROBLEM
        details["error"] = traceback.format_exc()

    return ValidationResponse(status, details)
