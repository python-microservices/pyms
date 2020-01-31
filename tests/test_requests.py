"""Test common rest operations wrapper.
"""
import json
import os
import unittest

import requests_mock

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice
from pyms.flask.services.requests import DEFAULT_RETRIES


class RequestServiceNoDataTests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-requests-no-data.yml")
        ms = Microservice(path=__file__)
        self.app = ms.create_app()
        self.request = ms.requests

    @requests_mock.Mocker()
    def test_get(self, mock_request):
        url = "http://www.my-site.com/users"
        full_url = url
        text = json.dumps([{'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'},
                           {'id': 2, 'name': 'Jon', 'email': 'jon@my-site.com.com'}])

        with self.app.app_context():
            mock_request.get(full_url, text=text)
            response = self.request.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(text, response.text)


class RequestServiceTests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-requests.yml")
        ms = Microservice(path=__file__)
        self.app = ms.create_app()
        self.request = ms.requests

    @requests_mock.Mocker()
    def test_get(self, mock_request):
        url = "http://www.my-site.com/users"
        full_url = url
        text = json.dumps({'data': [{'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'},
                                    {'id': 2, 'name': 'Jon', 'email': 'jon@my-site.com.com'}]})

        with self.app.app_context():
            mock_request.get(full_url, text=text)
            response = self.request.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(text, response.text)

    @requests_mock.Mocker()
    def test_get_for_object_without_json(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}/posts"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123/posts"
        expected = {}

        with self.app.app_context():
            mock_request.get(full_url)
            response = self.request.get_for_object(url, path_params)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_get_for_object_without_valid_json_data(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}/posts"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123/posts"
        text = json.dumps({'another_data': [{'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'},
                                            {'id': 2, 'name': 'Jon', 'email': 'jon@my-site.com.com'}]})
        expected = {}

        with self.app.app_context():
            mock_request.get(full_url, text=text)
            response = self.request.get_for_object(url, path_params)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_get_for_object_with_valid_data(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}/posts"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123/posts"
        text = json.dumps({'data': [{'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'},
                                    {'id': 2, 'name': 'Jon', 'email': 'jon@my-site.com.com'}]})
        expected = [{'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'},
                    {'id': 2, 'name': 'Jon', 'email': 'jon@my-site.com.com'}]

        with self.app.app_context():
            mock_request.get(full_url, text=text)
            response = self.request.get_for_object(url, path_params)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_post(self, mock_request):
        url = "http://www.my-site.com/users"
        full_url = url
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        text = json.dumps({'data': {'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com'}})

        with self.app.app_context():
            mock_request.post(full_url, text=text, status_code=201)
            response = self.request.post(url, json=user)

        self.assertEqual(201, response.status_code)
        self.assertEqual(text, response.text)

    @requests_mock.Mocker()
    def test_post_for_object_without_json(self, mock_request):
        url = "http://www.my-site.com/users"
        full_url = url
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        expected = {}

        with self.app.app_context():
            mock_request.post(full_url, status_code=201)
            response = self.request.post_for_object(url, json=user)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_post_for_object_without_valid_json_data(self, mock_request):
        url = "http://www.my-site.com/users"
        full_url = url
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        text = json.dumps({'another_data': {'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'}})
        expected = {}

        with self.app.app_context():
            mock_request.post(full_url, text=text, status_code=201)
            response = self.request.post_for_object(url, json=user)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_post_for_object_with_valid_data(self, mock_request):
        url = "http://www.my-site.com/users"
        full_url = url
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        text = json.dumps({'data': {'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'}})
        expected = {'id': 1, 'name': 'Peter', 'email': 'peter@my-site.com.com'}

        with self.app.app_context():
            mock_request.post(full_url, text=text, status_code=201)
            response = self.request.post_for_object(url, json=user)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_put(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123"
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        text = json.dumps({'data': {'id': 123, 'name': 'Peter', 'email': 'peter@my-site.com'}})

        with self.app.app_context():
            mock_request.put(full_url, text=text, status_code=200)
            response = self.request.put(url, path_params, json=user)

        self.assertEqual(200, response.status_code)
        self.assertEqual(text, response.text)

    @requests_mock.Mocker()
    def test_put_for_object_without_json(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123"
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        expected = {}

        with self.app.app_context():
            mock_request.put(full_url, status_code=200)
            response = self.request.put_for_object(url, path_params, json=user)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_put_for_object_without_valid_json_data(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123"
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        text = json.dumps({'another_data': {'id': 123, 'name': 'Peter', 'email': 'peter@my-site.com.com'}})
        expected = {}

        with self.app.app_context():
            mock_request.put(full_url, text=text, status_code=200)
            response = self.request.put_for_object(url, path_params, json=user)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_put_for_object_with_valid_data(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123"
        user = {'name': 'Peter', 'email': 'peter@my-site.com'}
        text = json.dumps({'data': {'id': 123, 'name': 'Peter', 'email': 'peter@my-site.com.com'}})
        expected = {'id': 123, 'name': 'Peter', 'email': 'peter@my-site.com.com'}

        with self.app.app_context():
            mock_request.put(full_url, text=text, status_code=200)
            response = self.request.put_for_object(url, path_params, json=user)

        self.assertEqual(expected, response)

    @requests_mock.Mocker()
    def test_delete(self, mock_request):
        url = "http://www.my-site.com/users/{user-id}"
        path_params = {'user-id': 123}
        full_url = "http://www.my-site.com/users/123"

        with self.app.app_context():
            mock_request.delete(full_url, status_code=204)
            response = self.request.delete(url, path_params)

        self.assertEqual(204, response.status_code)
        self.assertEqual('', response.text)

    def test_propagate_headers_empty(self, ):
        input_headers = {

        }
        expected_headers = {
            'Content-Length': '12',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'localhost'
        }
        with self.app.test_request_context(
                '/tests/', data={'format': 'short'}):
            headers = self.request.set_propagate_headers(input_headers)

        self.assertEqual(expected_headers, headers)

    def test_propagate_headers_no_override(self):
        input_headers = {
            'Host': 'my-server'
        }
        expected_headers = {
            'Host': 'my-server'
        }
        with self.app.test_request_context(
                '/tests/'):
            headers = self.request.set_propagate_headers(input_headers)

        self.assertEqual(expected_headers, headers)

    def test_propagate_headers_propagate(self):
        input_headers = {
        }
        expected_headers = {
            'Content-Length': '12',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'localhost',
            'A': 'b',
        }
        with self.app.test_request_context(
                '/tests/', data={'format': 'short'}, headers={'a': 'b'}):
            headers = self.request.set_propagate_headers(input_headers)

        self.assertEqual(expected_headers, headers)

    def test_propagate_headers_propagate_no_override(self):
        input_headers = {
            'Host': 'my-server',
            'Span': '1234',
        }
        expected_headers = {
            'Host': 'my-server',
            'A': 'b',
            'Span': '1234',
        }
        with self.app.test_request_context(
                '/tests/', headers={'a': 'b', 'span': '5678'}):
            headers = self.request.set_propagate_headers(input_headers)

        self.assertEqual(expected_headers, headers)

    def test_propagate_headers_on_get(self):
        url = "http://www.my-site.com/users"
        mock_headers = {
            'A': 'b',
        }
        self.request.set_propagate_headers = unittest.mock.Mock()
        self.request.set_propagate_headers.return_value = mock_headers
        with self.app.test_request_context(
                '/tests/', data={'format': 'short'}, headers=mock_headers):
            self.request.get(url, propagate_headers=True)

        self.request.set_propagate_headers.assert_called_once_with({})

    def test_propagate_headers_on_get_with_headers(self):
        url = "http://www.my-site.com/users"
        mock_headers = {
            'A': 'b',
        }
        get_headers = {
            'C': 'd',
        }
        self.request.set_propagate_headers = unittest.mock.Mock()
        self.request.set_propagate_headers.return_value = mock_headers
        with self.app.test_request_context(
                '/tests/', data={'format': 'short'}, headers=mock_headers):
            self.request.get(url, headers=get_headers, propagate_headers=True)

        self.request.set_propagate_headers.assert_called_once_with(get_headers)

    @requests_mock.Mocker()
    def test_retries_with_500(self, mock_request):
        url = 'http://localhost:9999'
        with self.app.app_context():
            mock_request.get(url, text="", status_code=500)
            response = self.request.get(url)

        self.assertEqual(DEFAULT_RETRIES, mock_request.call_count)
        self.assertEqual(500, response.status_code)

    @requests_mock.Mocker()
    def test_retries_with_200(self, mock_request):
        url = 'http://localhost:9999'
        with self.app.app_context():
            mock_request.get(url, text="", status_code=200)
            response = self.request.get(url)

        self.assertEqual(1, mock_request.call_count)
        self.assertEqual(200, response.status_code)
