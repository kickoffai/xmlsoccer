from datetime import date
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

    def get_fixtures(self, *, league, season=''):
        """Get matches given a league and a season."""
        res = self._get(
                "GetFixturesByLeagueAndSeason",
                seasonDateString=season,
                league=league)
        return parse_fixtures(res)
        
    def get_fixture(self, *, fid):
        """Get match by ID."""
        res = self._get(
                "GetFixtureMatchByID",
                id=fid)
        return parse_fixtures(res)
        
    def get_fixtures_by_date_interval(self, *, league, start=None, end=None):
        """Get matches given a league and a start/end date interval in ISO format yyyy-mm-dd."""
        if not start:
            start = date.today().isoformat()
        if not end:
            end = date(date.today().year, 12, 31).isoformat()
        res = self._get(
                "GetFixturesByDateIntervalAndLeague",
                startDateString=start,
                endDateString=end,
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
