Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # The code
from collections import deque

# function to check if its a valid identifier
def check_var(variable):
    for char in variable:
        if char.isdigit():
            return False
    return True
    
#function to add the variable to dictionary
def add_id(id_list):
    if check_var(id_list[0]):
        try:
            identifier[id_list[0]] = int(id_list[1])
        except ValueError:
            if check_var(id_list[1]):
                try:
                    identifier[id_list[0]] = identifier[id_list[1]]
                except KeyError:
                   print("Unknown Variable")
            else:
                print("Invalid assignment")
    
    else:
        print("Invalid identifier")
        return None
    try:
        for i in range(2, len(id_list)):    
            # if id_list[i] == "=":
            if id_list[i] != id_list[i-1]:
                print("Invalid assignment") 
    except IndexError:
        return None       

# function to evaluate the result from postfix notion
def postfix_eval(lis_):
    operands = ["+", "-", "*", "/", "^"]
    result_stack = deque()
    for x in lis_:
        if x in operands:                   # if x is an operand pop 2 numbers
            try: 
                p = result_stack.pop()
                q = result_stack.pop()
                if x == "^":
                    result = q ** p
                elif x == "/":
                    result = q / p
                elif x == "*":
                    result = p * q
                elif x == "+":
                    result = p + q
                else:
                    result = q - p
                result_stack.append(result)         # put the result back to the stack
            except IndexError:
                print("Invalid expression")         # if there are any extra operands it prints error msg
                return None    
        else:
            result_stack.append(x)                  # since its a number, its directly added to stack
    if len(result_stack) == 1:                      # finally after the loop if there's only one element then its 
        y = result_stack.pop()                      # the final result
        if (y - int(y)) == 0:
            print(int(y))
        else:
            print(y)     
    else:                                           # If there are more numbers it means less operands are there 
        print("Invalid expression")                 # and prints an error msg   
        return None      

def in_to_pos(pos_list):
    priority_dict = {"(": 0, "^": 1, "/": 2, "*": 3, "-": 4, "+": 5}    # priority order
    priority_list = ["(", "^", "/", "*", "+", "-"] 
    in_list = []
    symbol_stack = deque()
    
    for x in pos_list:
        try:
            n = int(x)                                          # if its a number, its directly added to list
            in_list.append(n)
        except ValueError:
            if x in priority_list:                              # if x is an operand
                for i in range(0, len(symbol_stack)):
                    y = symbol_stack.pop()                      # we see the previous element   
                    if priority_dict[y] <= priority_dict[x]:     # if its lower priority than x
                        if y != "(":
                            in_list.append(y)                   # we add the previous element to list
                        else:                                   # if prev ele is ( then x is pushed to stack on 
                            symbol_stack.append(y)              # top of ( in the symbol_stack
                            symbol_stack.append(x)
                            break    
                    else:                                       # else if y has higher priority than x
                        symbol_stack.append(y)                  # x is pushed on top of y
                        symbol_stack.append(x)
                        break    
                if len(symbol_stack) == 0:                      # if no element is there prevoiusly then 
                    symbol_stack.append(x)                      # directly added to stack
                
            elif x == ")":                                      # if x is ) then popping must happen till (    
                try:
                    y = symbol_stack.pop()
                    while y != "(":
                        in_list.append(y)                       # the popped element must be added to list
                        y = symbol_stack.pop()                   
                except IndexError:                              # if more ) bracket is there then print error msg
                    print("Invalid expression")
                    return None        
    if "(" in symbol_stack:                                     # if more ( bracket is there then print error msg
        print("Invalid expression")
        return None
    else:                                                       # pop the remaining the elements to list
        for _ in range(len(symbol_stack)):
            y = symbol_stack.pop()
            in_list.append(y)

        postfix_eval(in_list)                                   # pass the resultant list to evaluate its postfix
        
#function to convert variables into their values
def id_to_val(lis_):
    operands = ["+", "-", "*", "/", "^", "(", ")"]
    for i in range(len(lis_)):
        if lis_[i] not in operands:             # if its not an operand                     
            try:
                y = int(lis_[i])                # if its a number convert to int to perform calculation
                lis_.pop(i)
                lis_.insert(i,y)
            except ValueError:                   
                if lis_[i] in identifier:       # check if its an existing variable
                    y = lis_.pop(i)             # then insert its equivalent value to list
                    lis_.insert(i,identifier[y])
                else:                           # if its not an existing variable then print error msg
                    print("Unknown variable")
                    return None 
                                                # if its an operand, its as it is in the list               
    in_to_pos(lis_) 

# function to calculate the equivalent symbol
def calc_symbol(lis_):
    symbol = 1
    for i in range(len(lis_)):
        if lis_[i] == "-":          # if there are odd no. of '-' sugn then returns '-' else '+' 
            symbol *= -1
                        
    if symbol == 1:
        return "+"
    return "-"   
    
