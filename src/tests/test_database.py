import src.models as models
from datetime import datetime
import src.database.sqlite as sqlite

async def run(myDatabase: sqlite.MyDatabase):
    # test delete all users
    await myDatabase.deleteAllUsers()

    # test wrong email and password
    user = await myDatabase.getAUserByEmail(email="sad")
    assert user is None

    # test add a new user
    user_id = await myDatabase.addAUser(aUser=models.User(
        email="yingshaoxo@gmail.com",
        username="yingshaoxo",
    ))
    assert user_id is not None

    # test get a user
    shouldBeTrue = await myDatabase.getAUser(id=1)
    assert shouldBeTrue != None

    # test list users
    user_list = await myDatabase.listUsers()
    assert len(user_list) == 1

    # test update a user
    old_user = await myDatabase.getAUser(id=user_id)
    if old_user is not None:
        old_user.username = "yingshaoxo_new"
        user_id = await myDatabase.updateAUser(id=1, aUser=old_user)
        new_user = await myDatabase.getAUser(id=user_id)
        if new_user is not None:
            assert new_user.username == "yingshaoxo_new"

    # test delete a user
    if old_user is not None and old_user.id is not None:
        shouldBeTrue = await myDatabase.deleteAUser(id=old_user.id)
        assert shouldBeTrue == True
