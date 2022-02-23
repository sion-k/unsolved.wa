import requests, time
from bs4 import BeautifulSoup

user_name = []
file = open("user_name.txt", "r")

while True:
    user = file.readline().rstrip()
    if not user : break
    user_name.append(user)

file.close()

user_url = "https://www.acmicpc.net/user/%s"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
overhead_time = 1

def parse_problem(html, panel):
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("h3", string=panel)
    if not soup : return []
    soup = soup.parent.nextSibling
    problem = list(map(int, soup.text.split()))
    return problem

def get_solved(user):
    time.sleep(overhead_time)
    url = user_url % user
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("%s status_code : %d" % (user, response.status_code))
        return []
    solved = parse_problem(response.text, "맞은 문제")
    return solved

solved = set()
for user in user_name:
    print("total %d problem" % len(solved))
    print("%s solved..." % user)
    for problem in get_solved(user):
        solved.add(problem)

solved = sorted(solved)
file = open("solved.txt", "w")
for s in solved:
    file.write(str(s))
    file.write("\n")

file.close()
