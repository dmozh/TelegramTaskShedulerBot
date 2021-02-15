import requests
import logger
import settings
from enum import Enum


class TypeRequest(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


def send_request(host: str, api_url: str, request_type: TypeRequest, headers: dict = None, body: dict = None,
                 query_params: dict = None):
    """
    Общая функция отправки запроса
    :param host:
    :param api_url: str
    :param request_type: enum
    :param headers: dict
    :param body: dict
    :param query_params: dict
    :return: request.Response
    """
    if headers is not None:
        for key, value in headers.items():
            headers[key] = value
    else:
        headers = headers

    url = host+api_url
    response = None
    try:
        logger.info_logger.info(
            logger.generate_message(f"{request_type.name} request",
                                    f"Запрос к {url}\n"
                                    f"Параметры запроса: {query_params}\n"
                                    f"Тело запроса: {body}"))
        if request_type == request_type.GET:
            response = requests.get(url, headers=headers, params=query_params)
        elif request_type == request_type.POST:
            response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            logger.info_logger.info(
                logger.generate_message(f"{request_type.name} request",
                                        f"Запрос к {url} успешно завершен. Код статус: {response.status_code}",
                                        headers=response.headers))
        else:
            logger.info_logger.warning(
                logger.generate_message(f"{request_type.name} request", f"Запрос к {url} завершен, но ответ "
                                        f"не был получен из-за ошибки. Код статуса ошибки: {response.status_code}",
                                        headers=response.headers))
    except requests.exceptions.ConnectionError as err:
        logger.info_logger.error(
            logger.generate_message(f"{request_type.name} request",
                                    f"{err}\n"
                                    f"Запрос к {url} не смог получить ответа. Код статус: {500}"))
    except TimeoutError as e:
        logger.info_logger.error(
            logger.generate_message(f"{request_type.name} request",
                                    f"{e}\n"
                                    f"Запрос к {url} не смог получить ответа. Код статус: {500}"))
    except Exception as exception:
        logger.traceback_logger.critical(exception, exc_info=True)
    return response


