# 1.


def compute_roots(a, b, c):
    # calculate the DeltaK
    d = (b ** 2) - (4 * a * c)
    if d < 0 or a == 0:
        return ["no roots"]
    # find the solutions
    sol1 = (-b - d**0.5) / (2 * a)
    sol2 = (-b + d**0.5) / (2 * a)
    if sol1 == sol2:  # condition for 1 solution
        return [sol1, "none"]

    return [sol1, sol2]


# Run for check
print(compute_roots(5, 0, -125))


# 2.
def isSumDivided(x):                  # x is positive integer
    def sum_digits(Number):           # internal function for digits' sum
        Sum = 0                       # sum of digits
        while Number > 0:             # loop to compute sum
            Reminder = Number % 10
            Sum = Sum + Reminder
            Number = Number // 10
        return Sum

    divisor = sum_digits(x) + 1          # call the internal function
    while divisor % sum_digits(x) != 0:  # loop to compute first divisor
            divisor = divisor + 1

    return divisor


print(isSumDivided(101))  # print fo check the function


# 3.
def triangle(x):
    if x > 0:
        for i in range(1, x+1):  # char for printing range
            for j in range(i):   # j run for the spaces number for each i
                if j < i - 1:
                    print(i, end='')
                else:
                    print(i),
    else:                             # negative case
        count = -x                    # count used as condition for spaces amount
        output = ""
        for i in range(1, -x + 1):    # value for output from 1 to -x +1
            for j in range(1, -x + 1):  # j run from start to end of output
                if j < count:           # condition for add a space
                    output = output + str(" ")
                else:
                    output = output + str(i)  # concatenate char i to output
            count = count - 1            # set the count for next run of i loop
            print(output)                # print each line
            output = ""                  # restart output


# run for a check
triangle(-4)


# 4.


def histography(str1):
    to_print0 = 0                               # index to letters in str1
    to_print1 = 1                               # index to numbers in str1
    to_print = ""                               # sum the finale expression to print
    while to_print1 < len(str1):                # loop to fill toPrint
        to_print = to_print + str(str1[to_print0]) * int(str1[to_print1])
        to_print0 = to_print0 + 2
        to_print1 = to_print1 + 2

    print(to_print)   # print


# run for a check
histography("a1b2c3d4f9")

# 5.


def seperate(str1, str2):
    element1 = ""                     # declare 2 elements to append
    element2 = ""
    list_elements = []                # output list
    for i in range(1, len(str1), 2):  # run on str1 by odd numbers
        element1 += str(str1[i])
    for j in range(0, len(str2), 2):  # run on str2 by even numbers
        element2 += str(str2[j])
    element1 = element1.upper()       # set to lower/upper letters
    element2 = element2.lower()
    list_elements.append(element1)    # append elements to output list
    list_elements.append(element2)
    print(list_elements)

    return list_elements


# run for a check
seperate("hello", "WORLD")
# 6.


def prime_list(limit):
    def isPrime(n):
        for i in range(2, int(n ** 0.5) + 1):  # check possible divisors until the square root
            if n % i == 0:                     # as was showed in class that sufficient to conclude prime num
                return False                   # if n is divided by one of the - n is not prime
        return True

    output_list1 = []                            # list for primes
    for j in range(2, limit + 1):                # loop for numbers 2 to limit
        if isPrime(j):                           # call to isPrime
            output_list1.append(j)               # append to the list if the num is prime
    return output_list1


# run for a check
print(prime_list(1000))
