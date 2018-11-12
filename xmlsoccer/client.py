import requests

from .parsers import *


class Client:

    def __init__(self, key, endpoint='http://www.xmlsoccer.com/FootballData.asmx'):
        self._key = key
        self._endpoint = endpoint

    def get_all_leagues(self):
        """Get all available leagues."""
        res = self._get("GetAllLeagues")
        return parse_leagues(res)
        
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

    def get_live_scores(self, *, league):
        """Get live scores given a league."""
        res = self._get(
                "GetLiveScoreByLeague",
                league=league)
        return parse_fixtures(res)

    def _get(self, method, **payload):
        payload["ApiKey"] = self._key
        url = "{}/{}".format(self._endpoint, method)
        res = requests.post(url, data=payload)
        return res.content
