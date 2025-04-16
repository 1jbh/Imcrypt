from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import hashlib
import os, sys

def imageToKey(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())
    pixel_bytes = b''.join(bytes(pixel) for pixel in pixels)
    key = hashlib.sha256(pixel_bytes).digest()
    return key

def encrypt(image, infile, outfile):
    key = imageToKey(image)

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(infile, 'rb') as file:
        plaintext = file.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(outfile, 'wb')as file:
        file.write(cipher.iv + ciphertext)


def decrypt(image, infile, outfile):
    key = imageToKey(image)

    with open(infile, 'rb') as file:
        iv = file.read(16)
        ciphertext = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    except ValueError:
        print("Incorrect image to decrypt this file. Quitting...")
        quit()
        
    with open(outfile, 'wb') as file:
        file.write(plaintext)

    return 0

def main():
    arg_length = len(sys.argv)

    if arg_length != 5:
        print("Error- Improper amount of arguments.")
        print("\nUsage:")
        print("python main.py encrypt image.png file.txt secret.imc")
        print("python main.py decrypt image.png secret.imc file_out.txt")
        exit()

    operation, image, infile, outfile = sys.argv[1:]
    match operation:
        case "encrypt":
            encrypt(image, infile, outfile)
        case "decrypt":
            decrypt(image, infile, outfile)

if __name__ == "__main__":
    main()