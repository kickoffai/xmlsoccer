import requests

from .parsers import parse_odds, parse_fixtures


ENDPOINT = "http://www.xmlsoccer.com/FootballData.asmx"


class Client:

    def __init__(self, key):
        self._key = key

    def get_odds(self, *, fid):
        """Get all odds for a given fixture id."""
        res = self._get("GetAllOddsByFixtureMatchId", fixtureMatch_Id=fid)
        return parse_odds(res)

    def get_fixtures(self, *, league, season):
        """Get matches given a league and a season."""
        res = self._get(
                "GetFixturesByLeagueAndSeason",
                seasonDateString=season,
                league=league)
        return parse_fixtures(res)

    def _get(self, method, **payload):
        payload["ApiKey"] = self._key
        url = "{}/{}".format(ENDPOINT, method)
        res = requests.post(url, data=payload)
        return res.content
