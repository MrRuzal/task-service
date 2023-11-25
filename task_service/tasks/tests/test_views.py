from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch


class TaskViewSetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('tasks.views.process_task.delay')
    def test_create_task(self, mock_process_task):
        client = APIClient()
        data = {'number': 123, 'status': 'created'}
        response = client.post('/api/tasks/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
