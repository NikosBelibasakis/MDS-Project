
#this function checks if the input for the letter is in the correct form
def check_letter_inputs(letter):
    x=1
    while x==1:
        if len(letter)!=1 :
            letter=input("Hmm.. You entered more than one character please enter just one :\n")
            letter=check_letter_inputs(letter)
        if not (letter.isalpha() and 'A' <= letter.upper() <= 'Z'):
            print("We could not process that , it was not an english letter!")
            letter=input("Please enter a letter: \n")
            letter=check_letter_inputs(letter)
        else:
            x=0
    return letter

#this function checks if input is a digit
def check_digit(number):
    while not number.isdigit():
        print("Something wrong with the input, it was not a number.")
        number=input("Enter a number: ")
    return number

#this function checks the range, especially if input for the start is less or equal than the input from the end of the range
def compare(start,end,state):
    while start>end:
        print("Did you mean you want us to search from ",end,"to ",start," [yes or no]?")
        check=input()
        check=check.lower().strip()
        if check=='no':
            print("Let us start again.\n")
            if state==1: 
                #this state is for when we use this function for the comparison of letters
                start,end=get_letters()
            else:
                #this is for the comparison of digits
                start,end=get_dblp()
        elif check=='yes':
            # Swap the values for start and end
            start, end= end, start
        else:
            check=input("Enter 'yes' or 'no': ")
    return start,end

#this function  gets the range of the letters from the input
def get_letters():
    print("You are seaching for scientists! Lets look for the alphabetical range the surname may start with!")
    starting_letter=input("Please enter the letter from where you want us to start looking for :\n")
    start=check_letter_inputs(starting_letter).upper()
    ending_letter=input("Great! Now enter until which letter you want as to look for(it could be the same as the start) :\n")
    end=check_letter_inputs(ending_letter).upper()

    start,end=compare(start,end,state=1)

    return [start,end]

#this function gets the award threshold from the input
def get_awards():
    awards=input("Please enter the least amount of awards you want the scientist to have: ")
    awards=check_digit(awards)
    return int(awards)

#this input gets the range of dblp records from the input
def get_dblp():

    print("Now, lets see how many dblp records the scientist ypur looking for has. Give us a range.")
    start=input("Enter the least number of records the scientist may have :\n")
    start=check_digit(start)
    end=input("Great! Enter the maximum number of records the scientist may have :\n")
    end=check_digit(end)
    
    start,end=compare(int(start),int(end),state=0)
    
    return [int(start),int(end)]

"""
Now, that we have defined all the required functions for obtaining user-defined values:

1.alphabetical range 
2.threshold for awards
3.range of number of publications

we will use them for identifying scientists whose names fall alphabetically within the 
specified range, the number of awards they have received are greater than the threshold,
and the number of publications should also be within the user-defined range. This will 
be accomplished using the corresponding search function for each structure. 
So, in each tree structure we will the call the function bellow.
"""
#function that encapsulates all above functions
def get_searching_values():

    letters=get_letters()
    awards=get_awards()
    dblp_range=get_dblp()

    return letters,awards,dblp_range

