# password_handler.py — Tools for safe password management

from passlib.context import CryptContext

# CryptContext tells passlib WHICH hashing algorithm to use
# bcrypt is the industry standard for password hashing
# It is deliberately slow (unlike MD5/SHA1) to make brute-force attacks impractical
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Take a plain text password like "mypassword123"
    and return a hashed string like "$2b$12$..."
    The hash is different every time even for the same input (bcrypt adds 'salt').
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain text password matches a stored hash.
    Returns True if they match, False if not.
    We use this during login to check "did they type the right password?"
    """
    return pwd_context.verify(plain_password, hashed_password)