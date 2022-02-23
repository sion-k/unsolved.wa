import requests, re, time

attribute_regex = "href=\"/user/(\\w*)\">"
overhead_time = 1
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def parse_user(url):
	time.sleep(overhead_time)
	user_name = []
	response = requests.get(url, headers=headers)
	if response.status_code != 200:
		print("%s status_code : %d" % (url, response.status_code))
		return user_name

	attribute_pattern = re.compile(attribute_regex)
	user_matching = attribute_pattern.finditer(response.text)
	for m in user_matching:
		user_name.append(m.group(1))
	return user_name

def get_user(url):
	user_name = []
	index = 1
	while True:
		print("page %d..." % index)
		user = parse_user(url % index)
		if not user : break
		user_name += user
		index += 1
	return user_name

organization_url = "https://www.acmicpc.net/school/ranklist/385/%d"

user = get_user(organization_url)

file = open("user_name.txt", "w")
for u in user:
	file.write(u)
	file.write("\n")

file.close()
