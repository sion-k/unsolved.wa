import solved_manager
import data_manager
from functools import cmp_to_key

organization_number = 385 # CNU

if __name__ == "__main__":
    unsolved = solved_manager.get_unsolved(organization_number)
    unsolved = sorted(unsolved, key=cmp_to_key(data_manager.tier_cmp))
    unsolved = [u for u in unsolved if data_manager.is_solvable(u) and data_manager.is_rated(u)]
    data_manager.print_unsolved(unsolved)