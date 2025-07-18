# Save this in a file, e.g., generate_token.py
import jwt
token = jwt.encode({"role": "pro"}, "testsecret", algorithm="HS256")
print(token)
