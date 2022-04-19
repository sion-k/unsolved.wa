import request_manager
import parse_manager
import file_manager

user_dir = "data/usercache.json"

# returns dict
# users["ygonepiece"] = {
# 	solved_count: 1200,
#	active: True
# }
def get_users(organization_url: str) -> dict:
	old_users = file_manager.read_file(user_dir)
	users = {}
	index = 1
	while True:
		print("user page %d..." % index)
		rank_list_html = request_manager.get_html(organization_url % index)
		request_manager.overhead(1)
		if not rank_list_html:
			break
		new_users = parse_manager.parse_users(rank_list_html)
		for user_id in new_users:
			if user_id not in old_users or + \
				new_users[user_id]["solved_count"] != old_users[user_id]["solved_count"]:
				new_users[user_id]["active"] = True
			else:
				new_users[user_id]["active"] = False
		users.update(new_users)
		index += 1
	return users
