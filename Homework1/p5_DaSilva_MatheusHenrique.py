"""
Caesar Cipher Program with Frequency Analysis
Matheus Henrique da Silva

This program provides functionality to encrypt and decrypt text using a Caesar cipher,
and analyze letter frequencies in the text.
"""


def caesar_cipher(text, shift):
    """
    Encrypts text using a Caesar cipher by shifting letters by a given amount.
    
    Args:
        text (str): The text to encrypt
        shift (int): The number of positions to shift each letter
        
    Returns:
        str: The encrypted text with preserved spaces and casing
    """
    result = ""
    
    for char in text:
        if char.isupper():
            # Shift uppercase letters
            shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result += shifted
        elif char.islower():
            # Shift lowercase letters
            shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result += shifted
        else:
            # Preserve non-alphabetic characters (spaces, punctuation, etc.)
            result += char
    
    return result


def caesar_decipher(ciphertext, shift):
    """
    Decrypts a Caesar-encrypted string by reversing the shift.
    
    Args:
        ciphertext (str): The encrypted text
        shift (int): The shift value used during encryption
        
    Returns:
        str: The decrypted original text
    """
    # To decrypt, we reverse the shift by subtracting it
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    """
    Counts the frequency of each letter (A-Z) in the text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: A dictionary with letters as keys and their counts as values,
              sorted alphabetically
    """
    frequency = {}
    
    # Initialize all letters with 0 count
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        frequency[letter] = 0
    
    # Count occurrences of each letter (case-insensitive, alphabetic only)
    for char in text:
        if char.isalpha():
            upper_char = char.upper()
            frequency[upper_char] += 1
    
    return frequency


def print_frequency_table(frequency):
    """
    Prints the letter frequency data in a formatted table.
    
    Args:
        frequency (dict): Dictionary with letter frequencies
    """
    total_letters = sum(frequency.values())
    
    if total_letters == 0:
        print("No alphabetic characters found in the text.")
        return
    
    print("\n" + "="*50)
    print("LETTER FREQUENCY ANALYSIS")
    print("="*50)
    print(f"{'Letter':<8} {'Count':<8} {'Percentage':<12}")
    print("-"*50)
    
    for letter in sorted(frequency.keys()):
        count = frequency[letter]
        percentage = (count / total_letters) * 100
        print(f"{letter:<8} {count:<8} {percentage:>6.2f}%")
    
    print("-"*50)
    print(f"{'Total':<8} {total_letters:<8}")
    print("="*50)


def main():
    """
    Main function that runs the interactive Caesar cipher program.
    Displays a menu allowing the user to encrypt/decrypt text and analyze frequencies.
    """
    print("\n" + "="*60)
    print("CAESAR CIPHER & FREQUENCY ANALYSIS PROGRAM")
    print("="*60)
    
    while True:
        print("\nMENU:")
        print("1. Encrypt text (Caesar cipher)")
        print("2. Decrypt text (Caesar cipher)")
        print("3. Analyze letter frequency")
        print("4. Full analysis (encrypt, frequency, decrypt)")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            text = input("Enter the text to encrypt: ")
            try:
                shift = int(input("Enter the shift value (0-25): "))
                encrypted = caesar_cipher(text, shift)
                print(f"\nOriginal text: {text}")
                print(f"Shift value: {shift}")
                print(f"Encrypted text: {encrypted}")
            except ValueError:
                print("ERROR: Shift value must be an integer.")
        
        elif choice == '2':
            text = input("Enter the text to decrypt: ")
            try:
                shift = int(input("Enter the shift value used for encryption (0-25): "))
                decrypted = caesar_decipher(text, shift)
                print(f"\nEncrypted text: {text}")
                print(f"Shift value: {shift}")
                print(f"Decrypted text: {decrypted}")
            except ValueError:
                print("ERROR: Shift value must be an integer.")
        
        elif choice == '3':
            text = input("Enter the text to analyze: ")
            frequency = letter_frequency(text)
            print_frequency_table(frequency)
        
        elif choice == '4':
            text = input("Enter the text to analyze: ")
            try:
                shift = int(input("Enter the shift value (0-25): "))
                
                # Encryption
                encrypted = caesar_cipher(text, shift)
                print(f"\n{'='*60}")
                print(f"Original text: {text}")
                print(f"Shift value: {shift}")
                print(f"Encrypted text: {encrypted}")
                
                # Frequency analysis
                frequency = letter_frequency(text)
                print_frequency_table(frequency)
                
                # Decryption
                decrypted = caesar_decipher(encrypted, shift)
                print(f"Decrypted text: {decrypted}")
                print(f"{'='*60}")
                
            except ValueError:
                print("ERROR: Shift value must be an integer.")
        
        elif choice == '5':
            print("\nThank you for using the Caesar Cipher Program. Goodbye!")
            break
        
        else:
            print("ERROR: Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
