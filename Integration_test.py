import unittest
import json
from unittest.mock import patch
from flask import Flask
<<<<<<< HEAD
from app import app, initial_context  # Ensure your Flask app is correctly imported
=======
from app import app  # Ensure your Flask app is correctly imported
>>>>>>> 93e588febbaa72fcfd2eb866aec6e845dbe32598

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Setup test client for your Flask app
        self.app.testing = True

    @patch('app.getRecipe')  # Mock the getRecipe function which calls the Ollama API
    def test_integration_with_server(self, mock_getRecipe):
        # Define the mock return value of the Ollama API response
        mock_getRecipe.return_value = {
            'success': True,
<<<<<<< HEAD
            'ollama_reply': 'Here is a delicious recipe for chocolate cake.',
            'reply': 'Here is a delicious recipe for chocolate cake.'
=======
            'ollama_reply': 'Here is a delicious recipe for chocolate cake.'
>>>>>>> 93e588febbaa72fcfd2eb866aec6e845dbe32598
        }

        # URL of the Flask server endpoint
        url = '/process'  # Flask will handle the URL routing internally

        # Simulate sending a valid JSON payload to the server
        payload = {
            "ingredients": ["chocolate", "flour", "sugar"],
            "brand": "Generic"
        }

        # Send POST request
        response = self.app.post(url, json=payload)

        # Check the response status code (expected 200 OK)
        self.assertEqual(response.status_code, 200, "Expected 200 OK response status")

        # Parse the JSON response
        response_data = response.get_json()

        # Check that the response contains success and a valid reply
        self.assertTrue(response_data['success'], "Expected the success flag to be True")
        self.assertIn('ollama_reply', response_data, "Expected 'ollama_reply' in response data")

        # Verify the content of the response
        self.assertEqual(response_data['ollama_reply'], 'Here is a delicious recipe for chocolate cake.', "Expected response to match the mocked Ollama reply")

        # Ensure that the getRecipe function was called with the expected parameters
<<<<<<< HEAD
        mock_getRecipe.assert_called_once_with(initial_context, payload['ingredients'], payload['brand'])

if __name__ == '__main__':
    unittest.main()
=======
        mock_getRecipe.assert_called_once_with(app.initial_context, payload['ingredients'], payload['brand'])

if __name__ == '__main__':
    unittest.main()
#Everything passes for the integration test
# All functions work on their own
>>>>>>> 93e588febbaa72fcfd2eb866aec6e845dbe32598
