# HTTPS server/client in Python 3.6
Simple https server/client which validate server's certificate and do rsa encryption using server's public key on the client side and decrypt data on server side using server's private key

## openssl version
OpenSSL 1.0.2j-fips  26 Sep 2016

https://sourceforge.net/projects/openssl/

## Configure personal CA:
$ openssl genrsa -out ca.key 2048
$ openssl req -new -x509 -key ca.key -out ca.crt

## Create server certificate:
$ openssl genrsa -out example.org.key 2048 (keygen)
$ openssl req -new -key example.org.key -out example.org.csr (csr gen)

## Sign the certificate
$ openssl x509 -req -in example.org.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out example.org.crt

## How to install Cryptodome
please reference this article

https://pycryptodome.readthedocs.io/en/latest/src/installation.html

## How to install openssl 
https://sourceforge.net/projects/openssl/

Released /openssl-1.0.2j-fips-x86_64/openssl-1.0.2j-fips-x86_64.zip
