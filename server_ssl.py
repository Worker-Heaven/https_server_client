#########################################################
# The server and the client are using basic TLS handshake
#########################################################

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl

from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA
from Cryptodome import Random

listen_addr = '127.0.0.1'
listen_port = 8082
server_cert = './certs/server.crt'
server_key = './certs/server.key'

def decrypt_data(ciphertext):
    # NOTE: load server's private key & decrypt message with this private key
    dKey = RSA.importKey(open('./certs/server.key').read())
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15

    cipher = PKCS1_v1_5.new(dKey)
    message = cipher.decrypt(ciphertext, sentinel)

    digest = SHA.new(message[:-dsize]).digest()
    if digest==message[-dsize:]:                # Note how we DO NOT look for the sentinel
        print ("Encryption was correct.")
        print('message got', message[:-dsize])
        return message[:-dsize]
    else:
        print ("Encryption was not correct.")

    return ''


# NOTE: Configure the context with server's certificate and private key
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)

bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(5)

while True:
    print("Waiting for client")

    newsocket, fromaddr = bindsocket.accept()
    print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))

    conn = context.wrap_socket(newsocket, server_side=True)
    print("SSL established. Peer: {}".format(conn.getpeercert()))

    buf = b''  # Buffer to hold received client data
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            
            # NOTE: here extract ciphertext used on the client
            ciphertext = decrypt_data(data)

            # No more data from client. Show buffer and close connection.
            print("Received:", ciphertext)
            conn.send(ciphertext)
    finally:
        print("Closing connection")
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
