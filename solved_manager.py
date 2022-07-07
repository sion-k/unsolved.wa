import user_manager
import request_manager
import parse_manager
import data_manager
import problem_manager

# returns int list of solved by user
def get_solved_by_user(user_id: str) -> list:
    profile_url = "https://www.acmicpc.net/user/%s"
    profile_html = request_manager.get_html(profile_url % user_id)
    request_manager.overhead(3)
    if not profile_html : return []
    solved = parse_manager.parse_solved(profile_html)
    return solved


solved_dir = "data/solved.json"

# returns solved problem given organization number
# for optimization, checks only active user
def get_solved(organization_number: int) -> list:
    solved = set(data_manager.read_file(solved_dir)["solved"])
    users = user_manager.get_users(organization_number)
    for user_id, user in users.items():
        if not user["active"]:
            continue
        solved.update(get_solved_by_user(user_id))
        print("%s : total %d problem" % (user_id, len(solved)))
    solved = sorted(list(solved))
    data_manager.write_file(solved_dir, {"solved": solved})
    data_manager.write_file(user_manager.user_dir, users)
    return solved

unsolved_dir = "data/unsolved.json"

# returns unsolved problem given organization number
def get_unsolved(organization_number: int) -> list:
    solved = set(get_solved(organization_number))
    problems = problem_manager.get_problems()
    # filter unsolved
    def unsolved(problem):
        return not problem["problemId"] in solved
    unsolved = [problem for problem in problems if unsolved(problem)]
    data_manager.write_file(unsolved_dir, {"unsolved": unsolved})
    return unsolved
