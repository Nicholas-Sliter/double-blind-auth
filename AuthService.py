import hashlib
import os

class AuthService:
    def __init__(self, db: dict):
        # Note the separation of user data from password data
        # We test user auth by checking for set inclusion of 
        # provided password hashed with salt AND username.
        # This theroetically makes each password unique.
        # And it makes passwords double-blind.
        self.db = db
        self.passwords = set()
    
    def login(self, username: str, password: str) -> bool:
        if username not in self.db['users']:
            return False
        user = self.db['users'][username]

        salt = user['salt']

        blindPassword = self.blindPassword(password, salt, username)
        print(f"Login attempt with {blindPassword}")
        return blindPassword in self.passwords


    def blindPassword(self, password: str, salt: str, username: str) -> str:
        # Hash with salt and username
        return self.hashPassword(salt + password + username)

    def hashPassword(self, password: str) -> str:
        # Hash with SHA256
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str) -> bool:
        if username in self.db['users']:
            return False
        salt = self.generateSalt()
        blindPassword = self.blindPassword(password, salt, username)
        self.db['users'][username] = {
            'salt': salt,
        }
        self.passwords.add(blindPassword)
        return True

    
    def generateSalt(self) -> str:
        # Generate a random salt
        return os.urandom(32).hex()

    def changePassword(self, username: str, oldPassword: str, newPassword: str) -> bool:
        if not self.login(username, oldPassword):
            return False
       
        self.passwords.remove(self.blindPassword(oldPassword, self.db['users'][username]['salt'], username))

        salt = self.generateSalt()
        blindPassword = self.blindPassword(newPassword, salt, username)
        self.db['users'][username] = {
            'salt': salt,
        }

        self.passwords.add(blindPassword)
        return True


    def resetPassword(self, username: str, newPassword: str) -> bool:
        # Note, this resets the password but does not remove the old password
        # The old password is no longer valid, but it is still in the set
        if username not in self.db['users']:
            return False
        salt = self.generateSalt()
        blindPassword = self.blindPassword(newPassword, salt, username)
        self.db['users'][username] = {
            'salt': salt,
        }
        self.passwords.add(blindPassword)
        return True

    def logPasswords(self):
        print("Passwords:")
        for password in self.passwords:
            print(password)
