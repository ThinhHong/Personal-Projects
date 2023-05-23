import base64
import maskpass
import bcrypt
import mysql.connector
import configparser
import sys
import math
from mysql.connector import connect, errorcode, Error

config = configparser.ConfigParser()
try:
    config.read('configlol.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

my_host = config['userID']['host']
my_username = config['userID']['username']
my_password = config['userID']['password']
my_database = config['userID']['database']


class user_vertification:

    def __init__(self, users: dict={}) -> None:
        self.users = users

    def add_user(self) -> None:
        username = input("Enter Your Username : ")
        #maskpass allows for input from user privately 
        pwd = maskpass.askpass()
        pwd2 = maskpass.askpass()
        while pwd != pwd2:
            print("Passwords do not match")
            pwd = maskpass.askpass()
            pwd2 = maskpass.askpass()

        self.dict[username] = pwd



def encode_pass(password: str) -> str:
    pwd = maskpass.askpass()
    encode = base64.b64encode(pwd.encode("utf-8"))
    print("str-byte : ", encode)
    return encode

def decode_pass(coded: str) -> str:
    decode = base64.b64decode(coded).decode("utf-8")
    print("byte-str : ", decode)
    return decode

def encrypte(string: str, foward: int) -> str:
    #If foward is 13, this creates a rot13 encryption algorithm
    encrypted = ""
    for i in range(len(string)):
        char = string[i]

        if (char.islower()):
            uni = ord(char) + foward - 97
            new = chr((uni % 26) + 97)
            encrypted += new

        else:
            uni = ord(char) + foward -65
            new = chr((uni % 26) + 65)
            encrypted += new
    
    return encrypted

def hack(string :str) -> None:
    for i in range(26):
        result = ""
        for j in range(len(string)):
            char = string[j]
            if (char.islower()):
                uni = ord(char) + i - 97
                new = chr((uni) % 26 + 97)
                result += new
            else:
                uni = ord(char) + i -65
                new = chr((uni) % 26 + 65)
                result += new

        print(f"Encryption key: {i} decrypted result: {result}")
                
           
def transposition_encryption(string: str, length: int) -> str:
    number_rows = math.ceil(len(string)/length)
    list = []
    for i in range(number_rows):
        row = []
        for j in range(i,len(string),length):
            row.append(string[i])
        list.append(row)

    
def transposition_encryption(string: str, length: int) -> str:
    b = []
    row = []
    for i in range(0,length):
        row.append(string[i])
    b.append[row]
# Accept user password input
pwd = maskpass.askpass()
 
# Encoding the string
encode = base64.b64encode(pwd.encode("utf-8"))
print("str-byte : ", encode)
 
# Decoding the string
decode = base64.b64decode(encode).decode("utf-8")
print("byte-str : ", decode)

password = str(input("input password: ")).encode('utf-8')

hashed = bcrypt.hashpw(password, bcrypt.gensalt(10)) 

check = str(input("check password: ")).encode('utf-8')

if bcrypt.checkpw(check, hashed):
    print("Login is successful")
else:
    print("Incorrect password entered")

try:
      with connect(
            host= my_host,
            user= my_username,
            password= my_password,
            database = my_database,
      ) as connection:
            print(f"Connection {connection}")
           

           
except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Either your user name or password is incorrect")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
           
        else:
            print(e)