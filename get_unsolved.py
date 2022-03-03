import http.client, json, time, requests
from bs4 import BeautifulSoup

file = open("solved.txt", "r")
solved = set()

while True:
    id = file.readline().rstrip()
    if not id : break
    solved.add(int(id))

overhead_time = 3

def get_problem(id):
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


def parse_last_problem(html):
    soup = BeautifulSoup(html, "html.parser")
    return int(soup.select("#problemset > tbody > tr:nth-child(1) > td.list_problem_id")[0].text)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
added_problem_url = "https://www.acmicpc.net/problem/added"

def get_last_problem():
    time.sleep(overhead_time)
    response = requests.get(added_problem_url, headers=headers)
    if response.status_code != 200:
        print("last_problem status_code : %d" % response.status_code)
        return 0
    last_problem = parse_last_problem(response.text)
    return last_problem

file = open("unsolved.json", "w", encoding="utf-8")
index = 1000
last_problem = get_last_problem()
while index <= last_problem:
    query_statement = []
    while len(query_statement) < 100:
        if not index in solved:
            query_statement.append(str(index))
        index += 1
    print("query %s to %s..." % (query_statement[0], query_statement[-1]))
    problem = get_problem(query_statement)
    for p in problem:
        file.write(json.dumps(p))
        file.write("\n")

file.close()
