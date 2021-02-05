import logging
import logging.config
import os


def init_logger():
    """
    Инициализция логера
    :return:
    """
    if os.path.exists("logs"):
        pass
    else:
        os.mkdir("logs")
    logging.config.fileConfig("logger.conf")
    print("Init loggers")
    return logging.getLogger("infoLogger"), logging.getLogger("errorLogger")


def generate_message(prefix_msg: str, msg: str, **kwargs):
    """
    Генерация сообщения лога для журнала
    :param prefix_msg: str
    :param msg: str
    :param kwargs: dict
    :return: str
    """
    msg = f"{prefix_msg}: {msg}\n"
    if kwargs:
        # print(kwargs)
        msg += f"Additional info:"
        for key, value in kwargs.items():
            msg += f"\n{key}: {value}"
    return msg


info_logger, traceback_logger = init_logger()
