import re
import yaml

from os.path import join, abspath, dirname

from lifeguard.logger import lifeguard_logger as logger
from lifeguard_telegram.bot import bot_handler

from lifeguard_k8s.infrastructure.pods import (
    get_namespace_infos,
    delete_a_pod,
    get_last_error_event_from_pod,
)
from lifeguard_openai.infrastructure.prompt import execute_prompt

from bot_handlers import valid_request
from custom_settings import PROMPT_LANG


current_directory = dirname(abspath(__file__))
with open(join(current_directory, "cluster.yaml")) as file:
    CONTEXT = yaml.load(file, Loader=yaml.FullLoader)


def restart_pod(update, pod_name):
    logger.info("restart pod %s", pod_name)
    delete_a_pod("diegorubindev", pod_name)
    update.message.reply_text(f"reiniciando pod {pod_name}")


def explain_pod_error(update, pod_name):
    logger.info("explain pod error %s", pod_name)
    response = execute_prompt(
        CONTEXT["explain_pod_error_prompt_template"][PROMPT_LANG].replace(
            "ERROR", get_last_error_event_from_pod("diegorubindev", pod_name)
        )
    )
    update.message.reply_text(response)


def _execute_commands(update, response):
    for command in CONTEXT["commands"]:
        if command["command"] in response:
            logger.info("executing command %s", command["command"])
            regex = re.compile(f"{command['command']} (.*)")
            arg = regex.search(response).group(1)
            function = globals()[command["command"].replace(" ", "_")]
            function(update, arg)
            return True
    return False


def _build_infos(namespace_infos):
    infos = ["nome,status,restarts"]
    for pod in namespace_infos["pods"]:
        infos.append(
            f"{pod['name']},{pod['status']},{pod['containers'][0]['restart_count']}"
        )

    return "\n".join(infos)


def _build_commands(commands):
    return "\n\n".join([command["definitions"][PROMPT_LANG] for command in commands])


@bot_handler("cluster")
def cluster(update, _context):
    if not valid_request(update):
        return
    question = update.message.to_dict()["text"].replace("/cluster ", "")

    namespace_infos = get_namespace_infos("diegorubindev")

    prompt = (
        CONTEXT["prompt_template"][PROMPT_LANG]
        .replace("INFOS", _build_infos(namespace_infos))
        .replace("COMMANDS", _build_commands(CONTEXT["commands"]))
        .replace("QUESTION", question)
    )

    logger.info("prompt: %s", prompt)

    response = execute_prompt(prompt)

    logger.info("response: %s", response)

    if not _execute_commands(update, response):
        update.message.reply_text(response)
