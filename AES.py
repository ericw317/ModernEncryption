from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import tkinter
from tkinter import filedialog
from tkinter import messagebox

def file_destination():
    messagebox.showinfo("File Selection", "Select the file you'd like to encrypt")
    file = filedialog.askopenfilename()
    messagebox.showinfo("Save Directory", "Select the directory to save the encrypted file to.")
    directory = filedialog.askdirectory()

    return [file, directory]

def read_file_bytes(file):
    with open(file, "rb") as fi:
        byte_data = fi.read()

    return byte_data

class AESCipher:
    @staticmethod
    def encrypt256(text_or_file):
        # generate key and AES object
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_CFB)

        if text_or_file == "text":
            # ask user to input message
            message = input("Enter the message you want to encrypt: ")

            # encrypt message
            ciphertext = cipher.encrypt(message.encode('utf-8'))

            # Output the key and ciphertext in hex
            print("Key: " + cipher.iv.hex() + key.hex())
            print("Ciphertext: " + ciphertext.hex())
        elif text_or_file == "file":
            # get file to encrypt and output directory
            user_inputs = file_destination()
            file, output_dir = user_inputs[0], user_inputs[1]

            # read file data and encrypt it
            file_data = read_file_bytes(file)
            encrypted_data = cipher.encrypt(file_data)

            # get name for output file and write the encrypted data to a file
            output_file_name = input("What would you like to call the encrypted file?\n")
            with open(output_dir + "/" + output_file_name, "wb") as fo:
                fo.write(encrypted_data)

            # ask user how they want to receive the key
            key_method = input("Do you want your key given to you in hex or output to a file?\n"
                               "1) Given in hex\n"
                               "2) Output to a file\n")
            # input validation
            while not key_method.isnumeric() or int(key_method) < 1 or int(key_method) > 2:
                key_method = input("Input must be a number between 1-2.")

            # output the key
            if int(key_method) == 1:
                print("Key: " + cipher.iv.hex() + key.hex())
            elif int(key_method) == 2:
                messagebox.showinfo("Save Directory", "Select where to save key file to.")
                key_dir = filedialog.askdirectory()
                key_name = input("Name for key file?\n")

                with open(key_dir + "/" + key_name, "wb") as fo:
                    fo.write(cipher.iv + key)

    @staticmethod
    def decrypt256(text_or_file):
        if text_or_file == "text":
            # retrieve key and ciphertext
            key = input("Enter the key: ")
            ciphertext = input("Enter the ciphertext: ")

            # convert key and ciphertext back into bytes
            key = bytes.fromhex(key)
            ciphertext = bytes.fromhex(ciphertext)

            # decrypt the ciphertext
            cipher = AES.new(key[16:], AES.MODE_CFB, iv=key[:16])
            plaintext = cipher.decrypt(ciphertext)

            # output plaintext
            print(plaintext.decode('utf-8'))
        elif text_or_file == "file":
            # get encrypted file, and read the encrypted data
            messagebox.showinfo("Select File", "Select the encrypted file.")
            encrypted_file = filedialog.askopenfilename()
            with open(encrypted_file, "rb") as fi:
                encrypted_data = fi.read()

            # ask for how they are entering the key
            file_or_hex = input("Are you using a key file or a hex key?\n"
                                "1) Hex key\n"
                                "2) Key file\n")
            # input validation
            while not file_or_hex.isnumeric() or int(file_or_hex) < 1 or int(file_or_hex) > 2:
                file_or_hex = input("Input must be a number between 1-2: ")

            if int(file_or_hex) == 1:
                # convert hex to bytes and store the iv and key
                hex_key = input("Enter the key: ")
                key_bytes = bytes.fromhex(hex_key)
                iv = key_bytes[:16]
                key = key_bytes[16:]

                # ask for output destination and name for decrypted file
                messagebox.showinfo("Output Destination",
                                    "Select the directory you want to save the decrypted file to")
                output_destination = filedialog.askdirectory()
                output_name = input("Name for decrypted file?\n")

                # decrypt the data
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                decrypted_data = cipher.decrypt(encrypted_data)

                # write the decrypted data to a file
                with open(output_destination + "/" + output_name, "wb") as fo:
                    fo.write(decrypted_data)

            elif int(file_or_hex) == 2:
                # get the key file and read the iv and key bytes from it
                messagebox.showinfo("Select Key", "Select the key file.")
                key_file = filedialog.askopenfilename()
                with open(key_file, "rb") as fi:
                    iv = fi.read(16)
                    key = fi.read()

                # decrypt the data
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                decrypted_data = cipher.decrypt(encrypted_data)

                # get destination and name for output file
                messagebox.showinfo("Output destination", "Where would you like to output decrypted file.")
                output_destination = filedialog.askdirectory()
                output_name = input("Name for the decrypted file?\n")

                # write the decrypted data to a file
                with open(output_destination + "/" + output_name, "wb") as fo:
                    fo.write(decrypted_data)

