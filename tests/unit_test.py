import unittest
from unittest.mock import patch
from app import app  # Ensure your Flask app is correctly imported

class FlaskServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.getRecipe')
    def test_post_request_success(self, mock_getRecipe):
        mock_getRecipe.return_value = {'success': True, 'reply': 'Sample Reply'}
        response = self.app.post('/process', json={'ingredients': ['tomato'], 'brand': 'Heinz'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sample Reply', response.data)

    def test_post_request_malformed_json(self):
        response = self.app.post('/process', data='{"brand": "Heinz", "ingredients": ["tomato"', content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Expecting a 400 Bad Request
        self.assertIn(b'Malformed JSON', response.data)

    @patch('app.getRecipe')
    def test_ollama_invalid_response(self, mock_getRecipe):
        # Simulate invalid response from Ollama
        mock_getRecipe.return_value = {'success': False, 'ollama_reply': 'Invalid data'}
        response = self.app.post('/process', json={'brand': 'Heinz', 'ingredients': ['tomato']})
        self.assertEqual(response.status_code, 500)  # Internal Server Error
        self.assertIn(b'Invalid data', response.data)  # Ensure invalid data is detected

    @patch('app.getRecipe')
    def test_ollama_connection_failure(self, mock_getRecipe):
        # Simulate a connection error from Ollama API
        mock_getRecipe.side_effect = Exception('Failed to connect to Ollama API')
        response = self.app.post('/process', json={'brand': 'Heinz', 'ingredients': ['tomato']})
        self.assertEqual(response.status_code, 500)  # Internal Server Error
        self.assertIn(b'Failed to connect to Ollama API', response.data)


if __name__ == '__main__':
    unittest.main()



































'''import unittest
from unittest.mock import patch
from app import app  # Adjust the import if your app file is named differently

class FlaskServiceTest(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.getRecipe')  # Mock the getRecipe function
    def test_post_request(self, mock_getRecipe):
        # Define what the mock should return
        mock_getRecipe.return_value = {'success': True, 'reply': 'Sample Reply'}

        # Make a POST request to the /process route
        response = self.app.post('/process', json={'ingredients': ['tomato'], 'brand': 'Heinz'})

        # Check that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sample Reply', response.data)  # Check if 'Sample Reply' is in the response data

    # Add more test methods as needed...

if __name__ == '__main__':
    unittest.main()'''
>>>>>>> 93e588febbaa72fcfd2eb866aec6e845dbe32598
