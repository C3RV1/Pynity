import base64
from Crypto.Random import random, get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import re
import math

def base64_encode(str):
    return base64.b64encode(str).replace("/", "_")

def base64_decode(str):
    return base64.b64decode(str.replace("_", "/"))

def isBase64(s):
    try:
        return base64_encode(base64_decode(s)) == s
    except Exception:
        return False

def get_random_string(length):
    # type: (int) -> str
    while True:
        returnString = ""
        for x in range(0, length):
            returnString += get_random_bytes(1)
        if "\x00" not in returnString:
            break
    return returnString

def checkProofOfWork(msgToVerify, pow0es, powIterations):
    # type: (str, int, int) -> bool
    hash = SHA256.new(msgToVerify)
    for i in range(0, powIterations - 1):
        hash.update(hash.hexdigest())

    if re.search("^" + "0" * pow0es, hash.hexdigest()):
        return True
    else:
        return False

def isInt(strToTest):
    try:
        num = int(strToTest)
        return True
    except:
        return False

def encryptWithPadding(key, plaintext):
    # type: (str, str) -> tuple
    length = (16 - (len(plaintext) % 16)) + 16 * random.randint(0,14)
    plaintextPadded = plaintext + get_random_string(length-1) + chr(length)
    if len(key) != 16 and len(key) != 32 and len(key) != 24:
        return False, ""
    ciphertext = base64_encode(AES.new(key, AES.MODE_ECB).encrypt(plaintextPadded))
    return True, ciphertext

def decryptWithPadding(key, ciphertext):
    # type: (str, str) -> tuple
    if len(key) != 16 and len(key) != 32 and len(key) != 24:
        return False, ""
    ciphertextNotB64 = base64_decode(ciphertext)
    plaintextPadded = AES.new(key, AES.MODE_ECB).decrypt(ciphertextNotB64)
    plaintext = plaintextPadded[:-ord(plaintextPadded[-1])]
    return True, plaintext

def fromByteToB64Length(length):
    return int(math.ceil(length/3.0)*4)
