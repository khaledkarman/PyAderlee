import hashlib
import base64

class SecureData:
    def __init__(self, *secret_keys):
        """
        Initialize the SecureData with one or more secret keys.
        If no secret keys are provided, the default key "KhaledKarman" is used.
        All provided keys are concatenated into a single key string, which is then
        converted into its SHA‑512 hash (hexadecimal digest) for use as the encryption key.
        """
        # Use the default secret key if none are provided.
        if not secret_keys:
            secret_keys = ("KhaledKarman",)
        
        combined_key = ""
        for key in secret_keys:
            if not isinstance(key, str) or not key:
                raise ValueError("Each secret key must be a non-empty string.")
            combined_key += key  # Combine keys by concatenation
        
        # Convert the combined key to a SHA‑512 hash (hexadecimal string)
        self.secret_key = hashlib.sha512(combined_key.encode()).hexdigest()

    def encode(self, plaintext: str) -> str:
        """
        Encode the given plaintext by first converting it to Base64, then applying an XOR‑based cipher
        using the combined hashed secret key. A checksum (sum of Base64 character ordinals modulo 256)
        is computed and prepended (in two-digit hex format) to the encrypted output.
        
        :param plaintext: The string to encode.
        :return: The encoded string in hexadecimal format.
        """
        if not isinstance(plaintext, str):
            raise ValueError("Input plaintext must be a string.")
        
        # Convert plaintext to its Base64 representation.
        base64_text = base64.b64encode(plaintext.encode()).decode('utf-8')
        
        # Compute a simple checksum from the Base64-encoded text.
        checksum = sum(ord(c) for c in base64_text) % 256
        checksum_hex = '{:02x}'.format(checksum)
        
        encoded_chars = []
        key = self.secret_key
        # XOR each character in the Base64 string with the corresponding character from the hashed key.
        for i, char in enumerate(base64_text):
            result = ord(char)
            key_char = key[i % len(key)]
            result ^= ord(key_char)
            encoded_chars.append('{:02x}'.format(result))
        
        # Prepend the checksum to the encoded data.
        encoded_str = checksum_hex + ''.join(encoded_chars)
        return encoded_str

    def decode(self, encoded_str: str) -> str:
        """
        Decode the encoded string back to the original plaintext.
        This method extracts the checksum, reverses the XOR‑based encoding to recover the Base64 string,
        verifies the checksum, and then Base64‑decodes the result.
        
        :param encoded_str: The encoded string in hexadecimal format.
        :return: The original plaintext string.
        """
        if not isinstance(encoded_str, str):
            raise ValueError("Input encoded data must be a string.")
        if len(encoded_str) < 2 or len(encoded_str) % 2 != 0:
            raise ValueError("Encoded data is not valid.")
        
        # Extract the stored checksum (first two hex digits).
        stored_checksum_hex = encoded_str[:2]
        try:
            stored_checksum = int(stored_checksum_hex, 16)
        except ValueError:
            raise ValueError("Invalid checksum in encoded data.")
        
        encoded_data = encoded_str[2:]
        if len(encoded_data) % 2 != 0:
            raise ValueError("Encoded data length is invalid.")
        
        decoded_chars = []
        key = self.secret_key
        # Reverse the XOR operation for each pair of hex digits.
        for i in range(0, len(encoded_data), 2):
            hex_pair = encoded_data[i:i+2]
            try:
                value = int(hex_pair, 16)
            except ValueError:
                raise ValueError("Encoded data contains non-hex characters.")
            key_char = key[(i // 2) % len(key)]
            value ^= ord(key_char)
            decoded_chars.append(chr(value))
        
        # Reconstruct the Base64-encoded text.
        base64_text = ''.join(decoded_chars)
        # Verify checksum.
        computed_checksum = sum(ord(c) for c in base64_text) % 256
        if computed_checksum != stored_checksum:
            raise ValueError("Incorrect key or corrupted data.")
        
        try:
            # Convert the Base64 text back to the original plaintext.
            plaintext = base64.b64decode(base64_text).decode('utf-8')
        except Exception as e:
            raise ValueError("Base64 decoding failed: " + str(e))
        return plaintext

    def is_encoded(self, message: str) -> bool:
        """
        Detect if the provided message appears to be encoded using this scheme.
        Checks include validating the format (even length, valid hex characters) and
        attempting to decode using the current secret key.
        
        :param message: The message to test.
        :return: True if the message appears to be encoded; False otherwise.
        """
        if not isinstance(message, str) or len(message) < 2 or len(message) % 2 != 0:
            return False
        hex_digits = set("0123456789abcdefABCDEF")
        if any(c not in hex_digits for c in message):
            return False
        
        try:
            _ = self.decode(message)
            return True
        except Exception:
            return False

# Example usage:
if __name__ == "__main__":
    # No secret key is provided, so the default "KhaledKarman" will be used.
    encoder = SecureData()
    
    message = "Sensitive Data!"
    print("Original Message:", message)
    
    # Encode the message.
    encoded_message = encoder.encode(message)
    print("Encoded Message:", encoded_message)
    
    # Detect if the message is encoded.
    if encoder.is_encoded(encoded_message):
        print("The message appears to be encoded by this scheme.")
    else:
        print("The message does not appear to be encoded by this scheme.")
    
    try:
        # Decode the message.
        decoded_message = encoder.decode(encoded_message)
        print("Decoded Message:", decoded_message)
        if decoded_message == message:
            print("PASS: Decoded message matches original message.")
        else:
            print("FAIL: Decoded message does not match original message.")
    except ValueError as e:
        print("Decoding error:", e)
