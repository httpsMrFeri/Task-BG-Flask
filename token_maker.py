import json
import secrets

tokens = [secrets.token_hex(16) for _ in range(10)]

with open('tokens.json', 'w') as file:
    json.dump({"tokens": tokens}, file)
