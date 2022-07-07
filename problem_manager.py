import data_manager
import request_manager

# returns json type problem list
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

# returns json type problem list
# start_tier and end_tier are both inclusive range
def get_problems_by_tier_range(start_tier: int, end_tier: int) -> list:
    problems = []
    for tier in range(start_tier, end_tier + 1):
        problems += get_problems_by_tier(tier)
    return problems

problem_dir = "data/problem.json"
tier_range = 12 # 25

# returns json type problem list
def get_problems() -> list:
    problems = get_problems_by_tier_range(1, tier_range)
    data_manager.write_file(problem_dir, {"problems": problems})
    return problems
