import requests, time, User, json, os
import random
from bs4 import BeautifulSoup

user_url = "https://www.acmicpc.net/user/%s"

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

overhead_time = 3

def parse_problem(html, panel):
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("h3", string=panel)
    if not soup : return []
    soup = soup.parent.nextSibling
    problem = list(map(int, soup.text.split()))
    return problem

def get_solved_by_user(user):
    time.sleep(overhead_time)
    url = user_url % user
    headers = {"User-Agent": random.choice(user_agent_list)}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("%s status_code : %d" % (user, response.status_code))
        return []
    solved = parse_problem(response.text, "맞은 문제")
    return solved

# get_user()로 얻은 유저들이 푼 문제로 solved.json 갱신하고 반환
def get_solved():
    solved = set(read_solved())
    users = User.get_user()
    for user in users:
        solved.update(get_solved_by_user(user))
        print("%s : total %d problem" % (user, len(solved)))
    solved = sorted(list(solved))
    write_solved(solved)
    # _usercache를 usercache로 변경
    if os.path.exists("data/usercache.json") and os.path.exists("data/_usercache.json"):
        os.remove("data/usercache.json")
        os.rename("data/_usercache.json", "data/usercache.json")
    return solved

def read_solved():
    file = open("data/solved.json", "r")
    solved = json.loads(file.read())
    file.close()
    return solved

def write_solved(solved):
    file = open("data/solved.json", "w")
    file.write(json.dumps(solved))
    file.close()
