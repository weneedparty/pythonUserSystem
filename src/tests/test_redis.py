import src.models as models
from src.database.redis import MyRedis


async def run(my_redis: MyRedis):
    theKey = "hi"

    assert my_redis.get(theKey) is None

    assert my_redis.set(theKey, "hello") is True

    assert my_redis.get(theKey) == "hello"

    my_redis.delete(theKey)

    assert my_redis.get(theKey) is None