import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import app  # Assuming your Flask app is in a file named my_flask_app.py

class FlaskServiceTest(unittest.TestCase):
    
    @patch('app.submit')  # Mock the submit function (endpoint handler)
    def test_post_request(self, mock_submit):
        # Initialize test client from Flask app
        with app.test_client() as client:
            # Set up mock response data
            mock_response = {'status': 'success', 'data': {'key': 'value'}}
            mock_submit.return_value = MagicMock(status_code=201, json=mock_response)

            # Simulate a POST request
            response = client.post('/submit', 
                                   data=json.dumps({'key': 'value'}), 
                                   content_type='application/json')
            
            # Check that the POST request was successful
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, mock_response)

            # Assert that the mock_submit function was called correctly
            mock_submit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
