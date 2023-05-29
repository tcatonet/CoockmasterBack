# I don't know what these files are, but OpenSSL complains if they do not exist...
# mkdir demoCA
# touch demoCA/index.txt demoCA/index.txt.attr
# echo '01' > demoCA/serial

# Create a self-signed certificate and private key.
openssl req -x509 -nodes -newkey rsa:4096 -keyout ca.key -new -out ca.crt
# Create a certificate signing request for server, "localhost", and a private key.
openssl req -nodes -newkey rsa:4096 -keyout localhost.key -new -out localhost.csr
# Sign the certificate request.
openssl ca -keyfile ca.key -cert ca.crt -in localhost.csr -outdir . -out localhost.crt
cat localhost.crt localhost.key > localhost.pem