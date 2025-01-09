import os
import sys

import tomli
from box import Box
from loguru import logger
from .generate_self_signed_certs import generate_self_signed_cert
API_TOKEN = "ahG9rae2eipakah4Sia3eevieyiegu"

logger.remove()  # Entfernt den Standard-Handler
logger.add(
    sys.stdout,
    format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}',
    colorize=True
)

with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)

PROJECT_NAME = pyproject['tool']['poetry']['name']


def load_config():
    paths = [
        f'/etc/{PROJECT_NAME}/{PROJECT_NAME}.conf',
        os.path.expanduser("~/.config/{PROJECT_NAME}/{PROJECT_NAME}.conf"),
        "./env/env.toml"
    ]

    for path in paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                doc = tomli.load(f)
                logger.trace(doc)
                config = Box(doc)

                if not hasattr(config, 'ssl'):
                    config.ssl = Box({})

                if not hasattr(config.ssl, 'cert') or config.ssl.cert is None:
                    config.ssl.cert = f'/etc/{PROJECT_NAME}/cert.pem'

                if not hasattr(config.ssl, 'key') or config.ssl.key is None:
                    config.ssl.key = f'/etc/{PROJECT_NAME}/key.pem'

                if not os.path.isfile(config.ssl.cert) and not os.path.isfile(config.ssl.key):
                    # generate new self signed certificate
                    generate_self_signed_cert(config.ssl.cert, config.ssl.key)

                assert config.auth.api_tokens is not None
                return config
    raise FileNotFoundError("Could not load configuration!")


config = load_config()


