print("Welcome to the game!")
answer = input("Do you want to play").strip().lower()  

if answer == 'yes':
    print("Okay lets start")
else: 
    print("Thats too bad")
    quit()

name = input("What is your name").strip().lower()
print (f'Hello {name}, Welcome to your grand adventure!')

direction = input("Would you like to go straight, left , right or backwards?").strip().lower()

if direction == 'left':
    print ("You have encountered a new village")
    enter = input("Would you like to enter to prepare?").strip().lower()
    if enter == 'yes':
        print("You have prepared to fight the demon king")
        fight = input("Will you fight?").strip().lower()
        if fight == 'yes':
            print("Congrats!, You have defeated the demon king and brought peace")
        elif enter == 'no':
           print("GAME OVER!, you have fleed from battle")

    elif enter == 'no':
        fight = input("Will you face the demon king without any preperation?").strip().lower()
        if fight == 'yes':
            print("GAME OVER! you have failed to defeat the demon king due to lack of prepeartion")
        elif enter == 'no':
           print("GAME OVER!, you have fleed from battle")

elif direction == 'backwards':
    print('GAME OVER!, you have chosed to return from your adventure')
    quit()

elif direction == 'foward':
    print("You have gone towards the devil's castle")
    enter = input("Will you enter and fight?").strip().lower()
    if enter == 'yes':
        print("You have failed and died since you didn't prepare")
        quit()

elif direction == 'right':
    print("You have fallen into quicksand and died :(")
    quit()

else:
    print("You have done nothing untill the end of time")
    quit()