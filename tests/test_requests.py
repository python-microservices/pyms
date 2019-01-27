"""Test common rest operations wrapper.
"""
import json
import os
import unittest

import requests_mock

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice


class RequestServiceTests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")
        ms = Microservice(service="my-ms", path=__file__)
        self.app = ms.create_app()
        with self.app.app_context():
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
