import random
from werkzeug.security import generate_password_hash, check_password_hash

class utils:
    def random_num(limit=6):
        range_start = 10**(limit-1)
        range_end = (10**limit)-1
        return random.randint(range_start, range_end)
    
    def hash_password(password_text):
	    return generate_password_hash(password_text)