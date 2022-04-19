from bs4 import BeautifulSoup

# returns dict
# users["ygonepiece"] = { 
#   solved_count: 1200
# }
def parse_users(rank_list_html: str) -> dict:
    users = {}
    soup = BeautifulSoup(rank_list_html, "html.parser")
    rank_list = soup.select_one("table#ranklist").select_one("tbody")
    for tr in rank_list:
        tds = list(tr.select("a"))
        user_id = tds[0].text
        user = {
            "solved_count": int(tds[1].text) 
        }
        users[user_id] = user
    return users

# returns solved problem list
def parse_solved(profile_html: str) -> list:
    soup = BeautifulSoup(profile_html, "html.parser")
    soup = soup.find("h3", string="맞은 문제")
    if not soup : return []
    soup = soup.parent.nextSibling
    solved = list(map(int, soup.text.split()))
    return solved
