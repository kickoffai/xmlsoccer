from lxml import etree
from . import utils


def parse_odds(text):
    root = etree.XML(text)
    data = list()
    for odds_elem in root[0]:
        datum = dict()
        for x in odds_elem:
            if x.tag == "FixtureMatch_Id":
                datum["fid"] = int(x.text)
            elif x.tag == "Bookmaker":
                datum["bookmaker"] = x.text
            elif x.tag == "UpdatedDate":
                datum["updated_at"] = utils.parse_dt(x.text)
            elif x.tag == "Type":
                datum["type"] = x.text
            elif x.tag == "HomeOdds":
                datum["home_odds"] = float(x.text)
            elif x.tag == "DrawOdds":
                datum["draw_odds"] = float(x.text)
            elif x.tag == "AwayOdds":
                datum["away_odds"] = float(x.text)
            elif x.tag == "Handicap":
                datum["handicap"] = float(x.text)
        if datum:
            data.append(datum)
    return data


def parse_fixtures(text):
    root = etree.XML(text)
    data = list()
    for match_elem in root:
        if match_elem.tag != "Match":
            continue
        datum = dict()
        for x in match_elem:
            if x.tag == "Id":
                datum["fid"] = int(x.text)
            elif x.tag == "Date":
                datum["datetime"] = utils.parse_dt(x.text)
            elif x.tag == "HomeTeam":
                datum["home_team"] = x.text
            elif x.tag == "HomeTeam_Id":
                datum["home_team_id"] = int(x.text)
            elif x.tag == "AwayTeam":
                datum["away_team"] = x.text
            elif x.tag == "AwayTeam_Id":
                datum["away_team_id"] = int(x.text)
            elif x.tag == "Time":
                datum["time"] = x.text
            elif x.tag == "HomeGoals":
                datum["home_goals"] = int(x.text)
            elif x.tag == "AwayGoals":
                datum["away_goals"] = int(x.text)
            elif x.tag == "Location":
                datum["location"] = x.text
        if datum:
            data.append(datum)
    return data


def parse_leagues(text):
    root = etree.XML(text)
    data = list()
    for odds_elem in root:
        datum = dict()
        for x in odds_elem:
            if x.tag == "Id":
                datum["id"] = int(x.text)
            elif x.tag == "Name":
                datum["name"] = x.text
            elif x.tag == "Country":
                datum["country"] = x.text
            elif x.tag == "Historical_Data":
                datum["historical_data"] = utils.parse_bool(x.text)
            elif x.tag == "Fixtures":
                datum["fixtures"] = utils.parse_bool(x.text)
            elif x.tag == "Livescore":
                datum["livescore"] = utils.parse_bool(x.text)
            elif x.tag == "NumberOfMatches":
                datum["number_of_matches"] = int(x.text)
            elif x.tag == "LatestMatch":
                datum["latest_match"] = utils.parse_dt(x.text)
            elif x.tag == "IsCup":
                datum["is_cup"] = utils.parse_bool(x.text)
        if datum:
            data.append(datum)
    return data