# you can write to stdout for debugging purposes, e.g.
# print "this is a debug message"

def solution(A):
    # write your code in Python 2.7
    
    dom = None
    dom_cnt = 0
    
    for val in A:
        
        if dom_cnt == 0:
            dom = val
            dom_cnt = 1
        else:
            if val == dom:
                dom_cnt += 1
            else:
                dom_cnt -= 1
    
    # dom could be the answer
    candidate = -1
    if dom_cnt > 0:
        candidate = dom
        
    # check if the candidate is the answer
    if A.count(candidate) > len(A)//2:
        return A.index(candidate)
    else:
        return -1