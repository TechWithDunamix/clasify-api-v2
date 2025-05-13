import uuid
import random
import string


def generate_membership_code(prefix="MEM", length=8):
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    unique_segment = str(uuid.uuid4()).split('-')[0].upper()  # short unique ID
    return f"{prefix}-{random_part}-{unique_segment}"

