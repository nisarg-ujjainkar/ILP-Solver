import numpy as np
import copy
from helper import *


""" Function to add variable """
def addVar(var,A,C,variables):      
    A[var]=[]
    C[var]=[]
    variables.append(var)


""" Function to add constraints """
def addConstraint(string,A,B,C,width):
    constraint={}
    temp=''
    isPlus=True
    op=''
    readRHS=False
    lines=0
    offset=1
    for i in range(len(string)):
        if(string[i].isdigit()):
            temp+=string[i]
        elif(string[i]=='w'):
            if(readRHS==True):
                offset=int(temp)
                temp=''
            else:
                temp+=string[i]
        elif(string[i]=='l'):
            if(readRHS==True):
                num=int(temp)
                lines=int(width*(num-1))
                temp=''
            else:
                temp+=string[i]
        elif(string[i]=='*'):
            if(readRHS==False):
                num,temp=caseStar(temp)
        elif(string[i]=='+'):
            temp,isPlus=casePlus(temp,isPlus,constraint,num)
            #readRHS=True
        elif(string[i]=='-'):
            temp,isPlus=caseMinus(temp,isPlus,constraint,num)
            #readRHS=True
        elif(string[i]=='>'):
            temp,isPlus,op=caseGt(temp,isPlus,constraint,num)
            readRHS=True
        elif(string[i]=='<'):
            temp,isPlus,op=caseLt(temp,isPlus,constraint,num)
            readRHS=True
        elif(string[i]=='='):
            if(op=='gt'):
                op='geq'
            else:
                op='leq'
        else:
            temp+=string[i]
    for key in A.keys():
        if key in constraint:
            C[key].append(constraint[key])
            if(op=='gt' or op=='geq'):
                A[key].append(-1*constraint[key])
            else:
                A[key].append(constraint[key])
        else:
            A[key].append(0)
            C[key].append(0)
    num=lines+offset
    if(op=='gt' or op=='geq'):
        B.append(-1*num)
    else:
        B.append(num)


""" Function to add objective """
def addObjective(C,B,sram):
    # print(sram)
    if(sram=='single'):
        count={}
        toKeep=''
        Max=0
        iterable=list(C.keys())
        iterable.remove('Si')
        for i in range(len(C['Si'])):
            if(C['Si'][i]!=0):
                for j in iterable:
                    if(C[j][i]!=0):
                        count[j]=i
                        if(abs(B[i])>Max):
                            toKeep=j
                        break
        try:
            count.pop(toKeep)
            for i in list(count.keys()):
                C[i][count[i]]=0
                C['Si'][count[i]]=0
        except ValueError:
            pass
    keys=list(C.keys())
    keys.remove('Si')
    for i in keys:
        # print(i)
        count={}
        toKeep=''
        Max=0
        iterable=keys
        iterable.remove(i)
        # print(C[i])
        for j in range(len(C[i])):
            if(C[i][j]<0):
                for k in iterable:
                    if(C[k][j]!=0):
                        count[k]=j
                        if(abs(B[j])>Max):
                            toKeep=k
                        break
        # print(count,toKeep)
        try:
            count.pop(toKeep)
            for j in list(count.keys()):
                C[j][count[j]]=0
                C[i][count[j]]=0
        except KeyError:
            continue
    for i in list(C.keys()):
        C[i]=int(sum(C[i]))


""" Add virtual input stages """
def addVirtual(A,B,C,variables):
    count=0
    iterable=list(A.keys())
    iterable.remove('Si')
    for i in range(len(A['Si'])):
        if(A['Si'][i]!=0):
            count+=1
            A['Si'+str(count)]=[0]*len(A['Si'])
            A['Si'+str(count)][i]=A['Si'][i]
            C['Si'+str(count)]=-1*abs(A['Si'][i])
            variables.append('Si'+str(count))
    A.pop('Si')
    C.pop('Si')
    variables.remove('Si')


""" adding new constraint to existing set of constraints """
def addNewConstraint(string,A,B,variables):
    a=copy.deepcopy(A)
    b=copy.deepcopy(B)
    temp=''
    isPlus=True
    op=''
    for i in range(len(string)):
        if(string[i].isdigit()):
            temp+=string[i]
        elif(string[i]=='<'):
            var=temp
            temp=''
            op='lt'
        elif(string[i]=='>'):
            var=temp
            temp=''
            op='gt'
        elif(string[i]=='='):
            if(op=='gt'):
                op='geq'
            else:
                op='leq'
        elif(string[i]=='-'):
            isPlus=False
        else:
            temp+=string[i]
    num=int(temp)
    if(isPlus==False):
        num*=-1
    a=np.append(a,[[0]*len(a[0])],axis=0)
    index=variables.index(var)
    if(op=='gt' or op=='geq'):
        a[-1][index]=-1
        b.append(-1*num)
    else:
        a[-1][index]=1
        b.append(num)
    return a,b
        

""" Lexer Main """
def genMatrices(lines,sram='multi'):
    A={}
    C={}
    B=[]
    variables=[]
    for line in lines:
        if(line[0]=='#'):
            continue
        line=line.strip().split(' ')
        if(line[0]=='width'):
            width=int(line[1])
        if(line[0]=='var'):
            addVar(line[1],A,C,variables)
        if(line[0]=='con'):
            addConstraint(line[1],A,B,C,width)
    print(variables)
    addObjective(C,B,sram)
    A_ub=[]
    c=[]
    if(sram!='single'):
        addVirtual(A,B,C,variables)
    for i in variables:
        A_ub.append(A[i])
        c.append(C[i])
    A_ub=np.asarray(A_ub)
    A_ub=A_ub.transpose()
    return A_ub,np.asarray(B),np.asarray(c),variables
