#########################################################
# The server and the client are using basic TLS handshake
#########################################################

import socket
import ssl

host_addr = '127.0.0.1'
host_port = 8082
server_sni_hostname = 'example.com'
client_cert = 'client.crt'
client_key = 'client.key'

# NOTE: Get server's certificate in order to validate it
server_cert = ssl.get_server_certificate((host_addr, host_port))
print('server certificate: {}'.format(server_cert))

# NOTE: Establish the SSL/TLS connection between the server and the client
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cadata=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print("SSL established. Peer: {}".format(conn.getpeercert()))
print("Sending: 'Hello, world!")
conn.send(b"Hello, world!")
print("Closing connection")
conn.close()