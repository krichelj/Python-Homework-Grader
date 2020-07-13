# 1.


def compute_roots(a, b, c):
    x = []
    if b ** 2 - 4 * a * c < 0:
        x.append("no roots!")
        return x
    elif b ** 2 - 4 * a * c == 0:
        x.extend([-b / 2 * a, "none"])
        return x
    else:
        x.extend([(-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a), (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)])
        return x


print(compute_roots(5, 0, -125))


# 2.
def sum_div(x):
    y = sum(int(i) for i in str(x))
    return y*2

print(sum_div(32324))


# 3.

def triangle(x):
    if n > 0 and n < 10:

        for i in range(1, n + 1):
            print(str(i) * i)

    elif n < 0 and n > (-10):

        for i in range(1, n * -1 + 1):
            print(' ' * (n * -1 - i) + str(i) * i)

    else:
        return print("wrong value")


triangle(4)

# 4.

def histograph(str):


    for i in range(1, (len(x) + 1), 2):
        print(x[i - 1] * int(x[i]))


# 5.
def separate(str1, str2):


    b = e[1:len(e)+1:2]

    d=f[0:len(f)+1:2]

    return print(b.upper()+","+d.lower())


# 6.

def primeList(limit):
    for i in range(2, limit):
        for j in range(2, i):
            if (i % j) == 0:
                break

        else:
            print(i)


primeList(100)