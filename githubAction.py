import os
from dotenv import load_dotenv
import aurionAPI
from datetime import datetime, date, timezone
import calendar

def make_token():
    # load_dotenv()
    username = os.getenv("REMOTE_USERNAME")
    password = os.getenv("REMOTE_PASSWORD")

    if not username or not password:
        raise ValueError("Missing remote credentials in environment variables.")

    token = aurionAPI.get_token(username, password)
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"REMOTE_TOKEN={token}\n")
    return token 

def get_next_date(now: str):
    dt = datetime.strptime(now, "%Y-%m-%d").date()
    month = dt.month + 1
    year = dt.year + (month // 12)
    month = (month % 12) + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return date(year, month, day).strftime("%Y-%m-%d")

if __name__ == "__main__":
    token = os.getenv("REMOTE_TOKEN", "")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if now == "":
        raise ValueError("current date NOW is empty")
    end = get_next_date(now)
    planning = None

    #first try to fetch with known token
    if token != "":
        planning = aurionAPI.get_planning(token, now, end)

    # second try if invalid token, first try if no token
    if planning == None or len(planning) < 1:
        token = make_token()
        print("::warning::A token has been recreated")
        planning = aurionAPI.get_planning(token, now, end)
    
    ics = aurionAPI.generate_ics(planning)
    with open("dist/calendar.ics", "w", encoding="utf-8") as f:
        f.write(str(ics))