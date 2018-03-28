import pytest

from tutils import patch_post
from xmlsoccer import Client


@pytest.fixture
def client(patch_post):
    return Client(key="DUMMY")


def test_get_leagues(client):
    res = client.get_leagues()
    assert len(res) > 0


def test_get_teams(client):
    res = client.get_teams()
    assert len(res) > 0
    res = client.get_teams(league="Serie B", season="1617")
    assert len(res) > 0
    res = client.get_teams(name="Wisla Krakow")
    assert len(res) > 0
    with pytest.raises(ValueError):
        client.get_teams(league="Serie B")
