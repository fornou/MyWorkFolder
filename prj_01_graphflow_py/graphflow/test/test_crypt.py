from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hash = pwd_context.hash("mia_password")
print(pwd_context.verify("mia_password", hash))  # Deve stampare True
