"""
Unit tests for Caesar Cipher and Frequency Analysis Functions
Tests for p5_DaSilva_MatheusHenrique.py
"""

import unittest
from p5_DaSilva_MatheusHenrique import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):
    """Test cases for the caesar_cipher function"""
    
    def test_simple_shift_3(self):
        """Test basic encryption with shift of 3"""
        result = caesar_cipher("HELLO", 3)
        self.assertEqual(result, "KHOOR")
    
    def test_lowercase_shift(self):
        """Test that lowercase letters are preserved"""
        result = caesar_cipher("hello", 3)
        self.assertEqual(result, "khoor")
    
    def test_mixed_case(self):
        """Test mixed case letters"""
        result = caesar_cipher("Hello", 3)
        self.assertEqual(result, "Khoor")
    
    def test_with_spaces(self):
        """Test that spaces are preserved"""
        result = caesar_cipher("Hello World", 3)
        self.assertEqual(result, "Khoor Zruog")
    
    def test_with_punctuation(self):
        """Test that punctuation is preserved"""
        result = caesar_cipher("Hello, World!", 3)
        self.assertEqual(result, "Khoor, Zruog!")
    
    def test_wrap_around(self):
        """Test that Z wraps around to A"""
        result = caesar_cipher("XYZ", 3)
        self.assertEqual(result, "ABC")
    
    def test_lowercase_wrap_around(self):
        """Test that z wraps around to a"""
        result = caesar_cipher("xyz", 3)
        self.assertEqual(result, "abc")
    
    def test_shift_zero(self):
        """Test with shift of 0 (no change)"""
        result = caesar_cipher("Hello", 0)
        self.assertEqual(result, "Hello")
    
    def test_shift_26(self):
        """Test with shift of 26 (full cycle, should return same)"""
        result = caesar_cipher("Hello", 26)
        self.assertEqual(result, "Hello")
    
    def test_negative_shift(self):
        """Test with negative shift"""
        result = caesar_cipher("KHOOR", -3)
        self.assertEqual(result, "HELLO")
    
    def test_empty_string(self):
        """Test with empty string"""
        result = caesar_cipher("", 5)
        self.assertEqual(result, "")
    
    def test_numbers_preserved(self):
        """Test that numbers are preserved"""
        result = caesar_cipher("Hello123", 3)
        self.assertEqual(result, "Khoor123")


class TestCaesarDecipher(unittest.TestCase):
    """Test cases for the caesar_decipher function"""
    
    def test_simple_decryption(self):
        """Test basic decryption"""
        encrypted = caesar_cipher("HELLO", 3)
        decrypted = caesar_decipher(encrypted, 3)
        self.assertEqual(decrypted, "HELLO")
    
    def test_decrypt_message_with_spaces(self):
        """Test decryption of message with spaces"""
        original = "Hello World"
        encrypted = caesar_cipher(original, 5)
        decrypted = caesar_decipher(encrypted, 5)
        self.assertEqual(decrypted, original)
    
    def test_decrypt_message_with_punctuation(self):
        """Test decryption of message with punctuation"""
        original = "Hello, World!"
        encrypted = caesar_cipher(original, 7)
        decrypted = caesar_decipher(encrypted, 7)
        self.assertEqual(decrypted, original)
    
    def test_decrypt_lowercase(self):
        """Test decryption with lowercase letters"""
        original = "thequickbrownfox"
        encrypted = caesar_cipher(original, 13)
        decrypted = caesar_decipher(encrypted, 13)
        self.assertEqual(decrypted, original)
    
    def test_decrypt_large_shift(self):
        """Test decryption with large shift value"""
        original = "SECRET"
        encrypted = caesar_cipher(original, 100)
        decrypted = caesar_decipher(encrypted, 100)
        self.assertEqual(decrypted, original)


class TestLetterFrequency(unittest.TestCase):
    """Test cases for the letter_frequency function"""
    
    def test_simple_frequency(self):
        """Test basic frequency counting"""
        result = letter_frequency("AAA")
        self.assertEqual(result['A'], 3)
        self.assertEqual(result['B'], 0)
    
    def test_case_insensitive(self):
        """Test that frequency counting is case-insensitive"""
        result = letter_frequency("AaA")
        self.assertEqual(result['A'], 3)
    
    def test_frequency_ignores_spaces(self):
        """Test that spaces are ignored"""
        result = letter_frequency("A A A")
        self.assertEqual(result['A'], 3)
    
    def test_frequency_ignores_numbers(self):
        """Test that numbers are ignored"""
        result = letter_frequency("A1B2C3")
        self.assertEqual(result['A'], 1)
        self.assertEqual(result['B'], 1)
        self.assertEqual(result['C'], 1)
    
    def test_frequency_ignores_punctuation(self):
        """Test that punctuation is ignored"""
        result = letter_frequency("A, B! C?")
        self.assertEqual(result['A'], 1)
        self.assertEqual(result['B'], 1)
        self.assertEqual(result['C'], 1)
    
    def test_all_letters_initialized(self):
        """Test that all 26 letters are present in result"""
        result = letter_frequency("test")
        self.assertEqual(len(result), 26)
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.assertIn(letter, result)
    
    def test_empty_string(self):
        """Test frequency of empty string"""
        result = letter_frequency("")
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.assertEqual(result[letter], 0)
    
    def test_no_alphabetic_characters(self):
        """Test string with no alphabetic characters"""
        result = letter_frequency("123 !@# 456")
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.assertEqual(result[letter], 0)
    
    def test_pangram(self):
        """Test with a pangram (contains all letters)"""
        pangram = "The quick brown fox jumps over the lazy dog"
        result = letter_frequency(pangram)
        # Check that all letters have at least count of 1
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.assertGreaterEqual(result[letter], 1)
    
    def test_frequency_totals(self):
        """Test that frequency totals are correct"""
        text = "HELLO WORLD"
        result = letter_frequency(text)
        total = sum(result.values())
        # Total should be 10 (11 characters minus 1 space)
        self.assertEqual(total, 10)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple functions"""
    
    def test_encrypt_decrypt_cycle(self):
        """Test that encrypting then decrypting returns original"""
        original = "The Quick Brown Fox Jumps Over The Lazy Dog"
        shift = 15
        encrypted = caesar_cipher(original, shift)
        decrypted = caesar_decipher(encrypted, shift)
        self.assertEqual(decrypted, original)
    
    def test_frequency_after_encryption(self):
        """Test that letter frequency remains same after encryption"""
        original = "AABBCC"
        shift = 5
        encrypted = caesar_cipher(original, shift)
        
        freq_original = letter_frequency(original)
        freq_encrypted = letter_frequency(encrypted)
        
        # Total count should be same
        self.assertEqual(sum(freq_original.values()), sum(freq_encrypted.values()))
        # Encrypted letters should be shifted versions
        self.assertEqual(freq_encrypted['F'], freq_original['A'])  # A+5=F
        self.assertEqual(freq_encrypted['G'], freq_original['B'])  # B+5=G
        self.assertEqual(freq_encrypted['H'], freq_original['C'])  # C+5=H


if __name__ == '__main__':
    unittest.main()
