import asyncio
from distutils.log import error
from src.generated_grpc import account_service
from grpclib.server import Server
from typing import AsyncIterator


class MyAccountService(account_service.AccountServiceBase):
    async def SayHello(self, request: account_service.HelloRequest) -> account_service.HelloReply:
        print(request.name)
        return account_service.HelloReply(message="hi")

    async def UserRegisterRequest(self, request: account_service.RegisterRequest) -> account_service.RegisterReply:
        return account_service.RegisterReply(
            result="",
            error=""
        )

    async def UserRegisterConfirm(self, request: account_service.RegisterConfirmRequest) -> account_service.RegisterConfirmReply:
        return account_service.RegisterConfirmReply(
            result=account_service.JwtObject(jwt=""),
            error=""
        )

    async def JWTIsOK(self, request: account_service.JwtIsOkRequest) -> account_service.JwtIsOkReply:
        return account_service.JwtIsOkReply(
            ok=True,
        )

async def run():
    host = "0.0.0.0"
    port = 40053

    server = Server([MyAccountService()])
    await server.start(host, port)
    print(f"\nPython account service is running on: http://{host}:{port}")
    await server.wait_closed()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())