# 1.


def compute_roots(a, b, c):
    if 4*a*c > b**2:
        return ['no roots!']
    elif 4*a*c == b**2:
        return [-b/(2*a), 'none']
    else:
        return [(-b+((b**2)-4*a*c)**0.5)/(2*a), (-b-((b**2)-4*a*c)**0.5)/(2*a)]


# 2.

def isSumDivided(x):
    total_sum_digits = 0
    while x > 0:   # this is a loop for suming the digits of the number
        digit = x % 10
        total_sum_digits += digit
        x = x//10  # double // give me the int of the division
    return total_sum_digits * 2


"""i could have find the first biggest
number divided in a while loop but i think this way is faster and more efficient"""


# 3.

def triangle(x):
    result = ''
    if 0 < x < 10:
        for i in range(1, x + 1):
            result += str(i)*i + '\n'
        return result
    elif -10 < x < 0:
        x = abs(x)
        for i in range(1, x + 1):
            result += (x-i)*" " + str(i)*i + '\n'  # i am using spaces to move the triangle to the right
        return result
    else:
        return 'wrong value'


# 4.

def histograph(str):
    letter = []
    result = ''
    for i in str:
        if i.isdigit():
            result += letter*int(i)
        else:
            letter = i
    return result


# 5.

def separate(str1, str2):
    result = ['', '']
    for i in range(0, len(str1)):
        if i % 2 != 0:
            result[0] += str1[i].upper()
    for j in range(0, len(str2)):
        if j % 2 == 0:
            result[1] += str2[j].lower()
    return result


# 6.

def primeList(limit):
    prime_num = []

    def prime(limit):  # first i will check if a number is prime
        for j in range(2, limit):
            if limit % j != 0:
                continue
            else:
                return False
        return True
    for i in range(2, limit):
        if prime(i) == True:
            prime_num.append(i)
    return prime_num
