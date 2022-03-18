from operator import mod
import re
import jwt
from src.database.redis import MyRedis

from src import models
import src.config as config
import src.database.sqlite as sqlite
from typing import Optional, Any


REDIS_VERIFY_ACTION_KEY = 'verify'
REDIS_JWT_ACTION_KEY = 'jwt'


class MyAuthClass:
    def __init__(self, database: sqlite.MyDatabase, redis: MyRedis) -> None:
        self.myDatabase: sqlite.MyDatabase = database
        self.myRedis: MyRedis = redis


    async def auth_email(self, email: str) -> Optional[models.User]:
        user = await self.myDatabase.getAUserByEmail(email=email)
        if (not user):
            return None
        return user


    def encode_jwt(self, payload):
        return jwt.encode(payload, config.SECRET, algorithm='HS256')


    def decode_jwt(self, raw_string):
        return jwt.decode(raw_string, config.SECRET, algorithms=['HS256'])


    def regex_validate_for_jwt(self, raw_string):
        return bool(re.match(r'^[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+)?$', raw_string))


    # jwt: JSON Web Token
    async def auth_jwt_string(self, raw_jwt_string) -> Optional[models.User]:
        # print("the jwt I got: ", raw_jwt_string)
        
        if not self.regex_validate_for_jwt(raw_jwt_string):
            return None

        try: 
            object = self.decode_jwt(raw_jwt_string)
        except Exception as e:
            print(e)
            return None

        email = object.get('email')
        random_string = object.get('random_string')
        if not email or not random_string:
            return None
        
        verified = await self.check_if_the_info_is_in_verified_pool(email=email, random_string=random_string)
        if not verified:
            return None
        
        # if it is verified in redis but not in database, we save it to database
        user = await self.myDatabase.getAUserByEmail(email=email)
        if user is not None:
            return user
        else:
            if await self.myDatabase.addAUser(models.User(email=email)):
                return await self.myDatabase.getAUserByEmail(email=email)
            return None


    async def get_auth_jwt_string(self, email: str, random_string: str) -> str:
        return self.encode_jwt({'email': email, 'random_string': random_string})


    async def add_info_to_unverified_pool(self, email: str, random_string: str) -> None:
        key = f"{email}.{REDIS_VERIFY_ACTION_KEY}"
        value = f"{random_string}.deviceID"
        self.myRedis.set(key, value)
    
    async def check_if_any_info_matchs_in_unverified_pool(self, email: str, random_string: str) -> bool:
        key = f"{email}.{REDIS_VERIFY_ACTION_KEY}"
        value = f"{random_string}.deviceID"
        return self.myRedis.get(key) == value
    
    async def add_info_to_verified_pool(self, email: str, random_string: str) -> None:
        key = f"{email}.{REDIS_JWT_ACTION_KEY}"
        value = f"{random_string}.deviceID"
        self.myRedis.set(key, value)
    

    async def check_if_the_info_is_in_verified_pool(self, email: str, random_string: str) -> bool:
        key = f"{email}.{REDIS_JWT_ACTION_KEY}"
        value = f"{random_string}.deviceID"
        return self.myRedis.get(key) == value
