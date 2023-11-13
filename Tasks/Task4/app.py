#!/usr/bin/env python3

import asyncio
import binascii
import hashlib
import hmac
import os
import secrets
import subprocess
import time

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

# Two prime numbers for generating Keys
# You can generate parameters yourself with `openssl dhparam`, but these ones are from RFC3526
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca18217c32905e462e36ce3be39e772c180e86039b2783a2ec07a28fb5c55df06f4c52c9de2bcbf6955817183995497cea956ae515d2261898fa051015728e5a8aacaa68ffffffffffffffff
g = 0x2

# Create Auth-Key to create MAC (Message-Authentication-Codes)
if os.path.exists("auth-key.bin"):
    with open("auth-key.bin", "rb") as keyfile:
        auth_key = keyfile.read()
else:
    auth_key = os.urandom(32)
    with open("auth-key.bin", "wb") as keyfile:
        keyfile.write(auth_key)

MAC_LENGTH = 32
def compute_mac(message):
    """Generate a MAC (Message-Authentication-Codes) - It protects messages against manipulation"""
    return hmac.new(auth_key, message, digestmod="sha256").digest()

def generate_aes_key(secret):
    """Derive a key suitable for AES encryption/decryption from the negotiated DH secret"""
    h = hashlib.sha512()
    h.update(f"{secret}".encode())
    return h.digest()[:16]

def encrypt(message, key):
    """Computes the message's MAC, then encrypts the result from pad(message + mac) with AES-CBC"""
    iv = os.urandom(16)
    mac = compute_mac(message)
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    return iv + cipher.encrypt(pad(message + mac, block_size=16))

def decrypt(message, key):
    """Does the inverse of encrypt(message, key). Raises ValueError if the message was manipulated"""
    iv, message = message[:16], message[16:]
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    message = cipher.decrypt(message)
    # We unpad manually to avoid a padding oracle here
    unpadded = message[:-message[-1]]
    expected_mac = compute_mac(unpadded[:-MAC_LENGTH])
    if expected_mac != unpadded[-MAC_LENGTH:]:
        raise ValueError("Message tampering detected")
    return unpad(message, block_size=16)[:-MAC_LENGTH] # Finally raise ValueError on bad padding, _after_ the MAC check.

