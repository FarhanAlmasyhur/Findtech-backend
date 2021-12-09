import os
from dotenv import load_dotenv

load_dotenv()

findtechkey = {
  "type": os.environ.get("TYPE"),
  "project_id":  os.environ.get("PROJECT_ID"),
  "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
  "private_key": os.environ.get("PRIVATE_KEY").replace("\\n", "\n"),
  "client_email": os.environ.get("CLIENT_EMAIL"),
  "client_id": os.environ.get("CLIENT_ID"),
  "auth_uri": os.environ.get("AUTH_URI"),
  "token_uri": os.environ.get("TOKEN_URI"),
  "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
  "client_x509_cert_url": os.environ.get("client_x509_cert_url")
}