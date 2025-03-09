import unittest

# Assuming SecureData class is defined above or imported.
# from secure_data_encoder import SecureData

class TestSecureDataComplicatedMessages(unittest.TestCase):
    def setUp(self):
        # Create encoder instances with default key and with multiple custom keys.
        self.encoder_default = SecureData()  # Will use "KhaledKarman" by default.
        self.encoder_custom = SecureData("complexKey1", "anotherSecret", "yetAnotherKey")

    def test_empty_message(self):
        message = ""
        for encoder in [self.encoder_default, self.encoder_custom]:
            encoded = encoder.encode(message)
            self.assertTrue(encoder.is_encoded(encoded), "Encoded message should be detected as encoded")
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, message)

    def test_simple_message(self):
        message = "Hello, World!"
        for encoder in [self.encoder_default, self.encoder_custom]:
            encoded = encoder.encode(message)
            self.assertTrue(encoder.is_encoded(encoded))
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, message)

    def test_multiline_and_special_characters(self):
        message = (
            "This is a complicated message with newlines,\n"
            "special characters: !@#$%^&*()_+[]{}|;:',.<>/?\n"
            "and even JSON-like content: {\"key\": \"value\", \"list\": [1, 2, 3]}\n"
            "Unicode: 😊🚀💻, 中文测试, العربية"
        )
        for encoder in [self.encoder_default, self.encoder_custom]:
            encoded = encoder.encode(message)
            self.assertTrue(encoder.is_encoded(encoded))
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, message)

    def test_long_message(self):
        # Construct a long message by repeating a sentence.
        message = "Long message " * 1000
        for encoder in [self.encoder_default, self.encoder_custom]:
            encoded = encoder.encode(message)
            self.assertTrue(encoder.is_encoded(encoded))
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, message)

    def test_json_like_message(self):
        message = (
            "{\"name\": \"John Doe\", \"age\": 30, "
            "\"languages\": [\"English\", \"中文\", \"Español\"], "
            "\"bio\": \"Lorem ipsum dolor sit amet, consectetur adipiscing elit.\"}"
        )
        for encoder in [self.encoder_default, self.encoder_custom]:
            encoded = encoder.encode(message)
            self.assertTrue(encoder.is_encoded(encoded))
            decoded = encoder.decode(encoded)
            self.assertEqual(decoded, message)

if __name__ == '__main__':
    unittest.main()
