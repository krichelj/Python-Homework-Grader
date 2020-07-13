# 1.
def compute_roots(a,b,c):
    delta = b**2-4*a*c
    if delta<0:
        return "['no roots!']"
    elif delta==0:
        x = -b/(2*a)
        return [x, 'none']
    else:
        x = (-b + delta**0.5)/(2*a)
        y = (-b - delta**0.5)/(2*a)
        return [x, y]
print(compute_roots(int(input('enter a: ')),int(input('enter b: ')),int(input('enter c: '))))

# 2.
def isSumDivided(x):
    string_x = str(x)
    sum_sfarot = 0
    divide = True
    n = 1
    for i in range(len(string_x)):
        sum_sfarot += int(string_x[i])
    while divide:
        if ((n%sum_sfarot==0) & (n>sum_sfarot)):
            divide = False
        else:
            n += 1
    return (n)
print(isSumDivided(int(input('enter x: '))))

# 3.
def triangle(x):
    if ((x<10) & (x>0)):
        for i in range(x):
            print(str(i+1) * (i+1))
    elif ((x>-10) & (x<0)):
        for i in range(-x):
            print(str(" ") * (-x-i), str(i+1) * (i+1))
    else:
        print("wrong value")
triangle(int(input('enter x: ')))

# 4.
def histograph(str):
    x = ""
    for i in range(1, len(str), 2):
        for j in range(int(str[i])):
            x = x + str[i-1]
    return(x)
print(histograph(str(input('enter str: '))))

# 5.
def separate(str1,str2):
    location1 = ""
    location2 = ""
    for i in range(1, len(str1), 2):
        location1 = location1 + str.upper(str1[i])
    for j in range(0, len(str2), 2):
        location2 = location2 + str.lower(str2[j])
    return [location1, location2]
print(separate(str(input('enter str1: ')),str(input('enter str2: '))))

# 6.
def primeList(limit):
    lst = [2]
    for i in range(3, limit):
        n = 2
        while (i%n!=0) & (i>n):
            n += 1
        if (i == n):
            lst.append(i)
    return lst
print(primeList(int(input('enter limit: '))))