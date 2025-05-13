import random
import string

def generate_class_code(length=6):
    return ''.join(random.choices('0123456789abcdef', k=length))