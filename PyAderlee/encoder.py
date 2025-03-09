"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy LLC
Developer: Khaled Karman <k@rawasy.com>

A lightweight Python library for data processing and file handling.
"""

from typing import List, Dict, Any
import time, base64, hashlib, os, json

class Encoder:
    '''Aderlee Encoder/Decoder
    
    Encode & Decode sensitive data into a secure format

    Author: Khaled Karman
    Type: Internal class
    Date: 2025-03-08
    Usage:
        encoder = Encoder(SECURITY_KEY + env_key)
        encoded = encoder.encode("Hello, World!")
        decoded = encoder.decode(encoded)
        print(encoded, decoded)

    Post-History: 2023-12-28 
    Required Libraries:
        pip install PyAderlee
    '''
    
    
    _timestamp = None
    _authorized = False
    _authorized_tables = []
    _authorized_actions = []
    _ascii_table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+='
    _encode_table = None
    _secret_key = "khaled karman"
    _secret_key_split = None
    _default_algorithms = "sha512"
    _algorithms_available = ["md5","sha1","sha224","sha256","sha384","sha512","sha3-224","sha3-256","sha3-384","sha3-512","sha3_224","sha3_256","sha3_384","sha3_512"]
    __version__     = '4.0'

    def __init__(self, secret_key=None):
        self._timestamp = time.time()
        self._ascii_table = self._ascii_table+self._ascii_table
        self._encode_table = self._ascii_table
        if secret_key!=None: self._secret_key+=secret_key
        self._secret_key = self.sha512(self._secret_key)
        self._secret_key_split = [x for x in self._secret_key]
        self._secret_key_split_shift = [x for x in self._secret_key]
        
    def _update_curr_time(self):
        self._timestamp = time.time()
        return self._timestamp

    def get_ascii_table(self, pos=0):
        asscii_len = len(self._ascii_table)
        pos=pos % (63-1)
        return self._ascii_table[pos:pos+64]

    def get_ascii_shift(self, letter, table=None):
        if table==None: table=self._ascii_table
        return table.find(letter)

    def encode(self, word):
        word=base64.b64encode(word.encode("ascii")).decode("ascii")
        word=base64.b64encode(word.encode("ascii")).decode("ascii")
        o = self.prepare_secret_key()
        words = [x for x in word]
        encoded=[]
        w=[]
        for i in range(len(words)):
            c0=self.get_ascii_table(0)
            c=self.get_ascii_table(o[i])
            d = self.get_ascii_shift(words[i], c)
            d2 = self.get_ascii_shift(c[d])
            # print(d)
            encoded.append(c0[d])
            w.append({
                "orig":words[i],
                "encoder":o[i],
                "encoded":c0[d],
                "decoded":c[d],
            })
        return base64.b64encode(str.encode("".join(encoded))).decode("utf-8")

    def prepare_secret_key(self):
        r = []
        for x in self._secret_key.lower():
            ff = self._ascii_table.find(x)
            if ff<0: ff = 0
            r.append(ff)
        o = []
        for x in range(50): o=o+r
        return o

    def decode(self, word):
        word= base64.b64decode(word).decode("utf-8")
        o = self.prepare_secret_key()
        words = [x for x in word]
        encoded=[]
        w=[]
        for i in range(len(words)):
            c0=self.get_ascii_table(o[i])
            c=self.get_ascii_table(0)
            d = self.get_ascii_shift(words[i], c)
            d2 = self.get_ascii_shift(c[d])
            encoded.append(c0[d])
            w.append({
                "orig":words[i],
                "encoder":o[i],
                "encoded":c0[d],
                "decoded":c[d],
            })
        word = "".join(encoded).encode("ascii")
        word = base64.b64decode(word).decode("ascii")
        word = base64.b64decode(word).decode("ascii")
        return word

    def check_authintication(self):
        return self._authorized

    def md5(self, val):
        return hashlib.md5(val.encode()).hexdigest()

    def sha512(self, val):
        return hashlib.sha512(val.encode()).hexdigest()

    def hash(self, val, alg="sha512"):
        if alg not in self._algorithms_available:
            print(f"ERROR: Unknow algorithm {alg}")
            return False
        h = hashlib.new(alg)
        h.update(val.encode())
        return h.hexdigest()

    def secure(self, val):
        a = self.hash(val, "sha512")
        b = self.hash(val, "sha3-512")
        return "".join([f"{x[0]}{x[1]}" for x in list(zip([x for x in a], [x for x in b]))])
    
    # """
    # A class to handle encoding and decoding of various data formats

    
    # """
    # @staticmethod
    # def to_json(data: Any, indent: int = 4) -> str:
    #     """Convert data to JSON string"""
    #     return json.dumps(data, indent=indent)
    
    # @staticmethod
    # def from_json(json_str: str) -> Any:
    #     """Parse JSON string to Python object"""
    #     return json.loads(json_str)
    
    # @staticmethod
    # def to_csv(data: List[Dict], delimiter: str = ',') -> str:
    #     """Convert list of dictionaries to CSV string"""
    #     if not data:
    #         return ""
        
    #     headers = list(data[0].keys())
    #     rows = [delimiter.join(headers)]
        
    #     for item in data:
    #         row = [str(item.get(header, '')) for header in headers]
    #         rows.append(delimiter.join(row))
            
    #     return '\n'.join(rows) 