import unittest
from unittest.mock import Mock, patch

from ....libs.clients.open_whisk_client import (OpenWhiskClient,
                                                OpenWhiskClientException)


class OpenWhiskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.namespace = "guest"
        self.client = OpenWhiskClient()

    def _mock_response(self, status_code=200, content="",
                       json_data=None, raise_for_status=None):
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status_code
        mock_resp.content = content
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
        return mock_resp

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_list_trigger_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        resp = self.client.list_trigger(self.namespace)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_list_trigger_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.list_trigger(self.namespace)

    @patch('core.libs.clients.open_whisk_client.requests.put')
    def test_create_trigger_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        data = {
            "name": "trigger1",
            "annotations": [{
                "key": "feed",
                "value": "/whisk.system/alarms/alarm"}]
        }
        resp = self.client.create_trigger(self.namespace, data)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.put')
    def test_create_trigger_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.create_trigger(self.namespace, {})

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_retrieve_trigger_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        resp = self.client.retrieve_trigger("trigger1", self.namespace)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_retrieve_trigger_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.retrieve_trigger("trigger1", self.namespace)

    @patch('core.libs.clients.open_whisk_client.requests.delete')
    def test_delete_trigger_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        resp = self.client.delete_trigger("trigger1", self.namespace)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.delete')
    def test_delete_trigger_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.delete_trigger("trigger1", self.namespace)

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_list_rule_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        resp = self.client.list_rule(self.namespace)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_list_rule_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.list_rule(self.namespace)

    @patch('core.libs.clients.open_whisk_client.requests.put')
    def test_create_rule_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        data = {
            "name": "rule1",
            "status": "",
            "trigger": "/_/trigger1",
            "action": "/_/hello"
        }
        resp = self.client.create_trigger(self.namespace, data)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.put')
    def test_create_rule_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.create_rule(self.namespace, {})

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_retrieve_rule_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        resp = self.client.retrieve_rule("rule1", self.namespace)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.get')
    def test_retrieve_rule_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.retrieve_rule("rule1", self.namespace)

    @patch('core.libs.clients.open_whisk_client.requests.delete')
    def test_delete_rule_200(self, mock):
        mock_resp = self._mock_response(status_code=200)
        mock.return_value = mock_resp

        resp = self.client.delete_rule("rule1", self.namespace)
        self.assertEqual(resp.status_code, 200)

    @patch('core.libs.clients.open_whisk_client.requests.delete')
    def test_delete_rule_500(self, mock):
        mock_resp = self._mock_response(status_code=500)
        mock.return_value = mock_resp

        with self.assertRaises(OpenWhiskClientException):
            self.client.delete_rule("rule1", self.namespace)
