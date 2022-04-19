import user_manager
import request_manager
import parse_manager
import file_manager

organization_url = "https://www.acmicpc.net/school/ranklist/385/%d"

# returns int list of solved by user
def get_solved_by_user(user_id: str) -> list:
    profile_url = "https://www.acmicpc.net/user/%s"
    profile_html = request_manager.get_html(profile_url % user_id)
    request_manager.overhead(3)
    if not profile_html : return []
    solved = parse_manager.parse_solved(profile_html)
    return solved

solved_dir = "data/solved.json"

# returns solved problem given organization
# for optimization, checks only active user
def get_solved(organization_url: str) -> list:
    solved = set(file_manager.read_file(solved_dir))
    users = user_manager.get_users(organization_url=organization_url)
    for user_id, user in users.items():
        if not user["active"]:
            continue
        solved.update(get_solved_by_user(user_id))
        print("%s : total %d problem" % (user_id, len(solved)))
    solved = sorted(list(solved))
    file_manager.write_file(solved_dir, solved)
    file_manager.write_file(user_manager.user_dir, users)
    return solved
 