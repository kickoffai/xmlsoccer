from . import utils

class League:

    def __init__(self, elem):
        self._parse(elem)

    def _parse(self, elem):
        for x in elem:
            print(x.tag)
            if x.tag == "Id":
                self.lid = int(x.text)
            elif x.tag == "Name":
                self.name = x.text
            elif x.tag == "Country":
                self.country = x.text
            elif x.tag == "Historical_Data":
                self.has_historical_data = (x.text == "true")
            elif x.tag == "Fixtures":
                self.has_fixtures = (x.text == "true")
            elif x.tag == "Livescore":
                self.has_live_score = (x.text == "true")
            elif x.tag == "NumberOfMatches":
                self.n_matches = int(x.text)
            elif x.tag == "LatestMatch":
                self.latest_match = utils.parse_dt(x.text)
            elif x.tag == "IsCup":
                self.is_cup = (x.text == "true")
            else:
                raise RuntimeError("unknown tag: {}".format(x.tag))
