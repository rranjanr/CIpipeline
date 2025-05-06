import pytest
from app import app
from html.parser import HTMLParser

class HTMLValidationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
    
    def handle_endtag(self, tag):
        if not self.tags:
            self.errors.append(f"Found closing tag '{tag}' without matching opening tag")
            return
        if self.tags[-1] != tag:
            self.errors.append(f"Expected closing tag for '{self.tags[-1]}' but found '{tag}'")
        else:
            self.tags.pop()
    
    def validate(self):
        if self.tags:
            self.errors.append(f"Unclosed tags: {', '.join(reversed(self.tags))}")
        return len(self.errors) == 0, self.errors

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    return app.test_client()

def test_home_page(client):
    """Test if home page loads and contains required elements"""
    with app.app_context():
        response = client.get('/')
        assert response.status_code == 200
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
            assert element in html_content, f"Missing element: {element}"
        
        # Validate HTML structure
        parser = HTMLValidationParser()
        parser.feed(html_content)
        is_valid, errors = parser.validate()
        assert is_valid, f"HTML validation errors: {errors}" 