# function to calculate the value of list
def calc(lis_):
    for i in range(len(lis_)):
        if lis_[i].endswith("-") or lis_[i].endswith("+"):      # checks if its a symbol    
            if len(lis_[i]) > 1:                                # if so checks if there are more than one symbol 
                symbol = calc_symbol(lis_[i])                   # calc_symbol calculates what equivalent symbol
                                                                # must be used
                lis_.pop(i)                         
                lis_.insert(i,symbol)
                
    id_to_val(lis_)

# function to check if a character is digit or not as isdigit() gives "False" for "-7"    
def isdigi(char):
    try:
        y = int(char)
        return True
    except ValueError:
        return False    

# funtion to convert the user enetered string to list form
def req_list(string):
    operands = ["(", ")", "*", "/", "^", "+", "-"]
    list_ = []
    count = 0                                   # counter variable to move through string
    while count != len(string):
        if string[count].isalpha():             # if its an alphabet, try to get the entire variable
            y = ""                             
            while string[count].isalpha():
                y = y + string[count]
                count += 1
                if count == len(string):
                    break
            list_.append(y)                     # the variable is added to the list
            if count == len(string):            # if only one is given as input we need to print its equivalent
                break                           # so there's a chance that we might need to terminate the loop here
            if isdigi(string[count]):           
                print("Invalid variable")       # if variable is followed by number then its an invalid identifier
                return None
            elif string[count] not in operands and string[count] != " ":
                print("Invalid expression")     # if its an operand it moves on to next iteration and there it is
                                                # processed  
                return None                     # if it has unkonown symbols then prints error msg
        elif string[count] in operands[:5]:
            list_.append(string[count])         # if its an operand directly added to list except +/-
            count += 1
        elif string[count] in operands[5:]:
            y = ""                              # if its +/- check for sequence
            while string[count] in operands[5:]:
                y += string[count]              # y has the entire sequence or it could be a single +/-
                count += 1
                if count == len(string):
                    break
            if len(y) == 1:                     # if its a single +/-
                if isdigi(string[count]):       # if next character is number
                    if len(list_) > 0:          # if its not the first character of the entire expression 
                        if not isdigi(list_[-1]) and not list_[-1].isalpha() and list_[-1] != ")":    
                                                # if there's already a sequence of symbol then its an unary    
                            while isdigi(string[count]):        # so entire no with unary is added to list
                                y += string[count]
                                count +=1    
                                if count == len(string):
                                    break
                            list_.append(y)
                        else:                   # if there's no sequnce before then its a symbol and not an unary
                            list_.append(y)     # hence the symbol is added to list
                    else:                       # if its the first character of entire expression
                        while isdigi(string[count]):    # then its an unary and hence added to the list
                            y += string[count]          # along with the number
                            count += 1
                            if count == len(string):
                                break
                        list_.append(y)
                elif string[count].isalpha():   # if its next character is variable
                    if len(list_) == 0:         # if its the first character
                        if y == "-":
                            list_.append("-1")
                        else:
                            list_.append("1")    
                        list_.append("*")       # to evaluate the result -1/1 * variable is done
                    else:                       
                        if not isdigi(list_[-1]) and not list_[-1].isalpha() and list_[-1] != ")":        
                            if y == "-":                 # if it has a sequence then its unary    
                                list_.append("-1")
                            else:
                                list_.append("1")    
                            list_.append("*")
                            y = ""
                            while string[count].isalpha():
                                y += string[count]
                                count +=1    
                                if count == len(string):
                                    break
                            list_.append(y)
                        else:                   # if no sequence its the symbol so its added directly
                            list_.append(y)    
                elif string[count] in operands[1:5]:    # if any operand follows +/- sign except ( then its 
                    print("Invalid expression")         # invalid expression   
                    return None
                elif string[count] == " " or string[count] == "(":      # if its space or ( then it is symbol
                    list_.append(y)                                     # and appended directly to list
            else:
                list_.append(y)                 # the sequence is directly added to list                                
        elif isdigi(string[count]):             # if its a number, append the entire number to list
            y = ""
            while isdigi(string[count]):        
                y += string[count]
                count += 1
                if count == len(string):
                    break
            list_.append(y) 
        elif string[count] == " ":              # space is skipped
            count += 1   
              
    calc(list_)
                    
    
identifier = {}
while True:
    n = input()
    if n == '/exit':
        print('Bye!')
        exit()
    if n == '/help':
        print("The program calculates the sum of numbers")
        continue  
    try:
        if n[0] != '/':     # checks if its not a command
            if "=" in n:
                assign_lis = n.split("=")
                new_lis = []
                for i in assign_lis:
                    new_lis.append(i.strip())
                add_id(new_lis)

            else:
                req_list(n)
        else:                                                   # if so prints unknown command
            print("Unknown command")
    except IndexError:                                          # if index error happens it means that its an empty line    
        continue   
                  