# The messages that each side will send (and expect)
PROTOCOL_A = [
    b"Hi, I'm Alice!",
    b"Would you like a flag?",
    lambda flag: b"Here's the first half of your flag: " + flag[:len(flag) // 2],
    lambda flag: b"Here's the rest: " + flag[len(flag) // 2:],
]
PROTOCOL_A_FAILURE = b"Someone's listening, I'm sure of it! See you tomorrow!\n"

PROTOCOL_B = [
    b"Hi Alice, I'm Bob!",
    b"Yes, please!",
    b"Thank you! What about the rest?",
    b"Thanks!"
]
PROTOCOL_B_FAILURE = b"I think they're spying on us, let's continue this conversation tomorrow!\n"

# Gets called once there is a Client Connection
async def handle_request(reader, writer):
    connection_id = f"{time.strftime('%FT%T%z')}-{os.urandom(4).hex()}"
    print(f"New connection: {connection_id}")
	# Wait for Client Message, must be either "A" or "B"
    side = (await reader.readline()).strip().decode().upper()
    print(f"{connection_id}: Requesting side {side}")

    if side == "A":
        connection_id += "-A"
        print(f"{connection_id}: Side A")

	# Create Secret Diffie Hellman Key for side A
        a = secrets.randbits(128) # This is arbitrary, and may not be secure
        print(f"{connection_id}: DH secret a is {a}")
	# Calculate Public Diffie Hellman Key
        A = pow(g, a, p)
	# Send it to the Client
        writer.write(f"{A}\n".encode())
        await writer.drain()

	# Wait for the Client Public Key
        B = int((await reader.readline()).strip().decode())
        # Public Key must be between 1 and (p - 1) otherwise its not secure enough
        if not 1 < B < p - 1: # Compare e.g. RFC 6989, Sections 2.1 and 5
            writer.write(b"Oh no, that's an insecure public key!\n")
            await writer.drain()
            writer.close()
            return


	# Calculate the shared secret 's'
        s = pow(B, a, p)
        print(f"{connection_id}: Shared DH secret s is {s}")

	# Generate a AES Key from the shared secret
        key = generate_aes_key(s)
        print(f"{connection_id}: AES key is {key.hex()}")

	# Get the flag
        flag = subprocess.check_output(["/bin/flag", "4"]).strip()

	# Now go through all the message A has to send/receive
        for message in PROTOCOL_A:
	# If its not bytes, its a lambda function. Call it to get part of the flag
            if not isinstance(message, bytes):
                message = message(flag) # This message contains part of the flag
			
            # Sends the encrypted Message as Hex-Representation to the Client
            print(f"{connection_id}: Sending raw message {message.decode()!r}")
            encrypted = binascii.hexlify(encrypt(message, key))
            print(f"{connection_id}: Sending encrypted message {encrypted.decode()} | {binascii.unhexlify(encrypted)}")
            writer.write(encrypted + b"\n")
            await writer.drain()

	    # Wait for Client Response
            response = (await reader.readline()).strip()
            print(f"{connection_id}: Got encrypted response {response.decode()}")
            try:
		# Try to decrypt it
                decrypted = decrypt(binascii.unhexlify(response), key)
            except ValueError:
                print(f"{connection_id}: Tampering detected (bad padding or MAC)")
                writer.write(PROTOCOL_A_FAILURE)
                await writer.drain()
                writer.close()
                return
            print(f"{connection_id}: Got raw response {decrypted.decode()!r}")

    elif side == "B":
        connection_id += "-B"
        print(f"{connection_id}: Side B")

	# Create Secret Diffie Hellman Key for side A
        b = secrets.randbits(128) # This is arbitrary, and may not be secure
        print(f"{connection_id}: DH secret b is {b}")
	# Calculate Public Diffie Hellman Key
        B = pow(g, b, p)
	# Send it to the Client
        writer.write(f"{B}\n".encode())
        await writer.drain()

	# Wait for the Client Public Key
        A = int((await reader.readline()).strip().decode())
        # Public Key must be between 1 and (p - 1) otherwise its not secure enough
        if not 1 < A < p - 1: # Compare e.g. RFC 6989, Sections 2.1 and 5
            writer.write(b"Oh no, that's an insecure public key!\n")
            await writer.drain()
            writer.close()
            return
			
		# Calculate the shared secret 's'
        s = pow(A, b, p)
        print(f"{connection_id}: Shared DH secret s is {s}")

		# Generate a AES Key from the shared secret
        key = generate_aes_key(s)
        print(f"{connection_id}: AES key is {key.hex()}")

		# Now go through all the message B has to send/receive
        for index, message in enumerate(PROTOCOL_B):
            assert isinstance(message, bytes), "Party B doesn't have a flag"

			# Wait for Client Message
            from_a = (await reader.readline()).strip()
            print(f"{connection_id}: Got encrypted message {from_a.decode()}")
            try:
                decrypted = decrypt(binascii.unhexlify(from_a), key)
            except ValueError:
                print(f"{connection_id}: Tampering detected (bad padding or MAC)")
                writer.write(PROTOCOL_B_FAILURE)
                await writer.drain()
                writer.close()
                return
            print(f"{connection_id}: Got raw message {decrypted.decode()!r}")

            # Sends the encrypted Message as Hex-Representation to the Client
            print(f"{connection_id}: Sending raw message {message.decode()!r}")
            encrypted = binascii.hexlify(encrypt(message, key))
            print(f"{connection_id}: Sending encrypted message {encrypted.decode()}")
            writer.write(encrypted + b"\n")
            await writer.drain()

    else:
        writer.write(b"We only have two parties (A and B), sorry...\n")
        await writer.drain()
    print(f"{connection_id}: Connection done.")
    writer.close()

if __name__ == "__main__":
	# Starts the Server
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_request, "0.0.0.0", 5004)
    server = loop.run_until_complete(coro)

    print("Serving on {}".format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Quitting server")
