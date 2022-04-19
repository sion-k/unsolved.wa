import solved_manager
import data_manager

organization_url = "https://www.acmicpc.net/school/ranklist/385/%d"

if __name__ == "__main__":
    unsolved = solved_manager.get_unsolved(organization_url)
    unsolved = data_manager.sort_unsolved(unsolved)
    print(len(unsolved))
