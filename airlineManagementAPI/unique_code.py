import random
import string

def generate_unique_code(length=11):
    characters = string.ascii_uppercase + string.digits  # Büyük harfler ve sayılar
    return ''.join(random.choice(characters) for _ in range(length))