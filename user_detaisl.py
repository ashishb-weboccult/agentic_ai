dict = {"12345": "john", "12346": "jane", "12347": "joe"}
dict_2 = {"12345": "india", "12346": "itali", "12347": "france"}

async def get_user_name(user_id: str):
    return dict.get(user_id)


async def get_user_region(user_id: str):
    return dict_2.get(user_id)


if __name__ == "__main__":
    name = get_user_name("12345")
    print(name) 