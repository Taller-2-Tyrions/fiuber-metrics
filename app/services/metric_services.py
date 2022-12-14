def find_users_metric(db) -> dict:
    return db["users"].find_one({}, {"_id": 0})


def find_payments_metric(db) -> dict:
    return db["payments"].find_one({}, {"_id": 0})


def find_voyages_metric(db) -> dict:
    return db["voyages"].find_one({}, {"_id": 0})
