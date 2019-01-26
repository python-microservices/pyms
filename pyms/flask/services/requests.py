"""Encapsulate common rest operations between business services propagating trace headers if configured.
"""
import logging

import opentracing
import requests
from flask import current_app, request

from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService

logger = logging.getLogger(LOGGER_NAME)


class Service(DriverService):
    service = "requests"
    default_values = {
        "data": ""
    }

    def __init__(self, service, *args, **kwargs):
        """Initialization for trace headers propagation"""
        super().__init__(service, *args, **kwargs)

    def insert_trace_headers(self, headers):
        """Inject trace headers if enabled.

        :param headers: dictionary of HTTP Headers to send.

        :rtype: dict
        """

        try:
            # FLASK https://github.com/opentracing-contrib/python-flask
            span = self._tracer.get_span(request)
            self._tracer.tracer.inject(span.context, opentracing.Format.HTTP_HEADERS, headers)
        except Exception as ex:
            logger.debug("Tracer error {}".format(ex))
        return headers

    def _get_headers(self, headers):
        """If enabled appends trace headers to received ones.

        :param headers: dictionary of HTTP Headers to send.

        :rtype: dict
        """

        if not headers:
            headers = {}

        self._tracer = current_app.tracer
        if self._tracer:
            headers = self.insert_trace_headers(headers)

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
            current_app.logger.warning("Response.content is not a valid json {}".format(response.content))
            return {}

    def get(self, url, path_params=None, params=None, headers=None, **kwargs):
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
        headers = self._get_headers(headers)
        current_app.logger.info("Get with url {}, params {}, headers {}, kwargs {}".
                                format(full_url, params, headers, kwargs))
        response = requests.get(full_url, params=params, headers=headers, **kwargs)
        current_app.logger.info("Response {}".format(response))

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
        current_app.logger.info("Post with url {}, data {}, json {}, headers {}, kwargs {}".format(full_url, data, json,
                                                                                                   headers, kwargs))
        response = requests.post(full_url, data=data, json=json, headers=headers, **kwargs)
        current_app.logger.info("Response {}".format(response))

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
        current_app.logger.info("Put with url {}, data {}, headers {}, kwargs {}".format(full_url, data, headers,
                                                                                         kwargs))
        response = requests.put(full_url, data, headers=headers, **kwargs)
        current_app.logger.info("Response {}".format(response))

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
        current_app.logger.info("Delete with url {}, headers {}, kwargs {}".format(full_url, headers, kwargs))
        response = requests.delete(full_url, headers=headers, **kwargs)
        current_app.logger.info("Response {}".format(response))

        return response
