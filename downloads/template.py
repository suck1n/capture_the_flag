#!/usr/bin/env python3
import binascii
import hashlib
import select
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SERVER = ("10.10.30.50", 1024)

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca18217c32905e462e36ce3be39e772c180e86039b2783a2ec07a28fb5c55df06f4c52c9de2bcbf6955817183995497cea956ae515d2261898fa051015728e5a8aacaa68ffffffffffffffff
g = 0x2
MAC_LENGTH = 32


def kdf_aes(s):
    """Derive a key suitable for AES encryption/decryption from the negotiated DH secret"""
    h = hashlib.sha512()
    h.update("{}".format(s).encode())
    return h.digest()[:16]

def encrypt(message, key, iv):
    """Computes the message's MAC, then encrypts both with AES-CBC according to the task description"""
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

    return iv + cipher.encrypt(pad(message, block_size=16))

def decrypt(message, key):
    """Does the inverse of encrypt(message, key). Raises ValueError if the message was manipulated"""
    iv, message = message[:16], message[16:]
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    message = cipher.decrypt(message)

    return iv, unpad(message, block_size=16)

if __name__ == "__main__":
    with socket.socket() as side_a, socket.socket() as side_b:
        print("Connecting to party A")
        side_a.connect(SERVER)
        side_a.send(b"A\n")

        print("Connecting to party B")
        side_b.connect(SERVER)
        side_b.send(b"B\n")

        print("Connected successfully")
        # This forwards all messages, you can delete this and use the commented-out
        # hints below (or just adjust this code if you prefer working with raw sockets)
        while True:
            sockets_with_data, _, _ = select.select([side_a, side_b], [], [])

            if side_a in sockets_with_data:
                buf = side_a.recv(1024)
                if buf == b"":
                    print("Party A closed connection")
                    break
                print("A -> B: {}".format(buf.strip().decode()))
                side_b.sendall(buf)

            if side_b in sockets_with_data:
                buf = side_b.recv(1024)
                if buf == b"":
                    print("Party B closed the connection")
                    break
                print("B -> A: {}".format(buf.strip().decode()))
                side_a.sendall(buf)

        # You may find these hints useful:
        #
        # Convert socket to file like class to get a readline method
        #    side_a = side_a.makefile("rw")
        #    side_b = side_b.makefile("rw")
        #
        # To read a message from party A, you can then use
        #    message = side_a.readline().strip()
        # and to forward it to party B
        #    side_b.write("{}\n".format(message))
        #    side_b.flush()