import pika, os, time
from ..crud import crud
from ..database.mongo import db

def metrics_users_process_function(msg):
  print("Metrics users processing init ...")
  print("[x] Received: " + str(msg))

  crud.insert_metric(db, msg)

  print("Metrics users processing finished!");
  return;

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  metrics_users_process_function(body)


def run_rabbit_service():
  print("Starting rabbit services...")

  print("Check empty database ...")
  crud.insert_users_metric_empty()
  crud.insert_payments_metric_empty()
  crud.insert_voyages_metric_empty()

  # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
  url = os.environ.get('CLOUDAMQP_URL', 'amqps://wjcumqjk:5YBAhdzlge0w0Itf5t94VPWy_h0xs8cX@chimpanzee.rmq.cloudamqp.com/wjcumqjk')
  params = pika.URLParameters(url)
  connection = pika.BlockingConnection(params)
  channel = connection.channel() # start a channel
  channel.queue_declare(queue='metrics.users') # Declare a queue


  # set up subscription on the queue
  channel.basic_consume('metrics.users',
    callback,
    auto_ack=True)

  # start consuming (blocks)
  channel.start_consuming()
  connection.close()

  print("Stopping rabbit services...")