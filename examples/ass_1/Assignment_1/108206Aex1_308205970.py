# 1.

def compute_roots(a, b, c):
    if b ** 2 - 4 * a * c < 0:  # delta is negative, no roots
        print("['no roots!']")
    elif b ** 2 - 4 * a * c == 0:  # delta is 0, only one root
        print ("[",(int(-b +- (b**2-4*a*c)**0.5)/2*a), ",", "'none'","]")
    else:  # delta is positive, 2 roots.
        print ("[",(int(-b - (b**2-4*a*c)**0.5)/(2*a)),",", (int(-b + (b**2-4*a*c)**0.5)/(2*a)),"]")

# 2.

def isSumDivided(x):
    sum_digits = 0
    while x:  # sums the digits
        sum_digits += x % 10
        x //= 10
    big_num = sum_digits + 1
    while big_num % sum_digits != 0:  # finds the next first number that divides by the sum of the digits
        big_num += 1
    return big_num

# 3.

def triangle(x):
    if x < 10 and x > 0:
        x_minos_1 = x - 1
        while x - x_minos_1 != x + 1:  # prints a triangle that is left aligned
            for i in range(x - x_minos_1):
                print(x - x_minos_1, end = "")
            print("")
            x_minos_1 = x_minos_1 - 1
    elif x < 0 and x > -10:  # prints a triangle that is right aligned
        x_plus_1 = x - 1
        space = -x - 1
        for i in range(-x):
            for j in range(0,space):  # prints the spaces before the numbers
                print(end= " ")
            space = space-1
            for j in range(0,i+1):  # prints the numbers after the spaces
                print(x - x_plus_1, end = "")
            x_plus_1=x_plus_1-1
            print("")
    else:
        print("wrong value")
    return ""

# 4.

def histograph(str):
    even_number = str[1::2]  # letters
    odd_number = str[0::2]   # numbers
    for i in range(len(even_number)):   # prints each letter as many times as the number that is on the right
        print(odd_number[i]*int(even_number[i]), end = "")
    return ""

# 5.

def separate(str1, str2):
    str_even = str1[1::2]  # even letters from the first string
    str_odd = str2[0::2]   # odd letters from the second string
    New_list = [str_even.upper(), str_odd.lower()]
    print(New_list)


# 6.

def primeList(limit):
    prime_number_list = []
    for num in range(0, limit):
        if num > 1:
            for i in range(2, num):  # checks if the number is a prime number
                if num % i == 0:
                    break
            else:
                prime_number_list.append(num)   # adds the prime number to the list
                continue
    print(prime_number_list)
