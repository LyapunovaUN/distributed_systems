import grpc
import message_service_pb2
import message_service_pb2_grpc

def test():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = message_service_pb2_grpc.MessageServiceStub(channel)
        
        # Тест 1: Управление запасами
        resp1 = stub.StockManagement(message_service_pb2.StockRequest(product_id="item_001", sold_quantity=3))
        print(f"📦 Remaining stock: {resp1.remaining_quantity}")
        
        # Тест 2: UUID
        resp2 = stub.GenerateUUID(message_service_pb2.UUIDRequest(any_text="test"))
        print(f"🔑 UUID: {resp2.uuid}")
        
        # Тест 3: Reverse
        resp3 = stub.ReverseString(message_service_pb2.ReverseRequest(original_text="OpenAI"))
        print(f"🔄 Reversed: {resp3.reversed_text}")

if __name__ == '__main__':
    test()