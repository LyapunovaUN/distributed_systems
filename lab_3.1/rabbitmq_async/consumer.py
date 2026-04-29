import pika
import grpc
import sys
import os

# Добавляем путь к gRPC модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '../grpc_sync'))
import message_service_pb2
import message_service_pb2_grpc

def call_stock(product_id, sold_qty):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)
        resp = stub.StockManagement(message_service_pb2.StockRequest(product_id=product_id, sold_quantity=sold_qty))
        return f"Remaining stock: {resp.remaining_quantity}"

def call_uuid(text):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)
        resp = stub.GenerateUUID(message_service_pb2.UUIDRequest(any_text=text))
        return f"Generated UUID: {resp.uuid}"

def call_reverse(text):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)
        resp = stub.ReverseString(message_service_pb2.ReverseRequest(original_text=text))
        return f"Reversed: {resp.reversed_text}"

def process_message(body):
    msg = body.decode()
    print(f" [→] Received: {msg}")
    
    if msg.startswith("stock:"):
        _, rest = msg.split(":", 1)
        pid, qty = rest.split(":")
        return call_stock(pid, int(qty))
    elif msg.startswith("uuid:"):
        _, text = msg.split(":", 1)
        return call_uuid(text)
    elif msg.startswith("reverse:"):
        _, text = msg.split(":", 1)
        return call_reverse(text)
    else:
        return f"Unknown: {msg}"

def callback(ch, method, properties, body):
    result = process_message(body)
    print(f" [✓] Result: {result}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    
    print(" [*] Waiting for messages. Press CTRL+C to exit")
    channel.start_consuming()

if __name__ == '__main__':
    main()