from datetime import datetime

def parse_dt(s):
    try:
        return datetime.strptime(s.replace(":", ""), "%Y-%m-%dT%H%M%S%z")
    except ValueError:
        return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
