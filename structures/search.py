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


print("You are seaching for scientists! Lets look for the alphabetical range the surname may start with!")
starting_letter=input("Please enter the letter from where you want us to start looking for :\n")
start=check_letter_inputs(starting_letter)
ending_letter=input("Great! Now enter until which letter you want as to look for(it could be the same as the start) :\n")
end=check_letter_inputs(ending_letter)

letters =[start,end]

#example search only for alphabetica range input
x=OctreeSearch(letters,0,[4,118])
for i in range(len(x)):
     print(x[i])

#THINGS TO DO:
#1. put more comments to quads
#2.you need to develop a way to compare if the letters provided where in order and not like start='w' and end = 'a'
#3. develop input functions for awards and dblp

"""
EXAMPLE SEARCH

x=OctreeSearch(['z','z'],0,[4,118])
for i in range(len(x)):
     print(x[i])

"""