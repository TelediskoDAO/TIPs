import base64
import datetime
import jwt
import time
import uuid
from web3.auto import w3
from eth_account.messages import encode_defunct

SERVER_SECRET = "My server secret"
# MESSAGE_TEMPLATE = "I allow this website to manage my data on odoo.teledisko.com."
MESSAGE_TEMPLATE = "By signing this message, I allow this website to manage my data on odoo.teledisko.com\n(Request #{})"


def server_get_web3_auth():
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600),
        "message": MESSAGE_TEMPLATE.format(uuid.uuid4().hex),
    }
    signing_token = jwt.encode(payload, SERVER_SECRET, algorithm="HS256")
    print("[Server] Return signing_token:", payload)
    return signing_token


def server_post_web3_auth(encoded_authentication):
    authentication = eval(base64.b64decode(encoded_authentication).decode())
    print("[Server] Verify JWT token:", authentication['signing_token'])
    payload = jwt.decode(authentication['signing_token'], server_secret, algorithms=["HS256"])
    print("[Server] JWT is valid. Extract signature")
    message = encode_defunct(text=payload["message"])
    signer = w3.eth.account.recover_message(message, signature=signature)
    print("[Server] Signer:", signer)

    # Check if the signer is in the Database!

    return jwt.encode(
        {
            "sub": signer,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
            "role": "user",
        },
        SERVER_SECRET,
        algorithm="HS256",
    )


def client_run_authentication():
    wallet = w3.eth.account.create()
    print("[Client] Address:", wallet.address)
    print("[Client] Require signing_token")
    signing_token = server_get_web3_auth()
    payload = jwt.decode(signing_token, algorithms=["HS256"], options={"verify_signature": False})
    print("[Client] Create signature for:", payload["message"])
    message = encode_defunct(text=payload["message"])
    signed_message = w3.eth.account.sign_message(message, private_key=wallet.privateKey)
    print("[Client] Submit signature and require access_token")
    encoded_authentication = {'signing_token': token, 'signature': signed_message.signature}
    encoded_authentication = base64.urlsafe_b64encode(str(encoded_authentication).encode())
    access_token = server_post_web3_auth(encoded_authentication)
    print("[Client] access_token:", access_token)
    

client_run_authentication()
