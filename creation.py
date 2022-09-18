import json


async def create_warns(user):
    users = await get_warn_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Warns"] = 0

    with open("warns.json", "w") as f:
        json.dump(users, f, indent=2)
    return True


async def get_warn_data():
    with open("warns.json", "r") as f:
        users = json.load(f)
    return users
