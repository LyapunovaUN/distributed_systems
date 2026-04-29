import pika
import sys

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

if len(sys.argv) < 2:
    print("Usage:")
    print("  python3 producer.py stock:item_001:5")
    print("  python3 producer.py uuid:hello_world")
    print("  python3 producer.py reverse:OpenAI")
    sys.exit(1)

message = sys.argv[1]

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print(f" [x] Sent: {message}")
connection.close()