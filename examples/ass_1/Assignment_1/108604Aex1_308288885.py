# # # 1.
#
# def compute_roots(a, b, c):
#     x = []
#     if b ** 2 - 4 * a * c < 0:
#         x.append("no roots!")
#         return x
#     elif b ** 2 - 4 * a * c == 0:
#         x.extend([-b / 2 * a, "none"])
#         return x
#     else:
#         x.extend([(-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a), (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)])
#         return x



#2
 def isSumDivided(x):
     y=sum(int(digit) for digit in str(x))
     return y*2
#
# # 3.
#
# def triangle(x):
# # if 0<x<10:
# #         for i in range(1,x+1):
# #             print (str(i)*i)
# #     elif -10<x<0:
# #         for i in range(1, abs(x)+1):
# #             print(' '*(abs(x)-i)+str(i)*i)
# #     else: print('wrong value')
# # triangle(2)

# # 4.
#
# def histograph(str):
#     for i in range(1, (len(x) + 1), 2):
#         print(x[i - 1] * int(x[i]))


# histograph(x)

# 5.
# def separate(str1, str2):
#     str1_1=str1[0:len(str1)+1:2]
#     str2_2=str2[1:len(str2)+1:2]
#     print(str1_1.upper()," ",str2_2.lower())

# # 6.
# def primeList(limit):
#     for i in range(2, limit):
#         for j in range(2, i):
#             if (i % j) == 0:
#                 break
#
#         else:
#             print(i)
#
#
# primeList(100)




