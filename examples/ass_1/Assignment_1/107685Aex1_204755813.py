# 1.

def compute_roots(a, b, c):
   delta=((b ** 2) - 4 * a * c)                            # defining the delta
   roots_results = []                                      # creating an empty list
   if delta < 0 :
      roots_result.append("no roots!")                     # if the delta is negative, adding "no roots" to our list
   elif delta == 0 :
        roots_results.append((-b/2*a))
        roots_results.append("none")                       # if the delta equals to zero, adding two values to our list: the result, and "none"
   else:
        roots_results.append((-b+(delta ** 0.5))/2*a)
        roots_results.append((-b-(delta ** 0.5))/2*a)      # if the delta is positive, adding two values to our list: one with "+" and the other with "-"
   return roots_results                                    # at the end, the function returns to us the list it created

#check:
#print (compute_roots (4,4,1))



# 2.

def isSumDivided(x):
    digits_sum = 0
    for digit in str(x):
        digits_sum = digits_sum + int(digit)       # "digits_sum" is zero at first, and its adding the summerize of the other digits to itself using a "for" loop
    return digits_sum *2                           # for finding the lowest divisor of our result, thats enough to multiply by 2
#check:
#print(isSumDivided(32324))




# 3.

def triangle(x):
    if (x<10 and x>0):
        for i in range(x):                    """"" for creating the triangle I'm multiply each character by itself, and than moving to the next line """
        print(str(i + 1) * (i + 1))           # I'm multiply by i+1 because that i want my triangle to start from 1 and not from 0
    elif (x<0 and x>-10):                     # for the right-side triangle i'm adding spaces, and changing the range for being minus x
        for i in range(-x):
            print(" "*(-x-i) + str(i + 1) * (i + 1))
    else:
        print ("wrong value")

#check:
#triangle(-4)



# 4.

def histograph(str):
    new_word = " "                                                         # creating a new string called "new word"
    for character in str:
        if character.isdigit():                                            # if the character in the argument is a digit:
            new_word = new_word + (new_word[-1] * (int(character) - 1))    # it takes the previous character in "new word" and multiply it by the founded digit minus 1 (because we already have the character once)
        else:
            new_word = new_word + character                                # if its not a digit, it takes "new word" and adds  the next character (for example: 'b')
    return new_word                                                        # returns us the final "new word" we created
#check:
#print (histograph('a1b2c3d4'))




# 5.
def separate(str1, str2):
    upper1 = str1.upper()                              # I created two strings and used upper and lower methods on them
    lower2 = str2.lower()
    ans1 = upper1[1::2]                                # afterwards, I changed the strings to be only even and odd numbers"""
    ans2 = lower2[0::2]
    list = [ans1, ans2]                                # adding my two final string into a list
    return list

#check:
#print (separate("hello","world"))


# 6.

def primeList(limit):
    list = []
    for i in range(2,limit+1):
        flag = True
        for j in range(2,i):
            if (i%j)==0:                    # if i%j==0 it means that i isn't a prime number
                flag = False
                break                       # when it happens, we go back to the loop of i
        if (flag == True):                  # if we finished the loop of j without any i%j==0, so the flag stays true, and we add i to our list.
            list.append(i)
    return list
#check:
#print (primeList(100))






