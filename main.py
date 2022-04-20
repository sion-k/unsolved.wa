import solved_manager
import data_manager
from functools import cmp_to_key

organization_url = "https://www.acmicpc.net/school/ranklist/385/%d"

if __name__ == "__main__":
    unsolved = solved_manager.get_unsolved(organization_url)
    unsolved = sorted(unsolved, key=cmp_to_key(data_manager.tier_cmp))
    unsolved = [u for u in unsolved if data_manager.is_solvable(u) and data_manager.is_rated(u)]
    data_manager.print_unsolved(unsolved)