import json
from functools import cmp_to_key

file = open("unsolved.json", "r", encoding="utf-8")

unsolved = []
while True:
    problem = file.readline().rstrip()
    if not problem : break
    unsolved.append(json.loads(problem))

file.close()

def level_cmp(u, v):
    if u["level"] == v["level"]:
        return v["acceptedUserCount"] - u["acceptedUserCount"]
    return u["level"] - v["level"]

unsolved = sorted(unsolved, key=cmp_to_key(level_cmp))

def parse_level(level):
    level -= 1
    rating = ["B", "S", "G", "P", "D", "R"]
    return "%s%d" % (rating[level // 5], 5 - level % 5)

file = open("unsolved.txt", "w", encoding="utf-8")
for i in range(len(unsolved)):
    if unsolved[i]["level"] > 0 and unsolved[i]["isSolvable"]:
        line = "%s(id:%d, level:%s, solved:%d)\n" % (unsolved[i]["titleKo"], unsolved[i]["problemId"], parse_level(unsolved[i]["level"]), unsolved[i]["acceptedUserCount"])
        file.write(line)

file.close()