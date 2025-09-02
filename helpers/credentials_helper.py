import os
import json 

from google.cloud import secretmanager


CREDENTIALS_SECRET = os.environ.get("CREDENTIAL_SECRET")


def get_credentials():    
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=CREDENTIALS_SECRET, ).payload.data.decode("UTF-8")

    creds_dict = json.loads(response)

    return creds_dict
