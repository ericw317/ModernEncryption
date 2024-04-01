from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from AES import AESCipher
from lsb_steganography import LSBSteganography
from hashing import Hashing
import os

while True:
    encrypt = False
    decrypt = False
    hashing = False

    selection = input("Selection an option\n"
                      "1) Encryption\n"
                      "2) Decryption\n"
                      "3) Hash Cracking\n"
                      "0) Exit\n")

    while not selection.isnumeric() or int(selection) > 3 or int(selection) < 0:
        selection = input("Input must be a number between 0-3. Try again.\n")

    if int(selection) == 0:
        break
    elif int(selection) == 1:
        encrypt = True
    elif int(selection) == 2:
        decrypt = True
    elif int(selection) == 3:
        hashing = True

    if encrypt:
        selection = input("Selection an encryption algorithm.\n"
                          "1) AES-256\n"
                          "2) LSB Steganography\n"
                          "0) Exit\n")
        while not selection.isnumeric() or int(selection) > 2 or int(selection) < 0:
            selection = input("Input must be a number between 0-2. Try again.\n")

        if int(selection) == 0:
            break
        elif int(selection) == 1:
            selection = input("Do you want to encrypt a plaintext message or a file?\n"
                              "1) Plaintext message\n"
                              "2) File\n")
            while not selection.isnumeric() or int(selection) > 2 or int(selection) < 1:
                input("Input must be a number between 1-2: ")
            if int(selection) == 1:
                AESCipher.encrypt256("text")
            elif int(selection) == 2:
                AESCipher.encrypt256("file")
        elif int(selection) == 2:
            LSBSteganography.encrypt()

    if decrypt:
        selection = input("Selection an encryption algorithm.\n"
                          "1) AES-256\n"
                          "2) LSB Steganography\n"
                          "0) Exit\n")
        while not selection.isnumeric() or int(selection) > 2 or int(selection) < 0:
            selection = input("Input must be a number between 0-2. Try again.\n")

        if int(selection) == 0:
            break
        elif int(selection) == 1:
            selection = input("Do you want to decrypt a ciphertext message or a file?\n"
                              "1) Ciphertext message\n"
                              "2) File\n")
            while not selection.isnumeric() or int(selection) > 3 or int(selection) < 1:
                input("Input must be a number between 1-2: ")
            if int(selection) == 1:
                AESCipher.decrypt256("text")
            elif int(selection) == 2:
                AESCipher.decrypt256("file")
        elif int(selection) == 2:
            LSBSteganography.decrypt()

    if hashing:
        selection = input("Which hashing algorithm do you want to crack?\n"
                          "1) NTLM\n"
                          "0) Exit\n")

        # input validation
        while not selection.isnumeric() or int(selection) < 0 or int(selection) > 1:
            selection = input("Input must be a number between 0-1. Try again.\n")

        if int(selection) == 1:
            # obtain values for hash and wordlist
            hash_to_crack = input("Enter the hash you would like to crack: ").lower()
            wordlist = input("Enter the path to the wordlist you will be using: ")
            # input validation
            while not os.path.exists(wordlist):
                wordlist = input("File not found. Try again: ")
            Hashing.ntlm_crack(hash_to_crack, wordlist)
        elif int(selection) == 0:
            break
