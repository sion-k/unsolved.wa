import json
import os

# write temp data file at given dir
def write_file(dir: str, data: dict) -> None:
    file = open(dir, "w")
    file.write(json.dumps(data))
    file.close()

# returns json
def read_file(dir: str) -> dict:
    if not os.path.exists(dir):
        file = open(dir, "w")
        file.write("{}\n")
        file.close()
    file = open(dir, "r")
    data = json.loads(file.read())
    file.close()
    return data

# returns format string
# ex) 1 -> B5, 2 -> B4, ... 30 -> R1
def parse_level(tier: int) -> str:
    tier -= 1
    rating = ["B", "S", "G", "P", "D", "R"]
    return "%s%d" % (rating[tier // 5], 5 - tier % 5)

def tier_cmp(u, v):
    if u["level"] == v["level"]:
        return v["acceptedUserCount"] - u["acceptedUserCount"]
    return u["level"] - v["level"]

def accept_cmp(u, v):
    if u["acceptedUserCount"] == v["acceptedUserCount"]:
        return u["level"] - v["level"]
    return v["acceptedUserCount"] - u["acceptedUserCount"]

def is_rated(problem: dict) -> bool:
    return problem["level"] > 0

def is_solvable(problem: dict) -> bool:
    return problem["isSolvable"]

def is_korean(problem: dict) -> bool:
    return problem["titles"][0]["language"] and problem["titles"][0]["language"] == "ko"

def print_unsolved(unsolved: list) -> None:
    file = open("data/unsolved.txt", "w", encoding="utf-8")
    for i in range(len(unsolved)):
        line = "%s(id:%d, level:%s, solved:%d)\n" % (unsolved[i]["titleKo"], unsolved[i]["problemId"], parse_level(unsolved[i]["level"]), unsolved[i]["acceptedUserCount"])
        file.write(line)
    file.close()
