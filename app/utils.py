from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.hash(password)

def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)



# """
# testing another method of hashing
# """
# class Authenticate:
#     def create_salt_and_hashed_password(self, *, plaintext_password: str):
#         salt = self.generate_salt()
#         hashed_password = self.hash_password(password=plaintext_password, salt=salt)
#         return updatePassword(salt=salt, password=hashed_password)


#     def generate_salt():
#         return bcrypt.gensalt().decode()


#     def hash_password(*, password: str, salt: str) -> str:
#         return pwd_context.hash(password + salt)