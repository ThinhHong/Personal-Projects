import mysql.connector

class userVerification:

    def __init__(self) -> None:
        #constructor
        pass

    def create_user(string: str) -> None:

        user_name = input("Enter your username")
        pwd = input("Enter Your Password: ")
        pwd2 = input("Confirm Password : ")
        while pwd != pwd2: 
            print("Passwords do not match")
            pwd = input("Enter Your Password: ")
            pwd2 = input("Confirm Password : ")

        

        
    