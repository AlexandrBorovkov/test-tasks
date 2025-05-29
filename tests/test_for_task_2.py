import pytest
import requests

from tasks.task2.task2 import RUSSIAN_ORDER, parsing_wikipedia


HTML = """
    <div class="mw-category-group">
        <h3>А</h3>
        <ul>
            <li><a href="/wiki/Аист" title="Аист">Аист</a></li>
            <li><a href="/wiki/Акула" title="Акула">Акула</a></li>
        </ul>
        <h3>Б</h3>
        <ul>
            <li><a href="/wiki/Барсук" title="Барсук">Барсук</a></li>
        </ul>
    </div>
"""

@pytest.fixture
def mock_requests(monkeypatch):
    class MockResponse:
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code
            self.encoding = "utf-8"

        def raise_for_status(self):
            if self.status_code != 200:
                raise requests.exceptions.RequestException("Error")

    def mock_get(*args, **kwargs):
        return MockResponse(HTML)

    monkeypatch.setattr("requests.get", mock_get)

def test(mock_requests):
    result = parsing_wikipedia()
    assert isinstance(result, list)
    assert result.count("А") == 2
    assert result.count("Б") == 1
    assert all(char in RUSSIAN_ORDER for char in result)
