import numpy as np
from scipy.optimize import linprog
from constraints import genMatrices


a,b,c,variables=genMatrices()
#print(A,B,C)
#print(a,b,c)
#exit()
res=linprog(method='simplex',c=c,A_ub=a,b_ub=b)
str1=''
str2=''
for i in range(len(variables)):
    str1+=variables[i]
    str1+='='
    str1+=str(int(res.x[i]))
    str1+='\n'
print(str1[:-1])
# print(str2)
print('optimal number of elements',res.fun)
#res1=linprog(method='simplex',c=C1,A_ub=A1,b_ub=B1)
# print(res)
# print(res.x)
# print(res.fun)
#print(res1)