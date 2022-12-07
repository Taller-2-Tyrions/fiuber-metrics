import mongomock
from app.crud import crud


def test_insert_users_metric_empty():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()

    assert (metric["signup_federate_evt"] == 0)
    assert (metric["signup_pass_evt"] == 0)
    assert (metric["login_federate_evt"] == 0)
    assert (metric["login_pass_evt"] == 0)
    assert (metric["block_evt"] == 0)
    assert (metric["reset_evt"] == 0)


def test_insert_voyages_metric_empty():
    db = mongomock.MongoClient().db
    crud.insert_voyages_metric_empty(db)

    metric = db["voyages"].find_one()

    assert (metric["voyages"] == 0)
    assert (metric["average_duration"] == 0)
    assert (metric["vip_voyages"] == 0)
    assert (metric["no_vip_voyages"] == 0)


def test_insert_payments_metric_empty():
    db = mongomock.MongoClient().db
    crud.insert_payments_metric_empty(db)

    metric = db["payments"].find_one()

    assert (metric["payments_success"] == 0)
    assert (metric["payments_fail"] == 0)
    assert (metric["average_price"] == 0)


def test_insert_new_metric_signup_federate():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()

    assert(metric["signup_federate_evt"] == 0)
    assert(metric["signup_pass_evt"] == 0)

    new_user_metric = bytes('{"event":"Signup","is_federate":"true"}', 'utf-8')
    crud.insert_metric(db, new_user_metric)

    metric = db["users"].find_one()

    assert (metric["signup_federate_evt"] == 1)
    assert (metric["signup_pass_evt"] == 0)


def test_insert_new_metric_signup_pass():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()

    assert (metric["signup_federate_evt"] == 0)
    assert (metric["signup_pass_evt"] == 0)

    new_metric = bytes('{"event":"Signup","is_federate":"false"}', 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["users"].find_one()

    assert (metric["signup_federate_evt"] == 0)
    assert (metric["signup_pass_evt"] == 1)


def test_insert_new_metric_login():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()

    assert (metric["login_federate_evt"] == 0)
    assert (metric["login_pass_evt"] == 0)

    new__metric = bytes('{"event":"Login","is_federate":"true"}', 'utf-8')
    crud.insert_metric(db, new__metric)

    metric = db["users"].find_one()

    assert (metric["login_federate_evt"] == 1)
    assert (metric["login_pass_evt"] == 0)

    new__metric = bytes('{"event":"Login","is_federate":"false"}', 'utf-8')
    crud.insert_metric(db, new__metric)

    metric = db["users"].find_one()
    assert (metric["login_federate_evt"] == 1)
    assert (metric["login_pass_evt"] == 1)

    new__metric = bytes('{"event":"Login","is_federate":"false"}', 'utf-8')
    crud.insert_metric(db, new__metric)

    metric = db["users"].find_one()
    assert (metric["login_federate_evt"] == 1)
    assert (metric["login_pass_evt"] == 2)


def test_insert_new_metric_block():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()

    assert (metric["block_evt"] == 0)

    new_metric = bytes('{"event":"Block"}', 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["users"].find_one()

    assert (metric["block_evt"] == 1)


def test_insert_new_metric_unblock():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()
    assert (metric["block_evt"] == 0)

    new_metric = bytes('{"event":"Block"}', 'utf-8')
    crud.insert_metric(db, new_metric)
    metric = db["users"].find_one()

    assert (metric["block_evt"] == 1)

    new_metric = bytes('{"event":"Unblock"}', 'utf-8')
    crud.insert_metric(db, new_metric)
    metric = db["users"].find_one()

    assert (metric["block_evt"] == 0)


def test_insert_new_metric_reset():
    db = mongomock.MongoClient().db
    crud.insert_users_metric_empty(db)

    metric = db["users"].find_one()

    assert (metric["reset_evt"] == 0)

    new_metric = bytes('{"event":"Reset"}', 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["users"].find_one()

    assert (metric["reset_evt"] == 1)


def test_insert_new_metric_voyages():
    db = mongomock.MongoClient().db
    crud.insert_voyages_metric_empty(db)
    metric = db["voyages"].find_one()

    assert (metric["voyages"] == 0)
    assert (metric["average_duration"] == 0)
    assert (metric["vip_voyages"] == 0)
    assert (metric["no_vip_voyages"] == 0)

    body = '{"event":"Voyage", "duration": 10, "is_vip": "true"}'
    new_metric = bytes(body, 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["voyages"].find_one()

    assert (metric["voyages"] == 1)
    assert (metric["average_duration"] == 10)
    assert (metric["vip_voyages"] == 1)
    assert (metric["no_vip_voyages"] == 0)

    body = '{"event":"Voyage", "duration": 90, "is_vip": "true"}'
    new_metric = bytes(body, 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["voyages"].find_one()

    assert (metric["voyages"] == 2)
    assert (metric["average_duration"] == 50)
    assert (metric["vip_voyages"] == 2)
    assert (metric["no_vip_voyages"] == 0)

    body = '{"event":"Voyage", "duration": 10, "is_vip": "false"}'
    new_metric = bytes(body, 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["voyages"].find_one()

    assert (metric["voyages"] == 3)
    assert (metric["average_duration"] > 36.66
            and metric["average_duration"] < 36.7)
    assert (metric["vip_voyages"] == 2)
    assert (metric["no_vip_voyages"] == 1)


def test_insert_new_metric_payments():
    db = mongomock.MongoClient().db
    crud.insert_payments_metric_empty(db)
    metric = db["payments"].find_one()

    assert (metric["payments_success"] == 0)
    assert (metric["payments_fail"] == 0)
    assert (metric["average_price"] == 0)

    body = '{"event":"Payment", "status": "true", "price": "100"}'
    new_metric = bytes(body, 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["payments"].find_one()

    assert (metric["payments_success"] == 1)
    assert (metric["payments_fail"] == 0)
    assert (metric["average_price"] == 100)

    body = '{"event":"Payment", "status": "false", "price": "200"}'
    new_metric = bytes(body, 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["payments"].find_one()

    assert (metric["payments_success"] == 1)
    assert (metric["payments_fail"] == 1)
    assert (metric["average_price"] == 100)

    body = '{"event":"Payment", "status": "true", "price": "200"}'
    new_metric = bytes(body, 'utf-8')
    crud.insert_metric(db, new_metric)

    metric = db["payments"].find_one()

    assert (metric["payments_success"] == 2)
    assert (metric["payments_fail"] == 1)
    assert (metric["average_price"] == 150)
