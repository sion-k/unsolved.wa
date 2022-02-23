import http.client, json, time

file = open("solved.txt", "r")
solved = set()

while True:
    id = file.readline().rstrip()
    if not id : break
    solved.add(int(id))

overhead_time = 3

def get_problem(id):
    time.sleep(overhead_time)
    query_statement = "%2C".join(id)
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", "/api/v3/problem/lookup?problemIds=%s" % query_statement, headers=headers)
    res = conn.getresponse()
    data = res.read()
    if data.decode("utf-8") == "Not Found":
        return
    problems = json.loads(data.decode("utf-8"))
    return problems

file = open("unsolved.json", "w", encoding="utf-8")

index = 1000
while True:
    query_statement = []
    while len(query_statement) < 100:
        if not index in solved:
            query_statement.append(str(index))
        index += 1
    print("query %s to %s..." % (query_statement[0], query_statement[-1]))
    problem = get_problem(query_statement)
    if not problem : break
    for p in problem:
        file.write(json.dumps(p))
        file.write("\n")

file.close()
