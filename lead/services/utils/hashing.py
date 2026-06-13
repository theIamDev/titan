import hashlib


class Hashing:

    def __init__(self,*params):
        self.hashable_string = ''.join(str(a) for a in params)

    def hash(self):
        return self.__create_hash_for_string()

    def __create_hash_for_string(self):
        hash_func = hashlib.sha256()
        encoded_string = self.hashable_string.encode()
        hash_func.update(encoded_string)
        return hash_func.hexdigest()