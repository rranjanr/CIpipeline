import pytest
from app import app

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