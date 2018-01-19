import sys
import bcrypt
import re

# Generates password with bcrypt default settings.

if len(sys.argv) < 2:
    print("No password to parse.")
    exit(1)

pre = sys.argv[1]
encoded = bytes(pre, encoding='utf-8')
hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
decoded = hashed.decode('utf-8')

print(decoded)
exit(0)
