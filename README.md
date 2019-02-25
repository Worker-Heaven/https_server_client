# HTTPS server/client in Python
Simple https server/client

## openssl version
OpenSSL 1.0.2j-fips  26 Sep 2016

https://sourceforge.net/projects/openssl/

## Create server certificate:
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
common name: 'example.com'

## Create client certificate:
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt


## A few notes:
You can concatenate multiple client certificates into a single PEM file to authenticate different clients.
You can re-use the same cert and key on both the server and client. This way, you don’t need to generate a specific client certificate. However, any clients using that certificate will require the key, and will be able to impersonate the server. There’s also no way to distinguish between clients anymore.
You don’t need to setup your own Certificate Authority and sign client certificates. You can just generate them with the above mentioned openssl command and add them to the trusted certificates file. If you no longer trust the client, just remove the certificate from the file.
I’m not sure if the server verifies the client certificate’s expiration date.
