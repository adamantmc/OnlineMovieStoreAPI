import random
import string
from typing import List


def get_unique_random_strings(no_strings: int = 10, str_len: int = 10) -> List[str]:
    strings = set()

    while len(strings) != no_strings:
        strings.add(get_random_string(str_len))

    return list(strings)


def get_random_string(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits

    rand_str = "".join([random.choice(chars) for i in range(length)])
    return rand_str


def get_random_int(lower: int, upper: int) -> int:
    return random.randint(lower, upper)


def get_all_objects_pagination(client, response):
    objects = []

    done = False

    while not done:
        objects.extend(response.data["results"])

        if response.data["next"] is None:
            done = True
        else:
            response = client.get(response.data["next"])

    return objects