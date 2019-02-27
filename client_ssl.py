#########################################################
# The server and the client are using basic TLS handshake
#########################################################

import socket
import ssl
from OpenSSL import crypto

from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA
from Cryptodome import Random

# NOTE: server info
host_addr = '127.0.0.1'
host_port = 8082
server_sni_hostname = 'example.com'
ca_cert = './certs/ca.crt'

# NOTE: configure ssl context to detect the right server
context = ssl.SSLContext()
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations(ca_cert)

# NOTE: establish the tls/ssl connection
conn = context.wrap_socket(socket.socket(socket.AF_INET),
                           server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))

# NOTE: Get server's certificate
# sslSocket.getpeercert return DER certificate
# but we are using PEM certificate here, so need to convert it
server_cert = ssl.DER_cert_to_PEM_cert(conn.getpeercert(True))
print('server\'s certificate: \n', server_cert)

#cert is the encrypted certificate int this format -----BEGIN -----END 
x509 = crypto.load_certificate(crypto.FILETYPE_PEM, server_cert)
public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, x509.get_pubkey())
print('public key', public_key)

# NOTE: cipher session key will be used
message = b'To be encrypted'
print('cipher session text', message)

h = SHA.new(message)

# NOTE: RSA encryption with server's public key
key = RSA.importKey(public_key)
cipher = PKCS1_v1_5.new(key)
ciphertext = cipher.encrypt(message+h.digest())

print('ciphertext', ciphertext)

conn.send(ciphertext)

data = conn.recv(4096)
print('received data', data)

conn.close()
