from functools import wraps
import errno
import os
import signal
import time


class TimeoutError(Exception):
    pass


def timeout(seconds=10.0, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(0, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


# Timeout a long running function with the default expiry of 10 seconds.
@timeout(0.9)
def long_running_function1() -> object:
    while True:
        print(time.clock())
        time.sleep(4)

try:
    long_running_function1()

except TimeoutError as e:
    print("going with last best")