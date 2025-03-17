import random
import string

class StaffFactoryService:

    def __init__(self):
        pass

    @staticmethod
    def generate_random_password(length):
        characters = list(string.ascii_letters + string.digits + "!@#$%&")
        random.shuffle(characters)
        password = []
        for item in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        password = "".join(password)
        print(password)
        return password
