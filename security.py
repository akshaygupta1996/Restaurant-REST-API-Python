from werkzeug.security import safe_str_cmp
from models.users import UsersModel


# users = [
# 	User(1, 'akshay','akshay1234')
# ]

# username_mapping = {u.username: u for u in users}

# userid_mapping = {u.id: u for u in users}

def authenticate(username,password):
	# user = username_mapping.get(username,None)

		if len(username) == 10 and username.isdigit():
			user = UsersModel.find_by_phone(username)
		else:
			user = UsersModel.find_by_email(username)
		if user and safe_str_cmp(user.password , password):
			return user


def identity(payload):
	user_id = payload['identity']
	# return userid_mapping.get(user_id, None)
	return UserModel.find_by_id(user_id)