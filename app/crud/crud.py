from fastapi.encoders import jsonable_encoder
from ..schemas.users_schema import UserEvent, UserBase

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

	match new_event:
		case "Signup":
			print("UserEvent SIGNUP")
			user_metric = db["users"].find_one()
			if not user_metric:
				print("User not exist!")
				db["users"].insert_one({"signup_federate":0,"signup_user_pass":0})
			else:
				print("User exist!")
				if new_user_metric["federate_id"] == "":
					new_count = user_metric["signup_federate"] + 1
					db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"signup_federate": new_count}})
				elif new_user_metric["email"] != "" and new_user_metric["password"] != "":
					new_count = user_metric["signup_user_pass"] + 1
					db["users"].update_one({"_id":user_metric["_id"]},{"$set":{"signup_user_pass": new_count}})

				#db["users"].find_one_and_update({"$set": user_metric})
		case UserEvent.LOGIN:
			print("UserEvent LOGIN")
		case UserEvent.BLOCK:
			print("UserEvent BLOCK")
		case UserEvent.RESET:
			print("UserEvent RESET")

	print("End insert_user_metric")