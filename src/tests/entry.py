import asyncio
from fastapi.testclient import TestClient
from src.main import app

import src.tests.test_database as test_database
import src.tests.test_redis as test_redis
from src.tests import test_auth_system
from src.tests import test_restful_api 

import src.database.sqlite as sqlite
from src.database.redis import MyRedis
import src.config as config

client = TestClient(app)
myDatabase = sqlite.MyDatabase(DATABASE_URL=config.DATABASE_URL)
my_redis = MyRedis(redis_host_URL='localhost')

async def async_function():
    await test_database.run(myDatabase=myDatabase)
    await test_redis.run(my_redis=my_redis)
    await test_auth_system.run(myDatabase=myDatabase, my_redis=my_redis)
    # await test_restful_api.run(client=client, myDatabase=myDatabase, my_redis=my_redis)

def main():
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_function())