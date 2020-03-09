"""Encapsulate common rest operations between business services propagating trace headers if configured.
"""
import logging

import requests
from flask import request
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService
from pyms.flask.services.tracer import inject_span_in_headers

logger = logging.getLogger(LOGGER_NAME)

DEFAULT_RETRIES = 3

DEFAULT_STATUS_RETRIES = (500, 502, 504)


def retry(f):
    def wrapper(*args, **kwargs):
        response = False
        i = 0
        response_ok = False
        retries = args[0].retries
        status_retries = args[0].status_retries
        while i < retries and response_ok is False:
            response = f(*args, **kwargs)
            i += 1
            if response.status_code not in status_retries:
                response_ok = True
                logger.debug("Response {}".format(response))
        if not response_ok:
            logger.warning("Response ERROR: {}".format(response))
        return response

    return wrapper


class Service(DriverService):
    """
    Extend the [requests library](http://docs.python-requests.org/en/master/) with trace headers and parsing JSON objects.
    Encapsulate common rest operations between business services propagating trace headers if set up.
    All default values keys are created as class attributes in `DriverService`
    """
    service = "requests"
    default_values = {
        "data": "",
        "retries": DEFAULT_RETRIES,
        "status_retries": DEFAULT_STATUS_RETRIES,
        "propagate_headers": False,
    }
    tracer = None

    def requests(self, session: requests.Session):
        """
        A backoff factor to apply between attempts after the second try (most errors are resolved immediately by a
        second try without a delay). urllib3 will sleep for: {backoff factor} * (2 ^ ({number of total retries} - 1))
        seconds. If the backoff_factor is 0.1, then sleep() will sleep for [0.0s, 0.2s, 0.4s, ...] between retries.
        It will never be longer than Retry.BACKOFF_MAX. By default, backoff is disabled (set to 0).
        :param session:
        :return:
        """
        session_r = session or requests.Session()
        max_retries = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=0.3,
            status_forcelist=self.status_retries,
        )
        adapter = HTTPAdapter(max_retries=max_retries)
        session_r.mount('http://', adapter)
        session_r.mount('https://', adapter)
        return session_r

    @staticmethod
    def insert_trace_headers(headers: dict) -> dict:
        """Inject trace headers if enabled.

        :param headers: dictionary of HTTP Headers to send.

        :rtype: dict
        """

        try:
            headers = inject_span_in_headers(headers)
        except Exception as ex:  # pragma: no cover
            logger.debug("Tracer error {}".format(ex))
        return headers

    @staticmethod
    def set_propagate_headers(headers: dict) -> dict:
        for k, v in request.headers:
            if not headers.get(k):
                headers.update({k: v})
        return headers

    def _get_headers(self, headers, propagate_headers=False):
        """If enabled appends trace headers to received ones.

        :param headers: dictionary of HTTP Headers to send.

        :rtype: dict
        """

        if not headers:
            headers = {}

        if self._propagate_headers or propagate_headers:
            headers = self.set_propagate_headers(headers)
        return headers

    @staticmethod
    def _build_url(url, path_params=None):
        """Compose full url replacing placeholders with path_params values.

        :param url: base url
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :return: :class:`string`
        :rtype: string
        """

        return url.format_map(path_params)

    def parse_response(self, response):
        """Parses response's json object. Checks configuration in order to parse a concrete node or the whole response.

        :param response: request's response that contains a valid json

        :rtype: dict
        """

        try:
            data = response.json()
            if self.data:
                data = data.get(self.data, {})
            return data
        except ValueError:
            logger.warning("Response.content is not a valid json {}".format(response.content))
            return {}

    @retry
    def get(self, url, path_params=None, params=None, headers=None, propagate_headers=False, **kwargs):
        """Sends a GET request.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param params: (optional) Dictionary, list of tuples or bytes to send in the body of the :class:`Request` (as query
                    string parameters)
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param propagate_headers: Optional arguments that ``request`` takes.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        full_url = self._build_url(url, path_params)
        headers = self._get_headers(headers=headers, propagate_headers=propagate_headers)
        headers = self.insert_trace_headers(headers)
        logger.debug("Get with url {}, params {}, headers {}, kwargs {}".
                     format(full_url, params, headers, kwargs))

        session = requests.Session()
        response = self.requests(session=session).get(full_url, params=params, headers=headers, **kwargs)

        return response

    def get_for_object(self, url, path_params=None, params=None, headers=None, **kwargs):
        """Sends a GET request and returns the json representation found in response's content data node.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param params: (optional) Dictionary, list of tuples or bytes to send in the body of the :class:`Request` (as query
                    string parameters)
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        response = self.get(url, path_params=path_params, params=params, headers=headers, **kwargs)
        return self.parse_response(response)

    @retry
    def post(self, url, path_params=None, data=None, json=None, headers=None, **kwargs):
        """Sends a POST request.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the
                    :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        full_url = self._build_url(url, path_params)
        headers = self._get_headers(headers)
        headers = self.insert_trace_headers(headers)
        logger.debug("Post with url {}, data {}, json {}, headers {}, kwargs {}".format(full_url, data, json,
                                                                                        headers, kwargs))

        session = requests.Session()
        response = self.requests(session=session).post(full_url, data=data, json=json, headers=headers, **kwargs)
        logger.debug("Response {}".format(response))

        return response

    def post_for_object(self, url, path_params=None, data=None, json=None, headers=None, **kwargs):
        """Sends a POST request and returns the json representation found in response's content data node.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the
                    :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        response = self.post(url, path_params=path_params, data=data, json=json, headers=headers, **kwargs)
        return self.parse_response(response)

    @retry
    def put(self, url, path_params=None, data=None, headers=None, **kwargs):
        """Sends a PUT request.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        full_url = self._build_url(url, path_params)
        headers = self._get_headers(headers)
        headers = self.insert_trace_headers(headers)
        logger.debug("Put with url {}, data {}, headers {}, kwargs {}".format(full_url, data, headers,
                                                                              kwargs))

        session = requests.Session()
        response = self.requests(session=session).put(full_url, data, headers=headers, **kwargs)
        logger.debug("Response {}".format(response))

        return response

    def put_for_object(self, url, path_params=None, data=None, headers=None, **kwargs):
        """Sends a PUT request and returns the json representation found in response's content data node.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        response = self.put(url, path_params=path_params, data=data, headers=headers, **kwargs)
        return self.parse_response(response)

    @retry
    def delete(self, url, path_params=None, headers=None, **kwargs):
        """Sends a DELETE request.

        :param url: URL for the new :class:`Request` object. Could contain path parameters
        :param path_params: (optional) Dictionary, list of tuples with path parameters values to compose url
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        full_url = self._build_url(url, path_params)
        headers = self._get_headers(headers)
        headers = self.insert_trace_headers(headers)
        logger.debug("Delete with url {}, headers {}, kwargs {}".format(full_url, headers, kwargs))

        session = requests.Session()
        response = self.requests(session=session).delete(full_url, headers=headers, **kwargs)
        logger.debug("Response {}".format(response))

        return response
