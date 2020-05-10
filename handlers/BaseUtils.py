
import random
import time
from string import digits, ascii_letters

def get_cur_time_ms():
    return int(time.time() * 1000)

def random_string(size, chars=ascii_letters + digits):
    return ''.join([random.choice(chars) for _ in range(size)])