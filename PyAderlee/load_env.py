"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

Environment class for decoding environment variables
"""
from dotenv import load_dotenv
import os
from .secure_data import SecureData
load_dotenv()

class Environment:
    '''
    Environment class for decoding environment variables

    Features:
        - Decode environment variables
        - Encode environment variables
        - Check if environment variables are encoded
        - Decode environment variables
        - Encode environment variables
        - Check if environment variables are encoded

    Usage:
        env = Environment()
        print(env.decodeEnv("YOUR_ENV_KEY"))
    '''
    def __init__(self):
        self.aderlee_security = os.getenv("ADERLEE_SECURITY")

    def readEnv(self, env_key: str):
        return self.decodeEnv(env_key)
    def decodeEnv(self, env_key: str):
        env_value = os.getenv(env_key)
        if env_value == "":
            return ""
        if env_value:
            secret_keys = []
            if self.aderlee_security:
                secret_keys.append(self.aderlee_security)
            secret_keys.append(env_key)
            decoded = SecureData(*secret_keys)
            if decoded.is_encoded(env_value):
                return decoded.decode(env_value)
            else:
                return env_value
        else:
            return None