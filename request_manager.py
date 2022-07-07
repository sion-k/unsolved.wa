import json
import random
import time
import requests

# returns user agent list
def get_user_agents() -> list:
    user_agents_dir = "data/user_agents.json"
    user_agents_file = open(user_agents_dir, "r")
    user_agents = json.loads(user_agents_file.read())
    return user_agents

# returns http request header
# randomly selects an user agent
def get_header() -> dict:
    user_agent = random.choice(get_user_agents())
    header = { "User-Agent": user_agent }
    return header

# pauses program for overhead_time
def overhead(overhead_time: int) -> None:
    time.sleep(overhead_time)

# returns html str
# returns empty string with failure request
def get_html(rank_list_url: str) -> str:
    headers = get_header()
    response = requests.get(rank_list_url, headers=headers)
    if response.status_code != 200:
        print("%s status_code : %d" % (rank_list_url, response.status_code))
        return ""
    html = response.text
    return html

# returns api response
# returns empty list if failed with connection
def solvedac_api(url: str, query_string: str) -> list:
    headers = { 'Content-Type': "application/json" }
    response = requests.request("GET", url, headers=headers, params=query_string)
    if response.status_code != 200:
        print("%s status_code : %d" % (url, response.status_code))
        return []
    data = response.json()
    return data["items"]
