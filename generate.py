from jose import jwt
import datetime

SECRET_KEY = "dev-secret-key"
ALGORITHM = "HS256"

payload = {
    "sub": "test-user",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(token)