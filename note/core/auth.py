import os
from typing import MutableMapping
from hashlib import scrypt
from jose import jwt


def encode_token(claims: MutableMapping[str, any]):
    return jwt.encode(claims=claims, key=os.getenv("SECRET_KEY"))


def decode_token(token: str):
    return jwt.decode(token, key=os.getenv("SECRET_KEY"))


def hash_password(plain_password: str, salt: bytes = os.urandom(16)):
    hashed_password = scrypt(str.encode(plain_password), salt=salt, n=2**14, r=8, p=1)
    return hashed_password, salt


def verify_password(plain_password: str, hashed_password: bytes, salt: bytes):
    hashed_plain_password, _ = hash_password(plain_password, salt=salt)
    return hashed_plain_password == hashed_password
