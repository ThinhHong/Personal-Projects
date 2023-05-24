import base64
import os
import maskpass
import bcrypt
import mysql.connector
import configparser
import pathlib
import sys
import math
from mysql.connector import connect, errorcode, Error

cwd = os.getcwd()
os.chdir(cwd)
print(cwd)

config = configparser.ConfigParser()
try:
    config.read('config_users.ini')

except Exception as e:
        print(f'Could not read configuration file {e}')
        sys.exit()

my_host = config['user_database']['host']
my_username = config['user_database']['username']
my_password = config['user_database']['password']
my_database = config['user_database']['database']

class Encryption:
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def reverse_encrypt(string: str) -> str:

        encrypt = ""
        for i in range(len(string) -1, -1,-1):
            char = string[i]
            encrypt += char

        return encrypt

    def encrypt(string: str, foward: int) -> str:
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

    def transposition_encryption(string: str, length: int) -> list:
        list = []
        for i in range(0,len(string), length):
            split = string[i:i + length]
            list.append(split)

        print(list)
        encrypted = ""

        for i in range(length):
            for value in list:
                if i >= len(value):
                    break
                encrypted += value[i]
        return encrypted


    def transpostion_hack(string: str,length: int):
        no_col_pre = length
        no_row_pre = math.ceil(len(string)/length)
        no_uneven = (no_col_pre * no_row_pre) - len(string)
        no_row_uneven = no_row_pre - 1
        full = no_col_pre - no_uneven
        start = 0
        list = []
        i = 0
        decrypted = "" 
        while i < len(string):
            if start >= full:
                split = string[i: i+no_row_uneven]
                i += no_row_uneven
            else: 
                split = string[i: i + no_row_pre]
                i += no_row_pre
            start += 1
            list.append(split)

        for i in range(no_col_pre):
            for value in list:
                if i >= len(value):
                    break
                decrypted += value[i]

        return decrypted

    def encode_password(password: str) -> str:
        
        new = base64.b64encode(password)
        return new
    
    def decode_password(password: str) -> str:
        
        new = base64.b64decode(password)
        return new

    def xor_ord(int1: int, int2: int) -> str:

        xor = int1 ^ int2
        xor_length = (xor.bit_count()+7) // 8
        return xor.to_bytes(xor_length, byteorder='big').decode()
    
    def xor_binary(byte1: str, byte2: str) -> str:

        xor = zip(byte1,byte2)
        xor_str = ''
        for int1, int2 in xor:
            xor_str += str(int(int1) ^ int(int2))

        return xor

    def add_user(connection: connect,encryption_type :str, length, rollback_on_error: bool=False) -> None:
        username = input("Enter Your Username : ")
        #maskpass allows for input from user privately

        pwd = input("Enter Your Password: ")
        pwd2 = input("Confirm Password : ")
        while pwd != pwd2: 
            pwd = input("Enter Your Password: ")
            pwd2 = input("Confirm Password : ")
        encrypt = encryption_type(pwd,length)
        try:
            with connection.cursor() as cursor:
                query = f"INSERT INTO user VALUES ({username},{pwd})"
                print(query)
                cursor.execute(query)
                connection.commit()
                print("User has been succesful added")
                      
        except Error as e:
                print(f"Error has occured: {e}")
                if rollback_on_error:
                    connection.rollback()      
                raise

b = "00001"
c = "00010"
d = zip(b,c)
f = 'de'
g = ['a','b','c']
print(f.join(g))

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