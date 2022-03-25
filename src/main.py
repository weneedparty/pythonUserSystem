
from datetime import datetime
import sys
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import config
from src import utils
from src import models


import os
redis_NETWORK_NAME = os.getenv("redis_NETWORK_NAME")
if redis_NETWORK_NAME:
    config.REDIS_HOST_URL = redis_NETWORK_NAME


from src.auth import MyAuthClass
import src.database.sqlite as sqlite
from src.database.redis import MyRedis

myDatabase = sqlite.MyDatabase(DATABASE_URL=config.DATABASE_URL)
myRedis = MyRedis(redis_host_URL=config.REDIS_HOST_URL)
myAuthClass = MyAuthClass(database=myDatabase, redis=myRedis)

myO365 = utils.MyO365(config.O365_credentials)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@ app.get("/", response_model=str)
async def home():
    return "Hello, World!"


@ app.post("/user_register_request/", response_model=models.UserRegisterOutput)
async def user_register(input: models.UserRegisterInput):
    email = input.email
    if not utils.check_if_it_is_email(email):
        return models.UserRegisterOutput.parse_obj({"result": "failed.", "error": "email is not valid."})

    randomString = utils.generate_x_random_string(x=6)
    await myAuthClass.add_info_to_unverified_pool(email=email, random_string=randomString)

    myO365.send_email(email, "Thanks for register WeLoveParty App", "Here is your verification code: " + randomString)

    return models.UserRegisterOutput.parse_obj({"result": "success.", "error": None})


@ app.post("/user_register_confirm/", response_model=models.UserRegisterConfirmOutput)
async def user_register_confirm(input: models.UserRegisterConfirmInput):
    email = input.email
    randomString = input.random_string

    matched = await myAuthClass.check_if_any_info_matchs_in_unverified_pool(email=email, random_string=randomString)
    if (not matched):
        return models.UserRegisterConfirmOutput.parse_obj({"result": None, "error": "No matched info found."})
    
    await myAuthClass.add_info_to_verified_pool(email=email, random_string=randomString)
    jwt_string = await myAuthClass.get_auth_jwt_string(email=email, random_string=randomString)
    return models.UserRegisterConfirmOutput.parse_obj(
    {
        "result": {
            "jwt": jwt_string,
        }, 
        "error": None
    })



@ app.post("/auth_jwt/", response_model=models.AuthJwtOutput)
async def auth_jwt(input: models.AuthJwtInput):
    user = await myAuthClass.auth_jwt_string(raw_jwt_string=input.jwt)

    if (user is None):
        return models.AuthJwtOutput.parse_obj({"email": "", "error": "Invalid JWT."})
    
    return models.AuthJwtOutput.parse_obj({"email": user.email, "error": None})



@ app.post("/get_data/", response_model=models.GetDataOutput)
async def get_data(input: models.GetDataInput):
    user = await myAuthClass.auth_jwt_string(raw_jwt_string=input.jwt)

    if (user is None):
        return models.GetDataOutput.parse_obj({"result": None, "error": "Invalid JWT."})
    
    return models.GetDataOutput.parse_obj({"result": "Hello, " + user.email + "!", "error": None})


def start():
    # launch with: poetry run dev

    port = sys.argv[-1]
    if port.isdigit():
        port = int(port)
    else:
        port = 40052

    while utils.is_port_in_use(port):
        port += 1

    print(f"\n\n\nThe service is running on: http://localhost:{port}\n\n")

    uvicorn.run("src.main:app", host="0.0.0.0",
                port=port, debug=True, reload=True, workers=1)