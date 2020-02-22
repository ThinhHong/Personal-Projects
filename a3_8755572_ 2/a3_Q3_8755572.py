def longest_run(run):
    """
    list->int
    Preconditions:input a list of numbers seperated by a spalce
    return highest run in a list
    """
    if len(run)==0:
        x=0
    elif len(run)==1:
        x=1
    else:
        x=2
        for i in range(len(run)-1):
            if run[i]==run[i+1]:
                x=x+1
               
        print(x)
                    

run=input("Please enter a sequence of numbers seperated by a space").strip().replace(" ","")
run=list(run)
longest_run(run)
