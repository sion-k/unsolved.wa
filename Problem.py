import http.client, json, time, requests
import Unsolved
from bs4 import BeautifulSoup

overhead_time = 3

# 최대 길이 100의 id의 목록을 통해 구하는 방법
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
added_problem_url = "https://www.acmicpc.net/problem/added"

def get_last_problem():
    time.sleep(overhead_time)
    response = requests.get(added_problem_url, headers=headers)
    if response.status_code != 200:
        print("last_problem status_code : %d" % response.status_code)
        return 0
    def parse_last_problem(html):
        soup = BeautifulSoup(html, "html.parser")
        return int(soup.select("#problemset > tbody > tr:nth-child(1) > td.list_problem_id")[0].text)
    last_problem = parse_last_problem(response.text)
    return last_problem

def get_problem_by_id(id):
    time.sleep(overhead_time)
    query_statement = "%2C".join(id)
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", "/api/v3/problem/lookup?problemIds=%s" % query_statement, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    if data == "Not Found" or data == "[]" or not data:
        return []
    problems = json.loads(data)
    return problems

# 1~25 범위의 난이도를 정해서 구하는 방법
def get_problem_by_level(level):
    level = Unsolved.parse_level(level)
    page = 1
    problems = []
    while True:
        print("level: %s, page: %s..." % (level, page))
        time.sleep(overhead_time)
        conn = http.client.HTTPSConnection("solved.ac")
        headers = { 'Content-Type': "application/json" }
        query_statement = "tier%%3A%s&page=%s" % (level, page)
        conn.request("GET", "/api/v3/search/problem?query=%s" % query_statement, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        if data == "Not Found" or data == "[]" or not data:
            return []
        data = json.loads(data)
        if not data["items"]:
            break
        problems += data["items"]
        page += 1
    return problems

# 전체 문제 목록 반환
level_range = 3 # 테스트용으로 범위를 작게 함
def get_problem():
    problem = []
    for level in range(level_range, level_range + 2):
        problem += get_problem_by_level(level)
    write_problem(problem)
    return problem

def write_problem(problem):
    file = open("data/problem.json", "w")
    for p in problem:
        file.write(json.dumps(p))
        file.write("\n")
    file.close()
