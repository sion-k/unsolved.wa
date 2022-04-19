import json
import os

# write temp data file at given dir
def write_file(dir: str, data) -> None:
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
