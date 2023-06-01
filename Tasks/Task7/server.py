from Crypto.Cipher import AES
import binascii
import os
import sys
import asyncio
import subprocess


# Create secret key for encryption
if not os.path.exists("secret-key.bin"):
    with open("secret-key.bin", "wb") as keyfile:
        keyfile.write(os.urandom(16))

with open("secret-key.bin", "rb") as keyfile:
    key = keyfile.read()

# Exception Class: Throw if there is an error in the Padding of a message
class PaddingError(Exception):
    pass

# Pad the message according to PKCS#7
def pad_message(msg):
    val = 16 - (len(msg) % 16)
    return msg + "{}".format(chr(val)).encode()*val

# Unpad the message according to PKCS#7, if there is an invalid padding throw an error
def unpad_message(msg):
    val = msg[-1]
    if not all(x==val for x in msg[-val:]):
        raise PaddingError()
    msg = msg[:-val]
    return msg

# Lambda Function to transform bytes into a hex string
mhex = lambda x: binascii.hexlify(x).decode()

# Function that gets called for every new connection
async def handle_request(reader, writer):
    print("New connection")
    
    # Create IV and Pad-then-Encrypt Flag with AES in CBC Mode
    iv = os.urandom(16)
    secret_msg = b"This is your flag: " + subprocess.check_output(["/bin/flag", "7"])
    padded_msg = pad_message(secret_msg)

    my_aes = AES.new(key, AES.MODE_CBC, iv)
    crypted_msg = my_aes.encrypt(padded_msg)

    # Send IV and encrypted Message
    writer.write("I have an encrypted message for you:\n{} (IV was {})\n\n".format(mhex(crypted_msg), mhex(iv)).encode())
    writer.write(b"Do you also have an encrypted message for me?!\nIf so, please enter IV and the message seperated by newlines now! (plz give hexlified stuff)\n")
    await writer.drain()

    # Wait for response (IV and Message to decrypt)
    iv = await reader.readline()
    msg = await reader.readline()

    try:
        iv = binascii.unhexlify(iv.strip())
        msg = binascii.unhexlify(msg.strip())
        
        # Decrypt message
        my_aes = AES.new(key, AES.MODE_CBC, iv)
        decrypted = my_aes.decrypt(msg)
        print(binascii.hexlify(decrypted)) # Print it, for debugging purposes
        # Try to unpad it
        unpadded = unpad_message(decrypted)
        # If there was no error, send OK! back to client
        writer.write(b"OK!\n")
        
    except binascii.Error:
        # if the message of the client was not in hex
        writer.write(b"Couldn't unhexlify your stuff... :(\n")        
    except PaddingError:
        # if there was a padding error with given message
        writer.write(b"Bad padding :(\n")
    except ValueError as e:
        writer.write("Some other error: {}\n".format(e).encode())

    # Close server
    await writer.drain()
    writer.close()

# Start server
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_request, "0.0.0.0", 7007, loop=loop)
    server = loop.run_until_complete(coro)

    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Quitting server")
