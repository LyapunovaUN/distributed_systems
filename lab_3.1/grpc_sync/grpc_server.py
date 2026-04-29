import grpc
from concurrent import futures
import uuid
import message_service_pb2
import message_service_pb2_grpc

# Имитация склада
stock_db = {
    "item_001": 100,
    "item_002": 50,
    "item_003": 200,
}

class MessageService(message_service_pb2_grpc.MessageServiceServicer):
    
    def StockManagement(self, request, context):
        product_id = request.product_id
        sold = request.sold_quantity
        
        if product_id not in stock_db:
            stock_db[product_id] = 0
        
        if stock_db[product_id] < sold:
            context.set_code(grpc.StatusCode.OUT_OF_RANGE)
            context.set_details(f"Not enough stock for {product_id}")
            return message_service_pb2.StockResponse(remaining_quantity=stock_db[product_id])
        
        stock_db[product_id] -= sold
        print(f"✅ Stock: {product_id} -> remaining = {stock_db[product_id]}")
        return message_service_pb2.StockResponse(remaining_quantity=stock_db[product_id])
    
    def GenerateUUID(self, request, context):
        generated = str(uuid.uuid4())
        print(f"🔑 UUID for '{request.any_text}' -> {generated}")
        return message_service_pb2.UUIDResponse(uuid=generated)
    
    def ReverseString(self, request, context):
        reversed_str = request.original_text[::-1]
        print(f"🔄 Reversed: '{request.original_text}' -> '{reversed_str}'")
        return message_service_pb2.ReverseResponse(reversed_text=reversed_str)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_service_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()