import asyncio
import grpc
import message_pb2
import message_pb2_grpc


# Реализуем логику сервиса, описанного в .proto
class GreeterService(message_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        print(f"[gRPC Server] Получен запрос для имени: {request.name}")
        return message_pb2.HelloReply(message=f"Привет, {request.name}! Это ответ по gRPC.")


async def serve():
    server = grpc.aio.server()
    message_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC сервер запущен на порту 50051...")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
