from rest_framework.test import APITestCase
from django.urls import reverse


class DocsSimpleTest(APITestCase):

    def test_docs_endpoint_runs_without_errors(self):
        response = self.client.get(
            path=reverse('docs'),
        )
        self.assertEqual(response.status_code, 200)
