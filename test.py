from Crypto.PublicKey import RSA
RSA_ = RSA.generate(2048)
print RSA_.publickey().exportKey()
print RSA_.exportKey()
