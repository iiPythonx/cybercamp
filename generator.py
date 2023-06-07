# Copyright 2023 Benjamin O'Brien

# Modules
import string
import random
from score import score

# Initialization
wordlist = string.ascii_letters + string.digits + string.punctuation

# Main loop
count = 0
while True:
    password = "".join([random.choice(wordlist) for i in range(16)])
    score = score(password)
    if score[0] >= 85:
        print(f"Generated password: {password}\nScore: {score[0]}\nAmount of non-passing passwords: {count}")
        break

    count += 1
