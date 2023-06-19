from lifeguard.logger import lifeguard_logger as logger

from custom_settings import BOT_VALID_CHATS


def valid_request(update):
    context = update.message.to_dict()
    logger.info("chat id: %s", context["chat"]["id"])
    if str(context["chat"]["id"]) not in BOT_VALID_CHATS:
        logger.warn("unauthorized request %s", context)
        return False
    return True
