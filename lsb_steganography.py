from PIL import Image

class LSBSteganography:
    @staticmethod
    def encrypt():
        message = input("Enter the message you'd like to hide: ")  # get message from user

        # input validation
        while not message.replace(" ", "").isalpha():
            message = input("Message must contain only letters. No punctuation.\n")

        message = message.replace(" ", "_")  # replace spaces with underscores for encoding
        message_binary = ""  # variable to hold binary

        # convert message to binary
        for x in range(len(message)):
            message_binary += bin(ord(message[x]))[2:]

        # open image
        while True:
            try:
                image = Image.open(input("Enter the name of the image to encode (including extension): "))
                break
            except (FileNotFoundError, IOError):
                print("Error. Try again.\n")

        # set dimensions and load pixels
        width, height = image.size
        pixels = image.load()

        # count how far we are in message and set flag to break loop at the end
        message_counter = 0
        EOF = False

        # loop through image making adjustments
        for x in range(width):
            if EOF:
                break
            for y in range(height):
                if EOF:
                    break
                for z in range(3):
                    pixel_list = list(pixels[x, y])
                    if message_binary[message_counter] == "0":  # if number is zero, set pixel to nearest even number
                        pixel_list[z] -= pixel_list[z] % 2
                    elif message_binary[message_counter] == "1":  # if number is one, set pixel to nearest odd number
                        if pixel_list[z] % 2 == 0:
                            if pixel_list[z] == 0:
                                pixel_list[z] += 1
                            else:
                                pixel_list[z] -= 1
                    pixels[x, y] = tuple(pixel_list)
                    message_counter += 1
                    if message_counter == len(message_binary):  # break out of all loops once end of message is read
                        EOF = True
                        break

        # save the image
        new_name = input("What would you like to name the new image? (Excluding extension)")
        image.save(new_name + ".png")

    @staticmethod
    def decrypt():
        # open image
        while True:
            try:
                image = Image.open(input("Enter the name of the image to decode (including extension): "))
                break
            except (FileNotFoundError, IOError):
                print("Error. Try again.\n")

        # set dimensions and read pixels
        width, height = image.size
        pixels = image.load()

        # get message size
        message_size = input("How many characters would you like to read from the image?\n")
        while not message_size.isnumeric():
            message_size = input("Input must be a number.\n")

        # multiply size by seven
        message_size = int(message_size) * 7

        # set variables to hold message binary and converted plaintext
        message_binary = ""
        message_plaintext = ""

        # initialize counter to track message size and EOF flag to break once it's done
        counter = 0
        EOF = False

        # loop through image reading pixels
        for x in range(width):
            if EOF:
                break
            for y in range(height):
                if EOF:
                    break
                for z in range(3):
                    if pixels[x, y][z] % 2 == 0:  # if pixel is even, add a 0 to the binary message
                        message_binary += "0"
                    else:
                        message_binary += "1"  # if pixel is odd, add a 1 to the binary message
                    counter += 1
                    if counter == message_size:
                        EOF = True
                        break

        # variables to temporarily hold the individual binary numbers and count how many are being held
        bin_holder = ""
        bin_counter = 0

        # translate the message from binary back into text
        for x in range(len(message_binary)):
            bin_holder += message_binary[x]
            bin_counter += 1
            if bin_counter % 7 == 0:
                bin_holder = int(bin_holder, 2)  # convert to decimal
                message_plaintext += chr(bin_holder)  # convert to letter
                bin_holder = ""

        # encode the underscores back into spaces and output the plaintext message
        message_plaintext = message_plaintext.replace("_", " ")
        print(message_plaintext)
