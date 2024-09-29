import unittest
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
    unittest.main()
