import random
import time
from datetime import datetime
from uuid import uuid4


def random_string():
    return uuid4()


def random_datetime():
    d = random.randint(1, int(time.time()))
    return datetime.fromtimestamp(d)
