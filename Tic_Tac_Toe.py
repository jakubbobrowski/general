from random import choice
from time import sleep

fieldsLeft = [1, 2, 3, 4, 5, 6, 7, 8, 9]
fieldsComputer = []
fieldsUser = []
counter = 0
computerFirstMove = 5

def gui():
    def XOcheck(n):
        if n in fieldsComputer:
            return "X"
        elif n in fieldsUser:
            return "O"
        else:
            return n
    
    print(XOcheck(1), "|", XOcheck(2), "|", XOcheck(3))
    print("---------")
    print(XOcheck(4), "|", XOcheck(5), "|", XOcheck(6))
    print("---------")
    print(XOcheck(7), "|", XOcheck(8), "|", XOcheck(9))
    
def userTurn():
    while True:
        try:
            fieldChosen = int(input("Choose field: "))
            if fieldChosen in fieldsLeft:
                fieldsLeft.remove(fieldChosen)
                fieldsUser.append(fieldChosen)
                print("User put O on field: ", fieldChosen)
                gui()
                break
            elif fieldChosen not in range(1, 9):
                print("Provide a value from 1 to 9")
            else:
                print("This field is occupied, choose a different one")
            
        except:
            print("This is not a valid integer")
    fieldsUser.sort()
         
def computerTurn():
    sleep(1)
    global counter
    if counter == 0:
        fieldsLeft.remove(computerFirstMove)
        fieldsComputer.append(computerFirstMove)
        counter += 1
        print("Computer put X on field: ", computerFirstMove)
    else:
        fieldChosen = choice(fieldsLeft)
        fieldsLeft.remove(fieldChosen)
        fieldsComputer.append(fieldChosen)
        counter += 1
        print("Computer put X on field: ", fieldChosen)
    gui()
    fieldsComputer.sort()
    
def whoWon():
    winningCombinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9], 
        [1, 4, 7], [2, 5, 8], [3, 6, 9], 
        [1, 5, 9], [3, 5, 7]
    ]
    for combination in winningCombinations:
        if all(field in fieldsComputer for field in combination): 
            return "Computer won"
        elif all(field in fieldsUser for field in combination):
            return "User won"
     
def game():
    gui()
    startCommand = input("Input s to start: ")
    while startCommand != "s":
        startCommand = input("Input s to start: ")

    while fieldsLeft:
        computerTurn()
        if whoWon() == "Computer won":
            print(whoWon())
            break
        if not fieldsLeft: 
            print("Tie")
            break
        userTurn()
        if whoWon() == "User won":
            print(whoWon())
            break

game()
