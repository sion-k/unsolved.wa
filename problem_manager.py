import http.client, json, time, requests
import file_manager
import request_manager
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

def get_problems_by_tier(tier: int) -> list:
    query_url = "https://solved.ac/api/v3/search/problem"
    problems = []
    query = {
        "query": "tier:%d" % tier,
        "page": 1
    }
    while True:
        print("tier: %s, page: %s..." % (tier, query["page"]))
        problem = request_manager.solvedac_api(url=query_url, query_string=query)
        request_manager.overhead(3)
        if not problem:
            break
        problems += problem
        query["page"] += 1
    return problems

def get_problems_by_tier_range(start_tier: int, end_tier: int) -> list:
    problems = []
    for tier in range(start_tier, end_tier + 1):
        problems += get_problems_by_tier(tier)
    return problems

problem_dir = "data/problem.json"

# 전체 문제 목록 반환
level_range = 3 # 테스트용으로 범위를 작게 함
def get_problems():
    problems = get_problems_by_tier_range(1, 5)
    file_manager.write_file(problem_dir, problems)
    return problems
