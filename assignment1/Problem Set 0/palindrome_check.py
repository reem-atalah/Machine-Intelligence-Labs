import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    if(string == ""):
        return 1
    head:int = 0
    tail:int = len(string)-1
    while(head < tail):
        if(string[head] != string[tail]):
            return 0
        head +=1
        tail -=1
        
    return 1