# 1.
def compute_roots(a, b, c):
   if ((b*b-4*a*c)<0): #Check if there are no roots
       return ['no roots!']
   x=((b*-1)+((b*b)-4*a*c)**0.5)/(2*a) #x=The positive root
   y=((b*-1)-((b*b)-4*a*c)**0.5)/(2*a) #y=The negative root
   if((b*b-4*a*c)==0): #Check for the same root
       return[x,'none']
   return [x,y] #Return the roots

# 2.
def isSumDivided(x):
    sumx = 0
    while x:
        sumx, x = sumx + x % 10, x // 10 #Sum the digits in the number
    sumdiv = sumx + 1
    while sumx: #Keep running until break
        if((sumdiv)%sumx > 0):  #Check when the lowest dividier of the sumx
            sumdiv=sumdiv+1
        else:
            break
    return(sumdiv)

# 3.
def triangle(x):
    if(x>0 and x<10): #First if to postivie number
        for i in range(x): #Number of rows we will need
            for m in range (i+1): #Counting the number it self for know how much to print from him
                print(i+1,end="")
            print("")
    elif(x<0 and x>-10): #Second if for negative number
        for i in range(-x): #Number of rows we will need
            for m in range(-x-i-1): #This loop is for the spaces
                print(" ",end="")
            for z in range (i+1): #This loop is for the numbers
                print(i+1,end="")
            print("")
    else:
        print("wrong value")

# 4.
def histograph(str):
    i = 1
    while(i<len(str)): #loop that runs from 0 until our input is finish
        number = str[i] #Making index for the number after each letter
        while(int(number)>0):
           print(str[i-1],end="") #Print the letter before the number
           number=int(number)-1
        i=i+2 #Skip the next letter
    print(" ")

# 5.
def separate(str1, str2):
    i=1
    x1="" #Our first string in the list
    x2="" #Our second string in the list
    while(i<len(str1)): #Run until our index is out of the len
        x1=x1+str1[i].upper() #Making the first word
        i=i+2
    i=0
    while (i < len(str2)):
        x2 = x2 + str2[i].lower() #Making the second word
        i = i + 2
    return([x1,x2])

# 6.
def primeList(limit):
    """..."""
    x=2
    ourlist = []
    while(x<limit): #Will run from 2 untill our input
         for i in range(2, x): #Check all the numbers between 2 to the number in the while loop
             if (x % i)==0: #Prime checking
                   break #If its prime we will do nothing, so we can break
         else:
             ourlist.append(x) #If its a prime, add it to a list
         x=x+1
    print(ourlist)