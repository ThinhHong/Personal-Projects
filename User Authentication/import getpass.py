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
        #constructor
        pass
    
    @staticmethod
    def reverse_encrypt(string: str) -> str:
        """
    Reverses the order of characters in a given string.
    Parameters: string (str): The string to be reversed.
    Returns: str: The reversed string.
    """
        encrypt = ""
        for i in range(len(string) -1, -1,-1):
            char = string[i]
            encrypt += char

        return encrypt

    def encrypt(string: str, foward: int) -> str:
        """
    Pushes foward all characters in a given string.
    Parameters: string (str): The string to be pushes.
    Returns: str: The reversed string.
    """
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
        """
    Pushes foward all characters in a given string from 1-26. Prints out every possible decrypted message
    Parameters: string (str): The string to be decrypted.
    Returns: None.
    """
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

    def multiplicative_encrypt(string: str, foward: int) -> str:
        """
    Pushes foward all characters in a given string by a multiplicative .
    Parameters: string (str): The string to be pushes.
    Returns: str: The reversed string.
    """
        encrypted = ""
        for i in range(len(string)):
            char = string[i]
            if (char.islower()):
                uni = ord(char) * foward - 97
                new = chr((uni % 26) + 97)
                encrypted += new
            else:
                uni = ord(char) * foward -65
                new = chr((uni % 26) + 65)
                encrypted += new
        return encrypted


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

    def add_salt(password: str) -> str:
        return password + "ssaafdh"

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
                query = f"INSERT INTO user VALUES ({username},{encrypt})"
                print(query)
                cursor.execute(query)
                connection.commit()
                print("User has been succesful added")
                      
        except Error as e:
                print(f"Error has occured: {e}")
                if rollback_on_error:
                    connection.rollback()      
                raise
        
    def verify_user(connection: connect,encryption_type :str, length, rollback_on_error: bool=False) -> None:
        
        username = input("Enter Your Username : ")
        pwd = input("Enter Your Password: ")
        encrypt = encryption_type(pwd,length)
        try:
            with connection.cursor() as cursor:
                query = f"SELECT * FROM user WHERE user.name = '{username}' AND user.password = '{encrypt}'"
                print(query)
                cursor.execute(query)
                exist = cursor.fetchall()
                if exist == 0:
                    print("user does not exist")
                    return
                
                print("user is verified")
                      
        except Error as e:
                print(f"Error has occured: {e}")
                if rollback_on_error:
                    connection.rollback()      
                raise

b = "00001"
c = "00010"
 
d = 12
e = 21
def xor_ord(int1: int, int2: int) -> str:

        xor = int1 ^ int2
        xor_length = (xor.bit_count()+7) // 8
        return xor.to_bytes(xor_length, byteorder='big').decode()
    
def xor_binary(byte1: str, byte2: str) -> str:

    xor = zip(byte1,byte2)
    xor_str = ''
    for int1, int2 in xor:
        xor_str += str(int(int1) ^ int(int2))

    new_char = chr(int(xor_str,2)%26)
    return new_char

def xor_encryption(password: str,key: int) -> str:
    """
    Xor every charecter in a password by a key from 0-126
    Parameters: string (str): The string to be encrypted
    Returns: A string representing the encrypted password
    """
    uni_list = [ord(ch) for ch in password]
    xor_list = [key ^ uni for uni in uni_list]
    chr_list = [xor.to_bytes(((xor.bit_count()+7) // 8), byteorder='big').decode() for xor in xor_list]
    return ''.join(chr_list)
    
print(xor_encryption("Hello wrold!",7))

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