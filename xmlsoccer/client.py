import requests

from .models import League
from lxml import etree

# TODO
# fid: Fixture ID
# mid: Match ID
# tid: Team ID
# pid: Player ID


ENDPOINT = "http://www.xmlsoccer.com/FootballData.asmx"


class Client:

    def __init__(self, key):
        self._key = key

    def get_leagues(self):
        """Get all leagues"""
        res = self._get("GetAllLeagues")
        leagues = list()
        root = etree.fromstring(res)
        for elem in root.iter("League"):
            leagues.append(League(elem))
        return leagues

    def get_odds(self, fid):
        """Get all odds for a given fixture id"""
        res = self._get("GetAllOddsByFixtureMatchId", fixtureMatch_Id=fid)
        # TODO Process res...

    def get_teams(self, **kwargs):
        """
        Arguments: name, league, season.

        Valid combinations:

        - [no args]
        - league, season
        - name
        """
        if kwargs.keys() == set():
            res = self._get("GetAllTeams")
        elif kwargs.keys() == {"name"}:
            res = self._get("GetTeam", teamName=kwargs["name"])
        elif kwargs.keys() == {"league", "season"}:
            res = self._get(
                    "GetAllTeamsByLeagueAndSeason",
                    league=kwargs["league"],
                    seasonDateString=kwargs["season"])
        else:
            print(kwargs)
            raise ValueError()
        return res
        # TODO Process res...

    def get_fixtures(self, **kwargs):
        """
        Used mostly to get upcoming matches, even though it also returns data
        for matches in the past.

        Arguments: fid, begin, end, league, tid, seasons

        Valid combinations:

        - fid
        - begin, end
        - begin, end, league
        - begin, end, tid
        - league, season
        """
        if kwargs.keys() == {"fid"}:
            res = self._get("GetFixtureMatchByID", Id=kwargs["fid"])
        elif kwargs.keys() == {"begin", "end"}:
            res = self._get(
                    "GetFixturesByDateInterval",
                    startDateString=kwargs["begin"],
                    endDateString=kwargs["end"])
        elif kwargs.keys() == {"begin", "end", "league"}:
            res = self._get(
                    "GetFixturesByDateIntervalAndLeague",
                    startDateString=kwargs["begin"],
                    endDateString=kwargs["end"],
                    league=kwargs["league"])
        elif kwargs.keys() == {"begin", "end", "tid"}:
            res = self._get(
                    "GetFixturesByDateIntervalAndLeague",
                    startDateString=kwargs["begin"],
                    endDateString=kwargs["end"],
                    teamId=kwargs["tid"])
        elif kwargs.keys() == {"league", "season"}:
            res = self._get(
                    "GetFixturesByLeagueAndSeason",
                    seasonDateString=kwargs["season"],
                    league=kwargs["league"])
        else:
            raise ValueError()
        # TODO Process res...

    def get_matches(self, **kwargs):
        """
        Used to get historical data.

        Arguments: fid, mid, league, begin, end, season, tid, tid1, tid2

        Valid combinations:

        - fid
        - mid
        - league, begin, end
        - league, season
        - tid, begin, end
        - tid1, tid2, begin, end
        """
        if kwargs.keys() == {"fid"}:
            res = self._get(
                    "GetHistoricMatchesByFixtureMatchID", Id=kwargs["fid"])
        elif kwargs.keys() == {"mid"}:
            res = self._get(
                    "GetHistoricMatchesByID", Id=kwargs["mid"])
        elif kwargs.keys() == {"league", "begin", "end"}:
            res = self._get(
                    "GetHistoricMatchesByLeagueAndDateInterval",
                    startDateString=kwargs["begin"],
                    endDateString=kwargs["end"],
                    league=kwargs["league"])
        elif kwargs.keys() == {"league", "season"}:
            res = self._get(
                    "GetHistoricMatchesByLeagueAndSeason",
                    league=kwargs["league"],
                    seasonDateString=kwargs["season"])
        elif kwargs.keys() == {"tid", "begin", "end"}:
            res = self._get(
                    "GetHistoricMatchesByTeamAndDateInterval",
                    startDateString=kwargs["begin"],
                    endDateString=kwargs["end"],
                    teamId=kwargs["tid"])
        elif kwargs.keys() == {"tid1", "tid2", "begin", "end"}:
            res = self._get(
                    "GetHistoricMatchesByTeamsAndDateInterval",
                    startDateString=kwargs["begin"],
                    endDateString=kwargs["end"],
                    team1Id=kwargs["tid1"],
                    team2Id=kwargs["tid2"])
        else:
            raise ValueError()
        # TODO Process res...

    def get_live_scores(self, league=None):
        """
        Used to get current matches (rate limiting is less strict!).

        - [no args]
        - league
        """
        if league is not None:
            res = self._get("GetLiveScoreByLeague", league=league)
        else:
            res = self._get("GetLiveScore")
        # TODO Process res...

    def get_players(self, pid=None, tid=None):
        """
        - pid
        - tid
        """
        if pid is not None and tid is None:
            res = self._get("GetPlayerById", playerId=pid)
        elif tid is not None and pid is None:
            res = self._get("GetPlayersByTeam", teamId=tid)
        else:
            raise ValueError()

    def _get(self, method, **payload):
        payload["ApiKey"] = self._key
        url = "{}/{}".format(ENDPOINT, method)
        res = requests.post(url, data=payload)
        return res.content
