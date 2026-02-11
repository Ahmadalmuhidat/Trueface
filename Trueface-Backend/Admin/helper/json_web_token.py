import os
import sys
import jwt

from dotenv import load_dotenv

load_dotenv()

def GenerateToken(payload):
  try:
    return jwt.encode(
      payload = payload,
      key = os.getenv("JWT_TOKEN_SECRET"),
      algorithm = 'HS256'
    )

  except Exception as e: 
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(exc_obj)

def validate_token(token):
  try:
    return jwt.decode(
      token,
      key = os.getenv("JWT_TOKEN_SECRET"),
      algorithms = ['HS256']
    )

  except jwt.ExpiredSignatureError:
    print("Token has expired. Please log in again.")
  except jwt.InvalidTokenError:
    print("Invalid token. Access denied.")
  except Exception as e: 
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(exc_obj)
