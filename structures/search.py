from quad_trees import OctreeSearch

def check_letter_inputs(letter):
    x=1
    while x==1:
        if len(letter)!=1 :
            letter=input("Hmm.. You entered more than one character please enter just one :\n")
            letter=check_letter_inputs(letter)
        if not letter.isalpha():
            print("We could not process that , it was not a letter!")
            letter=input("Please enter a letter: \n")
            letter=check_letter_inputs(letter)
        else:
            x=0
    return letter

def compare(start,end):

    return start, end

def get_letters():
    print("You are seaching for scientists! Lets look for the alphabetical range the surname may start with!")
    starting_letter=input("Please enter the letter from where you want us to start looking for :\n")
    start=check_letter_inputs(starting_letter).upper()
    ending_letter=input("Great! Now enter until which letter you want as to look for(it could be the same as the start) :\n")
    end=check_letter_inputs(ending_letter).upper()

    start,end=compare(start,end,state=1)
        
    letters=[start,end]

    return letters

def get_awards():
    awards=input("Please enter the least amount of awards you want the scientist to have: ")
    awards=check_digit(awards)
    return int(awards)

def check_digit(number):
    while not number.isdigit():
        print("Something wrong with the input, it was not a number.")
        number=input("Enter a number: ")
    return number

def compare(start,end,state):
    while start>end:
        print("Did you mean you want us to search from ",end,"to ",start," [yes or no]?")
        check=input()
        check=check.lower().strip()
        if check=='no':
            print("Let us start again.\n")
            if state==1:
                start,end=get_letters()
            else:
                start,end=get_dblp()
        elif check=='yes':
            # Swap the values for start and end
            start, end= end, start
        else:
            check=input("Enter 'yes' or 'no': ")
    return start,end

def get_dblp():

    print("Now, lets see how many dblp records the scientist ypur looking for has. Give us a range.")
    start=input("Enter the least number of records the scientist may have :\n")
    start=check_digit(start)
    end=input("Great! Enter the maximum number of records the scientist may have :\n")
    end=check_digit(end)
    
    
    start,end=compare(start,end,state=0)
    dblp=[int(start),int(end)]

    
    return dblp

letters=get_letters()
awards=get_awards()
dblp_range=get_dblp()
#example search only for alphabetica range input
x=OctreeSearch(letters,awards,dblp_range)
print('\n\nThe results from our searching are: \n\n')
for i in range(len(x)):
     print(x[i])


"""
EXAMPLE SEARCH
x=OctreeSearch(['z','z'],0,[4,118])

"""