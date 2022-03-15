from src.database.redis import MyRedis
import src.models as models
from datetime import datetime
import src.database.sqlite as sqlite
import src.auth as auth

from fastapi.testclient import TestClient

async def run(myDatabase: sqlite.MyDatabase, client: TestClient, my_redis: MyRedis):
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello" in response.text
    # assert response.json() == {"msg": "Hello World"}

    # test delete all users
    await myDatabase.deleteAllUsers()
    my_redis.delete_all()

    # consts
    email = "yingshaoxo@gmail.com"

    # test user register
    response = client.post("/user_register_request/", json=
        models.UserRegisterInput(
            email=email,
        ).dict()
    )
    response = response.json()
    # print(response)
    assert "error" in response
    assert response.get("error") is None

    # get random string from email
    random_string = input("\nPlease input random string: ").strip()

    # confirm user register with wrong random string
    response = client.post("/user_register_confirm/", json=
        models.UserRegisterConfirmInput(
            email=email,
            random_string=random_string*3,
        ).dict()
    )
    response = response.json()
    assert "error" in response
    assert response.get("error") is not None

    # confirm user register
    response = client.post("/user_register_confirm/", json=
        models.UserRegisterConfirmInput(
            email=email,
            random_string=random_string,
        ).dict()
    )
    response = response.json()
    assert "error" in response
    assert "result" in response
    result = response.get("result")
    assert "jwt" in result
    jwt = result.get("jwt")
    assert jwt is not None

    # auth jwt
    response = client.post("/get_data/", json=
        models.GetDataInput(
            jwt=jwt,
        ).dict()
    )
    response = response.json()

    assert "error" in response
    assert response.get("error") is None

    assert "result" in response
    result = response.get("result")
    assert len(result) > 0

    # auth with wrong jwt
    response = client.post("/get_data/", json=
        models.GetDataInput(
            jwt=jwt * 2,
        ).dict()
    )
    response = response.json()
    assert "error" in response
    assert response.get("error") is not None



