import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        """Test if home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_content(self):
        """Test if home page contains expected content"""
        response = self.app.get('/')
        html_content = response.data.decode('utf-8')
        
        # Check for essential elements
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('<html lang="en">', html_content)
        self.assertIn('DevOps is So Much Fun to Learn!', html_content)

    def test_html_structure(self):
        """Test if HTML structure is complete and valid"""
        response = self.app.get('/')
        html_content = response.data.decode('utf-8')
        
        # Check for required HTML tags
        required_tags = [
            '<head>',
            '</head>',
            '<body>',
            '</body>',
            '</html>'
        ]
        
        for tag in required_tags:
            self.assertIn(tag, html_content, f"Missing HTML tag: {tag}")

if __name__ == '__main__':
    unittest.main() 