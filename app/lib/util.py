from random import choice, randint
import string

def get_random_number():
    return randint(1, 9999)

def get_random_text(length=0):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.whitespace
    if length == 0:
        length = randint(10, 20)
    return ''.join(choice(chars) for _ in range(length))
