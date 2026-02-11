import random
import string

def generate_password(length=12, use_special_chars=False):
  characters = string.ascii_letters + string.digits
  if use_special_chars:
    characters += string.punctuation

  password = [
    random.choice(string.ascii_lowercase),
    random.choice(string.ascii_uppercase),
    random.choice(string.digits),
  ]
  if use_special_chars:
    password.append(random.choice(string.punctuation))

  while len(password) < length:
    password.append(random.choice(characters))

  random.shuffle(password)
  return ''.join(password)
