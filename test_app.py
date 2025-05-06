import pytest
from app import app
import sys

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if home page loads and contains required elements"""
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

if __name__ == '__main__':
    # Run pytest with proper exit
    sys.exit(pytest.main([__file__, '-v', '--junitxml=test-results/junit.xml'])) 