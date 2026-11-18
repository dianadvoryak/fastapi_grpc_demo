from contextlib import asynccontextmanager
from fastapi import FastAPI
import grpc
import message_pb2
import message_pb2_grpc

# Словарь для хранения gRPC-клиента (stub)
grpc_client = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте FastAPI открываем соединение с gRPC-сервером
    channel = grpc.aio.insecure_channel("localhost:50051")
    grpc_client["stub"] = message_pb2_grpc.GreeterStub(channel)
    yield
    # При остановке приложения закрываем канал
    await channel.close()


app = FastAPI(lifespan=lifespan)


@app.get("/hello/{name}")
async def send_grpc_request(name: str):
    stub = grpc_client["stub"]

    # Формируем gRPC-запрос и отправляем его на сервер
    request = message_pb2.HelloRequest(name=name)
    response = await stub.SayHello(request)

    # Возвращаем результат пользователю в виде обычного JSON
    return {"grpc_response": response.message}
