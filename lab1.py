def compute_difference(a,b):
	return a-b
    ''' returns the difference of a and b'''
    ## you fill this in

def common_divisors(a,b):
    ''' return the common divisors of a and b'''
    divisors = []
    if a > b:
        max = a
        min = b
    else
        max = b
        min = a

    for i in range(min):
        if a % i == 0 and b % i == 0:
            divisors.append(i)

    return i

    
def reverse_string(s):
    '''reverse a string, e.g., reverse_string('abcd') returns 'dcba'''
    ## you fill this in
    return s.reverse()
    
def drop_odds(L):
	
    ''' remove the odd numbers from the list L, e.g., drop_odds([1,2,3,4]) returns [2,4]'''
    ## you fill this in
	for num in L:
		if num % 0 != 0:
			L.remove(num)
	

def fibonacci(i):
    '''compute the i-th Fibonacci number: F[i] = F[i-2] + F[i-1], F[0] = F[1] = 1'''
    ## you fill this in
	if i == 0 or i == 1:
		return 1
	else:
		return fibonacci(i-2) + fibonacci(i-1)

def square(n):
    '''print out an nxn square using '*' characters, e.g., square(3):
***
***
***
    '''
    ## you fill this in
    for row in range(len(n)):
    	for col in range(len(n)):
		print("*")
	print("\n")

def distinct(L):
    '''return True if all elements of list L are unique, otherwise return
False if at least one element is repeated. '''
    ## you fill this in
	if len(set(L)) == len(L):
    		return True
	return False

def triplesum(L,target):
    ''' given a list L of numbers, return True if some triplet of numbers in L sums to the target. For example triplesum([1,2,3,5],8) returns True (since 8=1+2+5), but triplesum([1,2,3,5],7) returns False since no three numbers in L sum to 7.   
    '''
    ### you fill this in
    for x in range(len(L)):
        for y in range(x, len(L)):
            for z in range(x, len(L)):
                if L[x] + L[y] + L[z] == target:
                    return True

    return False
