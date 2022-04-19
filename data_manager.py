import json
import os
from functools import cmp_to_key

# write temp data file at given dir
def write_file(dir: str, data: dict) -> None:
    file = open(dir, "w")
    file.write(json.dumps(data))
    file.close()

# returns json
def read_file(dir: str):
    if not os.path.exists(dir):
        file = open(dir, "w")
        file.write("{}\n")
        file.close()
    file = open(dir, "r")
    data = json.loads(file.read())
    file.close()
    return data

# 1~25 범위의 난이도를 "B5", "S1"과 같은 형식의 String으로 변환
def parse_level(tier):
    tier -= 1
    rating = ["B", "S", "G", "P", "D", "R"]
    return "%s%d" % (rating[tier // 5], 5 - tier % 5)

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

# 읽기 쉬운 텍스트 형태로 풀지 않은 문제 저장
def write_unsolved(unsolved):
    file = open("data/unsolved.txt", "w", encoding="utf-8")
    for i in range(len(unsolved)):
        if unsolved[i]["level"] > 0 and unsolved[i]["isSolvable"] and unsolved[i]["titles"][0]["language"] and unsolved[i]["titles"][0]["language"] == "ko":
            line = "%s(id:%d, level:%s, solved:%d)\n" % (unsolved[i]["titleKo"], unsolved[i]["problemId"], parse_level(unsolved[i]["level"]), unsolved[i]["acceptedUserCount"])
            file.write(line)
    file.close()
