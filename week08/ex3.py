from functools import wraps
from datetime import datetime
import time


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        tstart = datetime.now()
        result = f(*args, **kwargs)
        tend = datetime.now()
        print(tend - tstart)
        return result

    return wrapper


@timer
def add(a, b):
    time.sleep(10)
    return a + b


print(add(1, 2))
