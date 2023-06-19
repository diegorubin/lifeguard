import mariadb
import yaml

from os.path import join, abspath, dirname
from datetime import datetime

from lifeguard.logger import lifeguard_logger as logger
from lifeguard_telegram.bot import bot_handler

from lifeguard_openai.infrastructure.prompt import execute_prompt


from bot_handlers import valid_request
from custom_settings import (
    PROMPT_LANG,
    LAKE_DATABASE_HOST,
    LAKE_DATABASE_USER,
    LAKE_DATABASE_PASSWORD,
    LAKE_DATABASE_NAME,
)

current_directory = dirname(abspath(__file__))
with open(join(current_directory, "personal.yaml")) as file:
    CONTEXT = yaml.load(file, Loader=yaml.FullLoader)


@bot_handler("personal")
def cluster(update, _context):
    conn = mariadb.connect(
        host=LAKE_DATABASE_HOST,
        user=LAKE_DATABASE_USER,
        password=LAKE_DATABASE_PASSWORD,
        database=LAKE_DATABASE_NAME,
    )
    cursor = conn.cursor()

    if not valid_request(update):
        return

    question = update.message.to_dict()["text"].replace("/personal", "")
    today = datetime.now().strftime("%Y-%m-%d")

    response = execute_prompt(
        CONTEXT["discover_dates_prompt_template"][PROMPT_LANG]
        .replace("QUESTION", question)
        .replace("TODAY", today)
    )

    logger.info("response days: %s", response)

    infos = []
    days = response.split("\n")
    for day in days:
        if day:
            cursor.execute("SELECT content FROM daily_logs WHERE day = ?", (day,))
            result = cursor.fetchall()
            if result:
                infos.append(result[0][0])

    if not infos:
        cursor.execute(
            "SELECT content, day, match(content) against (%s IN NATURAL LANGUAGE MODE) as 'score' FROM daily_logs WHERE day NOT IN (%s) HAVING score > 0 ORDER BY score desc limit 4",
            (
                question,
                ",".join([f"{day}" for day in days if day]),
            ),
        )
        rows = cursor.fetchall()
        for row in rows:
            infos.append(row[0])
            days.append(row[1])

    logger.info("using days: %s", days)

    infos = "\n".join(infos)
    response = execute_prompt(
        CONTEXT["prompt_template"][PROMPT_LANG]
        .replace("INFOS", infos)
        .replace("QUESTION", question)
    )

    update.message.reply_text(response)
    conn.close()
