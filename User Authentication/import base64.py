import base64
import maskpass

database = {"kevin": "dadkgdgsz", "abel": "nihaocloud", "user_3": "123456"}
username = input("Enter Your Username : ").lower()
for key in database.keys():
    if username == key:
        password = input("Enter Your Password : ").lower()
        while password != database.get(key):
            password = input("Re-enter Your Password : ")   
        print("Welcome")
        print("User Verified")



# Accept user password input
pwd = maskpass.askpass()
 
# Encoding the string
encode = base64.b64encode(pwd.encode("utf-8"))
print("str-byte : ", encode)
 
# Decoding the string
decode = base64.b64decode(encode).decode("utf-8")
print("byte-str : ", decode)