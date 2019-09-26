"""
In this service, for convenience, ethereum private keys and
addresses are generated in real time when registering an account.
In production, ethereum wallets are typically pre-generated for security reasons and
then assigned an address to the ethereum wallet at registration to prevent the database from being hacked and
the private key being held by the hacker.
"""
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import os
import sha3
import string
from random import choice


def privateKey2publicKey(private_key_string):
    sk = SigningKey.from_string(bytes.fromhex(private_key_string), curve=SECP256k1)
    vk = sk.get_verifying_key()
    return vk.to_string().hex()


def publicKey2address(public_key):
    sha3256 = sha3.keccak_256(bytes().fromhex(public_key)).hexdigest()
    return '0x' + sha3256[-40:]


def generate_eth_wallet():
    private_key = os.urandom(32).hex()
    public_key = privateKey2publicKey(private_key)
    address = publicKey2address(public_key)
    return private_key, address


def generate_port_password(length=6, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for _ in range(length)])
