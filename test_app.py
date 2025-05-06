import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Test if home page loads and contains required elements"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html_content = response.data.decode('utf-8')
        
        # Check essential elements
        required_elements = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '</head>',
            '<body>',
            '</body>',
            '</html>',
            'DevOps is So Much Fun to Learn!'
        ]
        
        for element in required_elements:
            self.assertIn(element, html_content, f"Missing element: {element}")

if __name__ == '__main__':
    unittest.main() 