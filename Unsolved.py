import Problem, Solved
from functools import cmp_to_key

def get_unsolved():
    problems = Problem.get_problem()
    solved = set(Solved.get_solved())
    # filter unsolved
    def unsolved(problem):
        return not problem["problemId"] in solved
    unsolved = [problem for problem in problems if unsolved(problem)]
    unsolved = sort_unsolved(unsolved)
    write_unsolved(unsolved)
    return unsolved

# 1~25 범위의 난이도를 "B5", "S1"과 같은 형식의 String으로 변환
def parse_level(level):
    level -= 1
    rating = ["B", "S", "G", "P", "D", "R"]
    return "%s%d" % (rating[level // 5], 5 - level % 5)

# 읽기 쉬운 텍스트 형태로 풀지 않은 문제 저장
def write_unsolved(unsolved):
    file = open("data/unsolved.txt", "w", encoding="utf-8")
    for i in range(len(unsolved)):
        if unsolved[i]["level"] > 0 and unsolved[i]["isSolvable"]:
            line = "%s(id:%d, level:%s, solved:%d)\n" % (unsolved[i]["titleKo"], unsolved[i]["problemId"], parse_level(unsolved[i]["level"]), unsolved[i]["acceptedUserCount"])
            file.write(line)
    file.close()

def sort_unsolved(unsolved):
    return sorted(unsolved, key=cmp_to_key(level_cmp))

def level_cmp(u, v):
    if u["level"] == v["level"]:
        return v["acceptedUserCount"] - u["acceptedUserCount"]
    return u["level"] - v["level"]

def accept_cmp(u, v):
    if u["acceptedUserCount"] == v["acceptedUserCount"]:
        return u["level"] - v["level"]
    return v["acceptedUserCount"] - u["acceptedUserCount"]

if __name__ == "__main__":
    print(len(get_unsolved()))
