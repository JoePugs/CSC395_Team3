


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

    @patch('app.getRecipe')
    def test_post_request_missing_ingredients(self, mock_getRecipe):
        mock_getRecipe.return_value = {'success': False, 'error': 'Missing ingredients'}
        response = self.app.post('/process', json={'brand': 'Heinz'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Missing ingredients', response.data)

    @patch('app.getRecipe')
    def test_post_request_missing_brand(self, mock_getRecipe):
        mock_getRecipe.return_value = {'success': False, 'error': 'Missing brand'}
        response = self.app.post('/process', json={'ingredients': ['tomato']})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Missing brand', response.data)

    def test_post_request_invalid_json(self):
        response = self.app.post('/process', data='invalid json')
        self.assertEqual(response.status_code, 400)  # Adjust based on your error handling

    @patch('app.getRecipe')
    def test_post_request_server_error(self, mock_getRecipe):
        mock_getRecipe.side_effect = Exception("Server Error")
        response = self.app.post('/process', json={'ingredients': ['tomato'], 'brand': 'Heinz'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Server Error', response.data)

    @patch('app.getRecipe')
    def test_post_request_empty_ingredients_and_brand(self, mock_getRecipe):
        mock_getRecipe.return_value = {'success': False, 'error': 'No ingredients or brand provided'}
        response = self.app.post('/process', json={})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'No ingredients or brand provided', response.data)

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
