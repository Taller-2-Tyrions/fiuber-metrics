import pika
from ..crud import crud
from ..database.mongo import db
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("CLOUDAMQP_URL")
METRICS_QUEUE = os.getenv("METRICS_QUEUE")


def metrics_users_process_function(msg):
    print("Metrics users processing init ...")
    print("[x] Received: " + str(msg))

    crud.insert_metric(db, msg)

    print("Metrics users processing finished!")
    return


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    metrics_users_process_function(body)


def run_rabbit_service():
    print("Starting rabbit services...")

    print("Check empty database ...")
    crud.insert_users_metric_empty()
    crud.insert_payments_metric_empty()
    crud.insert_voyages_metric_empty()

    # Access the CLODUAMQP_URL environment variable and parse it
    # (fallback to localhost)
    # change!
    params = pika.URLParameters(URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue=METRICS_QUEUE)  # Declare a queue

    # set up subscription on the queue
    channel.basic_consume(METRICS_QUEUE, callback, auto_ack=True)

    # start consuming (blocks)
    channel.start_consuming()
    connection.close()

    print("Stopping rabbit services...")
