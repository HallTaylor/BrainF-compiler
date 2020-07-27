import sys
import time

class Error(Exception):
    """Base class for errors"""
    pass

class LoopMismatch(Error):
    """Raised when opening and closing brackets are mismatched"""

def shrink(file, char_set):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(){}\|=':;\"\?"
    f = open(file,"r")
    code = f.read()
    string = ""
    for i in code:
        string +=i
    string = ''.join(string.split())
    for char in chars:
        string = string.replace(char,"")
    return string

#compile() shrinks the txt file to only legal characters
def compile(file):
    char_set = ("+","-",".",",","[","]",">","<") #the legal characters
    array = [0 for i in range(100)]
    comms = shrink(file,char_set)

    #Loop Def
    def loop(comm):
        comms = comm
        n = 0
        f = 0
        for i in comms:     #runs through the code and finds all open and closed brackets for LoopMismatchError
            if i == "[":
                n += 1
            if i == "]":
                f += 1
        try:
            if n != f:     #if there is a missing bracket or if brackets are mismatched raise an error
                raise LoopMismatch
        except LoopMismatch:
                print("Error: missing closing bracket")
                sys.exit()
        looper_array = [[None for y in range(2)] for x in range(int((n+f)/2))] #Set the array for the loops
        m = 0
        for i, item in enumerate(comms):    #for each command, if it's a open brakcet
            if item == "[":                 #then add its position to looper_array
                looper_array[m][0] = i      #then add one to m
                m+=1                        
        temp_array = looper_array
        
        for i, item in enumerate(comms):    #Same, but wih closed brackets. It's more complicated :(
            if item =="]":
                closest = 100
                val_loc = 0
                loc = ()
                for x in temp_array:                        #for each tuple in looper_array, take the closest value to
                    if (abs(i-x[0])) < (abs(i-closest)):    #the current bracket and pair them, then remove the brackets
                        if x[0] < i:                        #from cconsideration
                            if x[1] == None:
                                closest = x[0]                  
                                val_loc = temp_array.index(x)
                                loc = x
                looper_array[val_loc][1] = i
        return looper_array
                
    loop_array = loop(comms)
    ptr_loc = 0 #pointer location
    comm_loc = 0 #current command
    def inc(ptr_loc): #Increments the pointer by one
        ptr_loc +=1
        return ptr_loc
    def dec(ptr_loc): #Decrements the pointer by one
        ptr_loc-=1
        return ptr_loc
    def plus(ptr_loc): #adds one to the value of the cell the pointer is located at
        array[ptr_loc] +=1
    def sub(ptr_loc): #subtracts one from the value of the cell the pointer is located at
        array[ptr_loc] -=1
    def out(ptr_loc): #outputs the byte value of the cell
        print(str(chr(array[ptr_loc])))   #yeah I know print works, but its for compeleteness
    def inp(ptr_loc): #takes in one byte of input to the cell
        array[ptr_loc] = input("Enter a number, i guess? ")
    def o_loop(loop_array, ptr_loc,comm_loc): #if the value of the current cell is 0, jump to the corresponding closing loop
        if array[ptr_loc] == 0:
            for y in loop_array:
                for x in y:
                    if x == comm_loc:
                        comm_loc = loop_array[loop_array.index(y)][1]
        else:
            inc(ptr_loc)
    def c_loop(loop_array,ptr_loc,comm_loc): #if value of the current cell is not 0, jump to the corresponding opening loop
        if array[ptr_loc] != 0:              #in the command sequence
            for y in loop_array:
                for x in y:
                    if x == comm_loc:
                        comm_loc = loop_array[loop_array.index(y)][0]
        else:
            inc(ptr_loc)
            comm_loc +=1
        return comm_loc
    
    while True:
        if comm_loc >= len(comms):
            sys.exit()
        item = comms[comm_loc]
        if item ==">":
            ptr_loc = inc(ptr_loc)
            comm_loc+=1
        if item =="<":
            ptr_loc = dec(ptr_loc)
            comm_loc+=1
        if item ==".":
            out(ptr_loc)
            comm_loc+=1
        if item ==",":
            inp(ptr_loc)
            comm_loc+=1
        if item =="+":
            plus(ptr_loc)
            comm_loc+=1
        if item =="-":
            sub(ptr_loc)
            comm_loc+=1
        if item =="[":
            o_loop(loop_array,ptr_loc,comm_loc)
            comm_loc+=1
        if item =="]":
            comm_loc = c_loop(loop_array,ptr_loc,comm_loc)
#compile("Bruh.txt")


while True:
    put = input(">")
    compile(put)
