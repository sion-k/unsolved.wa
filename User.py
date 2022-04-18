import requests, time, random, json, os
from bs4 import BeautifulSoup

overhead_time = 1

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

# url을 통해 html을 얻고 그 안에서 userId, solvedCount를 추출
# dict[userId] = solvedCount 형식의 dict로 반환
def parse_user(url):
	time.sleep(overhead_time)
	users = {}
	headers = {"User-Agent": random.choice(user_agent_list)}
	response = requests.get(url, headers=headers)
	# 존재하지 않는 페이지일때도 빈 리스트 반환
	if response.status_code != 200:
		print("%s status_code : %d" % (url, response.status_code))
		return users
	html = response.content
	soup = BeautifulSoup(html, "html.parser")
	ranklist = soup.select_one("table#ranklist").select_one("tbody")
	for tr in ranklist:
		tds = list(tr.select("a"))
		users[tds[0].text] = int(tds[1].text)
	return users

def get_user_by_organization(url):
	active_user = []
	oldCache = read_user()
	newCache = {}
	index = 1
	while True:
		print("user page %d..." % index)
		user = parse_user(url % index)
		# 유저가 존재하지 않는 페이지면 종료
		if not user : break
		for u in user:
			newCache[u] = user[u]
			if u not in oldCache or user[u] != oldCache[u]:
				active_user.append(u)
		index += 1
	write_user(newCache)
	return active_user

# 활성화된 유저의 아이디 리스트 반환
def get_user():
	organization_url = "https://www.acmicpc.net/school/ranklist/385/%d"
	user = get_user_by_organization(organization_url)
	return user

# cache를 읽는다
# TODO exception check for file existence
def read_user():
	if not os.path.exists("data/usercache.json"):
		file = open("data/usercache.json", "w")
		file.write("{}\n")
		file.close()
	file = open("data/usercache.json", "r")
	user = json.loads(file.read())
	file.close()
	return user

# dict[userId] = solvedCount 형식의 dict를 json형태로 저장
# 프로그램이 완전히 끝나기 전까지는 _usercache에 임시로 저장
def write_user(user):
	file = open("data/_usercache.json", "w")
	file.write(json.dumps(user))
	file.close()