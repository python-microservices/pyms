"""Encapsulate common rest operations between business services propagating trace headers if configured.
"""
import logging

import opentracing
import requests
from flask import current_app, request
from opentracing_instrumentation import get_current_span
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService

logger = logging.getLogger(LOGGER_NAME)

DEFAULT_RETRIES = 3

DEFAULT_STATUS_RETRIES = (500, 502, 504)


def retry(f):
    def wrapper(*args, **kwargs):
        response = False
        i = 0
        response_ok = False
        retries = args[0]._retries
        status_retries = args[0]._status_retries
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
    service = "requests"
    default_values = {
        "data": ""
    }
    tracer = None
    _retries = DEFAULT_RETRIES
    _status_retries = DEFAULT_STATUS_RETRIES
    _propagate_headers = False

    def __init__(self, service, *args, **kwargs):
        """Initialization for trace headers propagation"""
        super().__init__(service, *args, **kwargs)
        if self.exists_config():
            self._retries = self.config.retries or DEFAULT_RETRIES
            self._status_retries = self.config.status_retries or DEFAULT_STATUS_RETRIES
            self._propagate_headers = self.config.propagate_headers

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
        retry = Retry(
            total=self._retries,
            read=self._retries,
            connect=self._retries,
            backoff_factor=0.3,
            status_forcelist=self._status_retries,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session_r.mount('http://', adapter)
        session_r.mount('https://', adapter)
        return session_r

    def insert_trace_headers(self, headers: dict) -> dict:
        """Inject trace headers if enabled.

        :param headers: dictionary of HTTP Headers to send.

        :rtype: dict
        """

        try:
            # FLASK https://github.com/opentracing-contrib/python-flask
            span = self.tracer.get_span(request=request)
            if not span:  # pragma: no cover
                span = get_current_span()
                if not span:
                    span = self.tracer.tracer.start_span()
            context = span.context if span else None
            self._tracer.tracer.inject(context, opentracing.Format.HTTP_HEADERS, headers)
        except Exception as ex:
            logger.debug("Tracer error {}".format(ex))
        return headers

    @staticmethod
    def propagate_headers(headers: dict) -> dict:
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

        self.tracer = current_app.tracer
        if self.tracer:
            headers = self.insert_trace_headers(headers)
        if self._propagate_headers or propagate_headers:
            headers = self.propagate_headers(headers)
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
            if self.config.data:
                data = data.get(self.config.data, {})
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
        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        full_url = self._build_url(url, path_params)
        headers = self._get_headers(headers=headers, propagate_headers=propagate_headers)
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
        logger.debug("Delete with url {}, headers {}, kwargs {}".format(full_url, headers, kwargs))

        session = requests.Session()
        response = self.requests(session=session).delete(full_url, headers=headers, **kwargs)
        logger.debug("Response {}".format(response))

        return response
