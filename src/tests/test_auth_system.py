from random import random
from src.database.redis import MyRedis
import src.models as models
from datetime import datetime
import src.database.sqlite as sqlite
import src.auth as auth

async def run(myDatabase: sqlite.MyDatabase, my_redis: MyRedis):
    myAuthClass = auth.MyAuthClass(database=myDatabase, redis=my_redis)

    # test delete all users
    await myDatabase.deleteAllUsers()

    # test delete all redis cache
    my_redis.delete_all()

    # consts
    email = "yingshaoxo@gmail.com"
    random_string = "asdfhjh"

    # init check
    result = await myAuthClass.check_if_any_info_matchs_in_unverified_pool(email=email, random_string=random_string)
    assert result == False

    result = await myAuthClass.check_if_the_info_is_in_verified_pool(email=email, random_string=random_string)
    assert result == False

    # add info to unverified pool
    await myAuthClass.add_info_to_unverified_pool(email=email, random_string=random_string)

    # check if matchs unverified pool with wrong info
    result = await myAuthClass.check_if_any_info_matchs_in_unverified_pool(email=email, random_string=random_string*2)
    assert result == False

    # check if matchs unverified pool with right info
    result = await myAuthClass.check_if_any_info_matchs_in_unverified_pool(email=email, random_string=random_string)
    assert result == True

    # check if matchs verified pool with right info | it should be False since I didn't add it to verified pool yet
    result = await myAuthClass.check_if_the_info_is_in_verified_pool(email=email, random_string=random_string)
    assert result == False

    # add info to verified pool
    await myAuthClass.add_info_to_verified_pool(email=email, random_string=random_string)

    # check if matchs verified pool with right info
    result = await myAuthClass.check_if_the_info_is_in_verified_pool(email=email, random_string=random_string)
    assert result == True

    # check if matchs verified pool with wrong info
    result = await myAuthClass.check_if_the_info_is_in_verified_pool(email=email, random_string=random_string*2)
    assert result == False

    # get jwt
    jwt = await myAuthClass.get_auth_jwt_string(email=email, random_string=random_string)

    # auth jwt
    user = await myAuthClass.auth_jwt_string(raw_jwt_string=jwt)
    assert user is not None

    # get wrong jwt
    wrong_jwt = await myAuthClass.get_auth_jwt_string(email=email, random_string=random_string*2)

    # auth wrong jwt
    user = await myAuthClass.auth_jwt_string(raw_jwt_string=wrong_jwt)
    assert user is None