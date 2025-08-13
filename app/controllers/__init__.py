import uuid
import hashlib

user_id = str(uuid.uuid4())

password = 'admin123'
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print(hashed_password)

print("UserID:", user_id)
print("Hashed Password:", hashed_password)
