def primelist(limit): # def not work. i didn't succes.
    list1 = []  # list to get all the primes
    for i in range(2,limit+1): # the range is of all numbers betweem 2 to the input number
        div = 2
        while i >= div: # because if i< div we need to conitnue to the next number
            if i % div ==0: # not prime, continue
                continue
            for x in range(div,i): # i try to find a way to run on any divisibale number from 2 to i, i think that here is my mistake
                if i % x ==0: # not prime, we can break and continue
                    break
                elif i % x != 0 : # try all the numbers in the range and if none is divided by none, so he is a prime and return him
                    x = x +1
                    return i
        list1.append(i)

    print (list1)

primelist(int(input('enter a num : ')))