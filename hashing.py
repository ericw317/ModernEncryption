from Crypto.Hash import MD4
import binascii

def ntlm_hash(plaintext):
    #  the current libraries have no NTLM hash function, so we are going to replicate the function on our own
    #  NTLM hashes are created by encoding the plaintext with utf-16LE, then hashing that with MD4
    hash_ntlm = MD4.new()  # creates MD4 hash object
    hash_ntlm.update(plaintext.encode('utf-16le'))  # encodes plaintext to utf-16le then hashes it using MD4
    return binascii.hexlify(hash_ntlm.digest()).decode()  # returns the hash

class Hashing:
    @staticmethod
    def ntlm_crack(hash_to_crack, wordlist):
        success = False  # flag to indicate whether crack was successful or not

        # open wordlist and read line by line
        with open(wordlist, "r", errors="ignore") as dictionary_list:
            for line in dictionary_list:
                word = line.strip()  # strip whitespace from lines and store the word
                print(f"\rAttempting: {word}", end="")  # Output which word we are currently checking
                if ntlm_hash(word) == hash_to_crack:  # hash the word and check if the hashes match
                    print(f"\nCrack successful: {word}\n")
                    success = True
                    break

        if not success:
            print("\nHash crack failed.\n")
