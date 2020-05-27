import numpy as np
from scipy.optimize import linprog
from constraints import genMatrices,addNewConstraint
import math
import sys


def bnb(optimal,a,b,c,variables):
    res=linprog(method='simplex',c=c,A_ub=a,b_ub=b)
    temp=res.x.astype('int32')
    if(temp.all()==res.x.all()):
        if(res.fun<optimal):
            var=temp
            optimal=res.fun
        return optimal,var
    else:
        fractions=res.x-temp
        index=0
        maxFrac=fractions[0]
        for i in range(1,len(fractions)):
            if(fractions[i]>maxFrac):
                maxFrac=fractions[i]
                index=i
        string1=variables[index]+'<='+str(math.floor(res.x[index]))
        string2=variables[index]+'>='+str(math.ceil(res.x[index]))
        a1,b1=addNewConstraint(string1,a,b,variables)
        a2,b2=addNewConstraint(string2,a,b,variables)
        opt1,var1=bnb(optimal,a1,b1,c,variables)
        opt2,var2=bnb(optimal,a2,b2,c,variables)
        if(opt1<=opt2):
            return opt1,var1
        return opt2,var2

def main():
    Input=sys.argv[1]
    Sram=sys.argv[2]
    fil=open(Input,'r')
    lines=fil.readlines()
    a,b,c,variables=genMatrices(lines,sram=Sram)
    print(a,b,c)
    #exit()
    optimal=np.inf
    optimal,var=bnb(optimal,a,b,c,variables)
    if(optimal==np.inf):
        print("No integral solution found")
        return
    print('optimal number of line buffers = %d'%int(optimal))
    str1=''
    for i in range(len(variables)):
        str1+=variables[i]
        str1+='='
        str1+=str(int(var[i]))
        str1+='\n'
    print(str1[:-1])

if __name__=="__main__":
    main()