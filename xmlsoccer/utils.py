from datetime import datetime

def parse_dt(s):
    return datetime.strptime(s.replace(":", ""), "%Y-%m-%dT%H%M%S%z")
