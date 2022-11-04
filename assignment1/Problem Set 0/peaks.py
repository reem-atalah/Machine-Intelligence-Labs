from typing import List
import utils

def peaks(seq: List[int]) -> int:
    '''
    This function takes sequence of integers and returns the number of peaks.
    A peak is an element in the sequence whose value is higher than the two elements surrounding it.
    The first and last elements cannot be peaks.
    Any list containing less than 3 elements will have 0 peaks. 
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    if(len(seq) < 3):
        return 0

    countPeaks: int=0    
    for itr in range(1,len(seq)-1):
        if(seq[itr]> seq[itr+1] and seq[itr]> seq[itr-1]):
            countPeaks+=1

    return countPeaks


print(peaks([1,3,5,2,4,1]))