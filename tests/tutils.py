import hashlib
import os.path
import pytest
import requests


DATA_ROOT = os.path.join(os.path.dirname(__file__), "data")


class MockResponse():

    def __init__(self, content):
        self.content = content


def mock_post(url, data):
    d = make_digest(url, data)
    with open(os.path.join(DATA_ROOT, "{}.xml".format(d)), "rb") as f:
        return MockResponse(f.read())


@pytest.fixture
def patch_post(monkeypatch):
    # Prevent any external request.
    monkeypatch.delattr("requests.sessions.Session.request")
    # Patch the `post` method.
    monkeypatch.setattr(requests, "post", mock_post)


def make_digest(url, data):
    s = str(url)
    for key, val in sorted(data.items()):
        if key == "ApiKey":
            continue
        s += str(key) + str(val)
    return hashlib.md5(s.encode()).hexdigest()[:16]


def download(url, data):
    res = requests.post(url, data=data)
    d = make_digest(url, data)
    with open(os.path.join(DATA_ROOT, "{}.xml".format(d)), "wb") as f:
        f.write(res.content)
