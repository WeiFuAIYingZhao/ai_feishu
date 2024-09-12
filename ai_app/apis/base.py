import json
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from errors import FeishuError, ERRORS

def decrypt_aes(encrypt_key: str, encrypted: str) -> dict:
    """解密飞书事件回调加密部分

    https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM#%E9%80%9A%E8%BF%87Encrypt%20Key%E5%8A%A0%E5%AF%86%E6%95%B0%E6%8D%AE
    Args:
        encrypt_key: 飞书后台加密用的encrypt_key
        encrypted: 加密的密文
    """
    if not encrypt_key:
        raise FeishuError(ERRORS.MISSING_ENCRYPT_KEY, "飞书推送了需要解密的消息, 但是配置的encrypt_key为空")
    block_size = 16
    decoded = base64.b64decode(encrypted)
    iv = decoded[:block_size]
    key = hashlib.sha256(encrypt_key.encode()).digest()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    raw = cipher.decryptor().update(decoded[block_size:])
    if raw[-1] <= block_size:
        # unpad
        raw = raw[:-raw[-1]]
    return json.loads(raw)