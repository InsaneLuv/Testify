import json
from cryptography.fernet import Fernet

class QuizCrypto:
    DELIMITER = b'AS_ABii_'

    def __init__(self):
        self.key = None

    def generateKey(self):
        self.key = Fernet.generate_key()
        return self.key

    def encryptData(self, data):
        if not self.key:
            self.generateKey()
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode())

    def encryptToFile(self, filePath, jsonData):
        if not self.key:
            self.generateKey()
        encrypted_data = self.encryptData(jsonData)
        with open(filePath, 'wb') as f:
            f.write(self.key + self.DELIMITER + encrypted_data)

    @staticmethod
    def decryptData(encryptedData, key):
        fernet = Fernet(key)
        decryptedData = fernet.decrypt(encryptedData).decode()
        return decryptedData

    def decryptFromFile(self, filePath):
        with open(filePath, 'rb') as f:
            content = f.read()
            key, encryptedData = content.split(self.DELIMITER, 1)
        decrypted_data = self.decryptData(encryptedData, key)
        return json.loads(decrypted_data)
