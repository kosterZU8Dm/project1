import requests

def test_home_page(client):
    url = "http://localhost:8000"
    response = requests.get(url)
    assert response.status_code == 200
    assert "Project1" in response.text
    assert '<span class="site-title">Project1</span>' in response.text
    assert '&copy; 2023 Project1' in response.text
