from __future__ import annotations

import logging
import sys

import openai

from src.constants import LOGGING_FORMAT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(LOGGING_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def check_openai_api_key(api_key):
    openai.api_key = api_key
    try:
        openai.Model.list()
    except openai.error.AuthenticationError:
        logger.error(
            "The API key is invalid, please check your keys at: %s",
            "https://platform.openai.com/account/api-keys",
        )
        return False
    else:
        logger.info("The API key is valid!")
        return True
