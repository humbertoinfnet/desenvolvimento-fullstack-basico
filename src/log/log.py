import logging
import json


def format_logger() -> None:
    """
    Função responsável pela formatação do Logger
    """
    log_format = {
        'asctime': '%(asctime)s',
        'name': '%(name)s',
        'levelname': '%(levelname)s',
        'message': '%(message)r',
        'pathname': '%(pathname)s',
        'lineno': '%(lineno)d',
        'funcName': '%(funcName)s',
        'filename': '%(filename)s'
    }

    formatter = logging.Formatter(json.dumps(log_format, ensure_ascii=False))
    file_handler = logging.FileHandler('src/log/app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
