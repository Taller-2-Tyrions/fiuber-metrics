from fastapi.encoders import jsonable_encoder
from ..schemas.users_schema import UserEvent

import json

def find_user_metric(db) -> dict:
	return db["users"]

def insert_user_metric(db, new_user_metric):
	new_user_metric_je = jsonable_encoder(new_user_metric)
	
	my_json = new_user_metric.decode('utf8').replace("'", '"')
	print("insert_user_metric: "+ str(new_user_metric_je))
	new_user_metric = json.loads(my_json)

	new_event = new_user_metric.get("event")
	print("event: {event}".format(event=new_event))

	empty_metric = { "signup_federate_evt": 0, "signup_pass_evt": 0, "login_federate_evt": 0, "login_pass_evt": 0, "block_evt": 0, "reset_evt": 0 }
	user_metric = db["users"].find_one()
	if not user_metric:
		print("User not exist! Insert empty_metric")
		db["users"].insert_one(empty_metric)
		user_metric = db["users"].find_one()
	match new_event:
		case "Signup":
			print("UserEvent Signup, insert new value")
			
			if new_user_metric["is_federate"] == "true":
				new_count = user_metric["signup_federate_evt"] + 1
				db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"signup_federate_evt": new_count}})
			else:
				new_count = user_metric["signup_pass_evt"] + 1
				db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"signup_pass_evt": new_count}})

		case "Login":
			print("UserEvent Login, insert new value")
			if new_user_metric["is_federate"] == "true":
				new_count = user_metric["login_federate_evt"] + 1
				db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"login_federate_evt": new_count}})
			else:
				new_count = user_metric["login_pass_evt"] + 1
				db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"login_pass_evt": new_count}})
			
		case "Block":
			print("UserEvent Block, insert new value")

			new_count = user_metric["block_evt"] + 1
			db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"block_evt": new_count}})

		case "Reset":
			print("UserEvent Reset, insert new value")

			new_count = user_metric["reset_evt"] + 1
			db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"reset_evt": new_count}})

	print("End insert_user_metric")

