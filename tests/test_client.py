import pytest
import datetime

from tutils import patch_post
from xmlsoccer import Client


@pytest.fixture
def client(patch_post):
    return Client(key="DUMMY")


def test_get_odds(client):
    res = client.get_odds(fid=386834)
    assert len(res) == 238
    assert res[32] == {
        "fid": 386834,
        "bookmaker": "Betrally",
        "updated_at": datetime.datetime(2018, 5, 30, 7, 18, 36, 400000),
        "type": "Over/Under",
        "home_odds": 23.75,
        "away_odds": 1.0,
        "handicap": 6.5,
    }


def test_get_odds_empty(client):
    res = client.get_odds(fid=387436)
    assert len(res) == 0


def test_get_fixtures(client):
    res = client.get_fixtures(league="Major League Soccer", season="1819")
    assert len(res) == 397
    assert res[47] == {
        "fid": 387298,
        "datetime": datetime.datetime(2018, 4, 7, 21, 0, tzinfo=datetime.timezone.utc),
        "home_team": "Atlanta United",
        "home_team_id": 4780,
        "away_team": "Los Angeles FC",
        "away_team_id": 4846,
        "time": "Finished",
        "home_goals": 5,
        "away_goals": 0,
        "location": "Bobby Dodd Stadium"
    }
