from fastapi.encoders import jsonable_encoder
import json
from datetime import datetime


def insert_users_metric_empty(db):
    empty_metric = {"signup_federate_evt": 0, "signup_pass_evt": 0,
                    "login_federate_evt": 0, "login_pass_evt": 0,
                    "block_evt": 0, "reset_evt": 0}
    user_metric = db["users"].find_one()
    if not user_metric:
        print("Users Collection not exist! Insert empty Collection")
        db["users"].insert_one(empty_metric)


def insert_voyages_metric_empty(db):
    empty_metric = {"voyages": 0, "average_duration": 0.0,
                    "vip_voyages": 0, "no_vip_voyages": 0}
    user_metric = db["voyages"].find_one()
    if not user_metric:
        print("Voyages Collection not exist! Insert empty Collection")
        db["voyages"].insert_one(empty_metric)


def insert_payments_metric_empty(db):
    empty_metric = {"payments_success": 0, "payments_fail": 0,
                    "average_price": 0.0}
    user_metric = db["payments"].find_one()
    if not user_metric:
        print("Payments Collection not exist! Insert empty Collection")
        db["payments"].insert_one(empty_metric)


def insert_metric(db, new_user_metric):
    new_user_metric_je = jsonable_encoder(new_user_metric)
    my_json = new_user_metric.decode('utf8').replace("'", '"')
    print("insert_metric: " + str(new_user_metric_je))
    new_user_metric = json.loads(my_json)

    new_event = new_user_metric.get("event")
    print("event: {event}".format(event=new_event))

    match new_event:
        case "Signup":
            print("UserEvent Signup, insert new value")

            user_metric = db["users"].find_one()
            if new_user_metric["is_federate"] == "true":
                new_count = user_metric["signup_federate_evt"] + 1
                db["users"].update_one({"_id": user_metric["_id"]},
                                       {"$set": {
                                        "signup_federate_evt": new_count}})
            else:
                new_count = user_metric["signup_pass_evt"] + 1
                db["users"].update_one({"_id": user_metric["_id"]},
                                       {"$set":
                                       {"signup_pass_evt": new_count}})

        case "Login":
            user_metric = db["users"].find_one()
            print("UserEvent Login, insert new value")
            if new_user_metric["is_federate"] == "true":
                new_count = user_metric["login_federate_evt"] + 1
                db["users"].update_one({"_id": user_metric["_id"]},
                                       {"$set":
                                       {"login_federate_evt": new_count}})
            else:
                new_count = user_metric["login_pass_evt"] + 1
                db["users"].update_one({"_id": user_metric["_id"]},
                                       {"$set":
                                       {"login_pass_evt": new_count}})

        case "Block":
            user_metric = db["users"].find_one()
            print("UserEvent Block, insert new value")

            new_count = user_metric["block_evt"] + 1
            db["users"].update_one({"_id": user_metric["_id"]},
                                   {"$set":
                                   {"block_evt": new_count}})
        case "Unblock":
            user_metric = db["users"].find_one()
            print("UserEvent Unblock, insert new value")

            block_evt = user_metric["block_evt"]
            if block_evt == 0:
                return
            new_count = block_evt - 1
            db["users"].update_one({"_id": user_metric["_id"]},
                                   {"$set":
                                   {"block_evt": new_count}})

        case "Reset":
            user_metric = db["users"].find_one()
            print("UserEvent Reset, insert new value")

            new_count = user_metric["reset_evt"] + 1

            db["users"].update_one({"_id": user_metric["_id"]},
                                   {"$set":
                                   {"reset_evt": new_count}})

        case "Voyage":
            print("UserEvent Voyage, insert new value")

            user_metric = db["voyages"].find_one()
            voyages = user_metric["voyages"] + 1

            f1 = user_metric["voyages"]/voyages
            start = datetime.fromisoformat(new_user_metric["start_time"])
            end = datetime.fromisoformat(new_user_metric["end_time"])
            duration = (end-start).total_seconds()
            f2 = duration / voyages
            average_duration = (user_metric["average_duration"] * f1) + f2

            vip_voyages = user_metric["vip_voyages"]
            no_vip_voyages = user_metric["no_vip_voyages"]
            if new_user_metric["is_vip"] == "true":
                vip_voyages = vip_voyages + 1
            else:
                no_vip_voyages = user_metric["no_vip_voyages"] + 1

            db["voyages"].update_one({"_id": user_metric["_id"]},
                                     {"$set": {
                                      "voyages": voyages,
                                      "average_duration": average_duration,
                                      "vip_voyages": vip_voyages,
                                      "no_vip_voyages": no_vip_voyages}})

        case "Payment":
            print("UserEvent Payment, insert new value")

            user_metric = db["payments"].find_one()
            payments_success = user_metric["payments_success"]
            payments_fail = user_metric["payments_fail"]

            average_price = user_metric["average_price"]

            if new_user_metric["status"] == "true":
                payments_success = payments_success + 1
                f1 = user_metric["payments_success"]/payments_success
                f2 = (float(new_user_metric["price"]) / payments_success)
                average_price = (user_metric["average_price"] * f1) + f2
            else:
                payments_fail = payments_fail + 1

            db["payments"].update_one(
                {"_id": user_metric["_id"]},
                {"$set": {
                    "payments_success": payments_success,
                    "payments_fail": payments_fail,
                    "average_price": average_price
                    }})
        case _:
            print("UserEvent is not register")
    print("End insert_metric")
