import traceback

from lifeguard import NORMAL, PROBLEM
from lifeguard.http_client import get
from lifeguard.logger import lifeguard_logger as logger
from lifeguard.validations import ValidationResponse


def simple_http_validation(url, status_code=200):
    status = NORMAL
    details = {}
    settings = {"notification": {"data": {"url": url}}}

    try:
        response = get(url)
        logger.info("status code %s from %s", response.status_code, url)
        settings["notification"]["data"]["status"] = response.status_code

        if response.status_code != status_code:
            status = PROBLEM
    except Exception as error:
        status = PROBLEM
        details["error"] = traceback.format_exc()
        settings["notification"]["data"]["error"] = str(error)

    return ValidationResponse(status, details, settings)
