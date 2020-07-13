def compute_roots(a, b, c):
    """check if there are no roots, there is one root, or there are two roots and print the right option."""
a = 1
b = 2
c = 1
if (b**2 - 4 * a * c) < 0:
    print("['no roots!']")
elif (b**2 - 4 * a * c) == 0:
    print("[", (int(-b+-(b**2 - 4 * a * c) * 0.5) / (2 * a)), ",", "'none'", "]")
else:
    print("[",(int(-b-(b**2 - 4 * a * c)**0.5)/(2 * a)),",",(int(-b+(b**2 - 4 * a * c) ** 0.5)/(2 * a)),"]")

    # 2.

def isSumDivided(x):
    sum_num = 0
    """ To get the sum of the digits of the number, I take the remainder of the division at 10 (%), and then divide
    it again until the rest is 0. every time I add the rest to the last one and get the sum of the digits."""
    while x>0:
        sum_num += x % 10
        x//=10
    higher_num = sum_num +1
    """I define a new variable and every time that I divide this var by the sum of the digits and the rest is 
        not 0, I add plus one to the var. In the end of the loop I get the smaller number that divide by the sum of 
        digits."""
    while higher_num % sum_num !=0:
        higher_num += 1
    return higher_num
print(isSumDivided(111))


    # 3.
def triangle(x):
    number_plus_1 = 1
    """ I define a new variable that starts with 1, and every time that x is bigger then 1, I take the range of the 
     number and print it in the same line, then, I add 1 to this number until we get the number of x."""
    if x<10 and x>0:
        while x >= number_plus_1:
            for i in range(number_plus_1):
                print(number_plus_1, end="")
            number_plus_1 = number_plus_1 + 1
            print("")
    elif x > -10 and x < 0:
        """The second condition is for negative numbers, and I make them positive by reducing them from zero."""
        while (0-x) >= number_plus_1:
            """I take the range between the number and the variable and print the number of spaces according to it
            in the same line."""
            for i in range((0-x)-number_plus_1):
                print(" ", end="")
                """I print the numbers as before with the earnings in the same line"""
            for i in range(number_plus_1):
                print(str(number_plus_1), end="")
            number_plus_1 = number_plus_1 + 1
            print("")
    else:
        print("wrong value")
    return ""
print(triangle(-7))


# 4.

def histograph(stri):
    """I separate the string for two strings, one for numbers and one for letters."""
    stri_a = stri[1::2]
    stri_b = stri[0::2]
    """For each index I multiply the letter by the number of times of the number in the same index."""
    for i in range(len(stri_a)):
        print(stri_b[i]*int(stri_a[i]), end="")
    return ""
print(histograph("a1b2c3d4"))

    # 5.


def separate(str1, str2):

    """I separate the string for two strings, one for odd numbers, and the other for even numbers."""
    str_1 = str1[1::2]
    str_2 = str2[0::2]
    """I define a new list with the strings and the functions of upper and lower, and print is."""
    list_new = [str_1.upper(), str_2.lower()]
    print (list_new)
separate("hello", "world")


    # 6.


def primeList(limit):
    """I define a new variable for a list."""
    num_list = list(range(2,limit))
    """I take all the numbers that are higher then 1 from the number of the limit. and then I check for every number
    if there are numbers except from 1 and himself, that it can divide with modulo 0. if there are - I remove them 
    from the list. then I print the list only with the prime numbers."""
    for num in range(0, limit):
        if num > 1:
            for i in range(2, num):
                if num % i == 0:
                    num_list.remove(num)
                    break
            else:
                continue
    print(num_list)
primeList(100)